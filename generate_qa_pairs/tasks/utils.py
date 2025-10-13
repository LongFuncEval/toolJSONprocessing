import json
import os
from enum import Enum
from typing import Any, Dict, List, Tuple, Union
import ast

from genai.extensions.langchain.chat_llm import LangChainChatInterface
from langchain_core.language_models import BaseLLM
from langchain_ollama import OllamaLLM
from pydantic import SecretStr
from transformers import AutoTokenizer

from openai import OpenAI, AzureOpenAI

from .data_structures import LongResponseQASample

class LLM_Options(Enum):
    AUTO = (1,)
    LOCAL = 5
    AZURE = 6


def get_lm(
    model_id: str,
    llm_provider: Enum = LLM_Options.AUTO,
    parameters: dict[str, Any] | None = None,
) -> Any:
    # returns LLM provider, Auto selects based on env variable, defaults to WatsonX
    provider_env = os.getenv("LLM_PROVIDER", "azure").lower()
    if llm_provider == LLM_Options.AUTO:
        if provider_env == "local":
            return get_lm_local(model_id, parameters=parameters)
        elif provider_env == "azure":
            return get_lm_azure(model_id)


def get_lm_local(model_id: str, parameters: Any) -> BaseLLM:
    llm = OllamaLLM(model=model_id, **parameters)
    return llm



def get_lm_azure(model_id:str) -> AzureOpenAI:
    api_version = ""
    if "gpt" in model_id:
        api_version = "2024-08-01-preview"
    endpoint_url = os.getenv("AZURE_ENDPOINT").format(model_id=model_id.split("/")[1], api_version = api_version)
    return AzureOpenAI(
        azure_endpoint=endpoint_url,
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=api_version
        )


def invoke_llm(llm_object: Any, prompt: str, model_id: str) -> Any:
    if isinstance(llm_object, LangChainChatInterface):
        try:
            response = llm_object.invoke(prompt)
        except BaseException as e:
            raise e
        return response.content
    elif isinstance(llm_object, OpenAI):
        try:
            response = llm_object.chat.completions.create(
                model=model_id,
                messages=[{"role": "user", "content": prompt}],
                temperature=0,
                max_tokens=1000,
                stop=["\nObservation"],
            )
        except BaseException as e:
            raise e
        return response.choices[0].message.content


def get_model_prompt(conversation: list[dict[str, str]], model_name: str) -> Any:
    model_name_hf_map = {
        "meta-llama/llama-3-1-70b-instruct": "meta-llama/llama-3.1-70b-instruct",
        "mistralai/mixtral-8x22B-instruct-v0.1": "mistralai/Mixtral-8x22B-Instruct-v0.1",
        "ibm-granite/granite-3.1-8b-instruct": "ibm-granite/granite-3.1-8b-instruct",
        "deepseek-ai/DeepSeek-V3": "deepseek-ai/DeepSeek-V3",
    }
    try:
        tokenizer = AutoTokenizer.from_pretrained(
            model_name_hf_map[model_name], token=os.getenv("HF_TOKEN")
        )
    except BaseException as e:
        raise e
    return tokenizer.decode(tokenizer.apply_chat_template(conversation))


def generate(
    llm: Any,
    model_name: str,
    prompts: list[str] | str,
    temperature: float = 0,
    max_tokens: int = 256,
    stop: Any = None,
) -> list[str]:

    generations = []
    if isinstance(llm, AzureOpenAI):
        for prompt in prompts:
            num_retries = 0
            while num_retries <= 10:
                try:
                    completions = llm.chat.completions.create(
                        model=model_name,
                        messages=[{"role": "user", "content": prompt}],
                        temperature=temperature,
                        max_tokens=max_tokens,
                        # stream=False,
                        timeout = 3600,
                        stop=stop
                    )
                    generation = completions.choices[0].message.content
                    generations.append(generation)
                    break
                except Exception as e:
                    import traceback
                    print("!! inside exception, sleeping", num_retries)
                    print(traceback.format_exc())
                    time.sleep(200)
                    num_retries += 1
    elif isinstance(llm, OpenAI):
        completions = llm.completions.create(
            model=model_name,
            prompt=prompts,
            temperature=temperature,
            max_tokens=max_tokens,
            # stream=False,
            timeout = 3600,
            stop=stop,
        )

        generations = [choice.text for choice in completions.choices]

        print(generations)
        return generations  # .content
    return generations

def convert_dict_to_list_of_objects(json_dict):
    return_list = []
    for record in json_dict:
        qa_pair_obj = LongResponseQASample(api_response=record['api_response'],
                        question=record['question'],
                        gold_answer=record['gold_answer'],
                        schema=record['schema'],
                        pred_answer=record['predicted_answer'],
                        model_output=record['model_output'],
                        code_exec_status=record['code_exec_status'],
                        metrics=record['metrics']['exact_match_metric'],
                        task=record['task'],
                        task_type=record['task_type'],
                        uid=record['uid'])

        return_list.append(qa_pair_obj)
    return return_list