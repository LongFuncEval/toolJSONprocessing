import json
import os
import types
from typing import Any
from multiprocessing import Pool
import inspect, textwrap

from generate_qa_pairs.tasks.data_structures import LongResponseQASample
from generate_qa_pairs.tasks.utils import generate, get_lm
from codegen_scripts.general_code_generation import (
    PromptStyle,
    get_answer_from_json,
)
from codegen_scripts import direct_prompting_code
from counterfactuals import extract_json_paths, filter_data_by_keys,filter_schema_by_keys
import importlib

try:
    from dotenv import load_dotenv
    load_dotenv()
    print(os.getenv("LLM_PROVIDER"))
except ImportError:
    pass

def get_prompt(qa_sample: LongResponseQASample, setup_type: str):
    prompt = ""
    if setup_type == "direct_prompting":
        prompt = direct_prompting_code.get_prompt(qa_sample)
    elif setup_type == "direct_prompting_schema" or setup_type == "direct_prompting_schema_cfx2":
        prompt = direct_prompting_code.get_prompt_schema(qa_sample)
    elif setup_type == "cot_direct_prompting_schema":
        prompt = direct_prompting_code.cot_get_prompt_schema(qa_sample)
    return prompt

def get_prompt_style(setup_type: str) -> PromptStyle:
    if setup_type == "code_generation":
        return PromptStyle.ZERO_SHOT
    elif setup_type == "code_generation_schema" or setup_type == "code_generation_schema_cfx2":
        return PromptStyle.ZERO_SHOT_WITH_RESPONSE_SCHEMA
    elif setup_type == "code_generation_schema_no_resp":
        return PromptStyle.ZERO_SHOT_WITH_NO_RESPONSE
    elif setup_type == "code_generation_schema_compact_response":
        return PromptStyle.ZERO_SHOT_WITH_COMPACT_RESPONSE
    elif setup_type == "cot_code_generation_schema":
        return PromptStyle.ZERO_SHOT_WITH_COT_RESPONSE_SCHEMA

def get_api_response_cf(api_response,schema,sample,task):

    if "Hotel" in task:
        module = 'generate_qa_pairs.tasks.booking_search_hotel_by_coordinates'
    elif "Car" in task:
        module = 'generate_qa_pairs.tasks.booking_search_car_rentals'
    elif "last10k" in task or "SEC" in task:
        module = 'generate_qa_pairs.tasks.SEC_filings'
    elif "real-time" in task or "Shoes" in task:
        module = 'generate_qa_pairs.tasks.product_details_shoes'
    elif "Availability" in task:
        module = 'generate_qa_pairs.tasks.booking_rooms_with_availability'
    elif "Map" in task:
        module = 'generate_qa_pairs.tasks.booking_get_seat_map'

    module = importlib.import_module(module)
    try:
        task_list_cls = getattr(module, sample['task'])
    except:
        print("Get the correct tasklist")

    task_list_obj = task_list_cls()
    path_keys = extract_json_paths(textwrap.dedent(inspect.getsource(task_list_obj.get_answer)))
    api_response = filter_data_by_keys(api_response, path_keys)
    schema = filter_schema_by_keys(schema=schema, keys=path_keys)
    return (api_response, schema)


def run_inference(qa_pairs: list[LongResponseQASample], setup_type: str, model_name: str, llm_parameters: dict[str, Any]) -> list[LongResponseQASample]:
    output_list = []
    llm = get_lm(model_name, parameters=llm_parameters)

    if "code_generation" in setup_type:
        prompt_style = get_prompt_style(setup_type)
        for qa_pair in qa_pairs:
            answer = get_answer_from_json(
                api_response=qa_pair.api_response,
                query=qa_pair.question,
                llm_object=llm,
                model_name=model_name,
                prompt_style=prompt_style,
                few_shots="",
                json_schema=qa_pair.schema
            )
            try:
                qa_pair.model_output = answer[0]
                if isinstance(answer[1], types.GeneratorType):
                    qa_pair.pred_answer = ', '.join(map(str, answer[1]))
                else:
                    qa_pair.pred_answer = answer[1]

                if isinstance(answer[2], types.GeneratorType):
                    qa_pair.code_exec_status = ', '.join(map(str, answer[2]))
                else:
                    qa_pair.code_exec_status = answer[2]

            except BaseException:
                if isinstance(answer, (list, tuple)):
                    qa_pair.model_output = answer[0]
                else:
                    qa_pair.model_output = answer

                if "maximum context length" in str(answer):
                    qa_pair.pred_answer = "context length exceeded"
                    qa_pair.code_exec_status = None
                else:
                    qa_pair.pred_answer = None
                    qa_pair.code_exec_status = None
            output_list.append(qa_pair)
    else:
        if len(qa_pairs) > 0:
            prompts = [
                get_prompt(qa_sample=qa_sample, setup_type=setup_type) for qa_sample in qa_pairs
            ]
            try:
                generations = generate(
                    llm=llm, model_name=model_name, prompts=prompts, temperature=0
                )
            except BaseException as e:
                if "maximum context length" in str(e):
                    generations = ["context length exceeded" for i in range(len(prompts))]
                else:
                    generations = [str(e) for i in range(len(prompts))]

        for qa_sample, generation in zip(qa_pairs, generations):
            qa_sample.pred_answer = generation
            output_list.append(qa_sample)
    return output_list


if __name__ == "__main__":
    setup_types = [
        "direct_prompting",
        "direct_prompting_schema",
        "code_generation",
        "code_generation_schema",
        "code_generation_schema_no_resp",
        "code_generation_schema_compact_response",
        "cot_direct_prompting_schema",
        "cot_code_generation_schema",
        "direct_prompting_schema_cfx2",
        "code_generation_schema_cfx2",
    ]

    task_lists = [ #sorted by size
        "booking-com15.p.rapidapi.com_Search_Hotels_By_Coordinates",
        "booking-com15.p.rapidapi.com_Search_Car_Rentals",
        "booking-com15.p.rapidapi.com_Get_Seat_Map",
        "real-time-product-search.p.rapidapi.com_search?",
        "last10k-company-v1.p.rapidapi.com_v1_company_filings",
        "booking-com15.p.rapidapi.com_Get_Room_List_With_Availability",
    ]
    model_names = [
        "Azure/gpt-4o",
        # "GCP/claude-4-sonnet",
        # "meta-llama/Llama-3.1-8B-Instruct",
        # "meta-llama/Llama-3.2-3B-Instruct",
        # "meta-llama/Llama-3.1-8B-Instruct",
        # "ibm-granite/granite-3.3-8b-instruct",
        # "meta-llama/llama-4-maverick-17b-128e-instruct-fp8",
        # "deepseek-ai/DeepSeek-V3",
        # "mistralai/mixtral-8x22B-instruct-v0.1",
        # "meta-llama/llama-3-3-70b-instruct",
        # "deepseek-ai/DeepSeek-R1-Distill-Llama-70B",
        # "Qwen/Qwen3-Coder-480B-A35B-Instruct-FP8",
        # "Qwen/Qwen3-235B-A22B-Instruct-2507",
        # "Qwen/Qwen3-8B",
        # "deepseek-ai/deepseek-r1",
        # "openai/gpt-oss-20b",
        # "openai/gpt-oss-120b",
        # "meta-llama/llama-3-405b-instruct",
        # "mistralai/mistral-large",
        # "meta-llama/llama-3-2-3b-instruct",
        # "mistralai/Devstral-Small-2507",
    ]

    llm_parameters = {
        "max_new_tokens": 1000,
        "min_new_tokens": 1,
        "top_p": 0.1,
        "temperature": 0.0,
        "random_seed": 1,
        "decoding_method": "greedy",
        "stop_sequences": [],
    }

    num_processes = 40
    for model_name in model_names:
        for setup_type in setup_types:
            if 'cf' in setup_type: # for counterfactual analysis
                simplify_json = True
            else:
                simplify_json = False
            for task in task_lists:
                if os.path.exists(os.path.dirname(__file__) + f"/results/predictions/{task}_{model_name.split('/')[1]}_{setup_type}_predictions.json"):
                    print("SKIPPING: " + f"{task}_{model_name.split('/')[1]}_{setup_type}")
                    continue
                # Load json file with QA pairs
                task_file = "../generate_qa_pairs/data/qa_pairs/" + task + "_qa_pairs.json"
                with open(task_file, 'r') as file:
                    qa_pairs = json.load(file)
                # Build LongSampleQA
                qa_pair_obj_list = []
                updates_qa_pairs_obj_list = []
                for sample in qa_pairs:
                    with open("../generate_qa_pairs/data/" + sample['api_response_path'], 'r', encoding='utf-8') as f:
                        tmp = json.load(f)
                        api_response = tmp[sample["app"]][sample["endpoint"]][sample["api_query"]]
                    with open("../generate_qa_pairs/data/" + sample['api_response_schema'], 'r', encoding='utf-8') as f:
                        schema = f.read()
                    if simplify_json:
                        # Simplify the json response to only keep paths which are required by the get_answer method
                        schema = json.loads(schema)
                        api_response, schema = get_api_response_cf(api_response, schema, sample, task)
                        schema = str(schema)

                    qa_pair_obj = LongResponseQASample(api_response=api_response,
                                                       question=sample['question'],
                                                       gold_answer=sample['gold_answer'],
                                                       schema=schema,
                                                       pred_answer=None,
                                                       model_output=None,
                                                       code_exec_status=None,
                                                       metrics=sample['metrics'],
                                                       task=sample['task'],
                                                       task_type=sample['task_type'],
                                                       uid=sample['uid'])
                    qa_pair_obj_list.append(qa_pair_obj)

                # Call the model
                if num_processes == 0:
                    updates_qa_pairs_obj_list = run_inference(qa_pair_obj_list, setup_type, model_name, llm_parameters)
                else:
                    args = []
                    for sample in qa_pair_obj_list:
                        args.append(([sample], str(setup_type), str(model_name), dict(llm_parameters)))
                    with Pool(processes=num_processes) as pool:
                        output_lists = pool.starmap(
                            run_inference, args
                        )
                    for output_list in output_lists:
                        updates_qa_pairs_obj_list.extend(output_list)  # _with_changed_prompt_again

                # Save the new json file with predicted answer and intermediary outputs
                results = []
                for sample in updates_qa_pairs_obj_list:
                        results.append({
                            "endpoint": task,
                            "setup_type": setup_type,
                            "model": model_name,
                            "uid": sample.uid,
                            "api_response": sample.api_response,
                            "question": sample.question,
                            "gold_answer": sample.gold_answer,
                            "schema": sample.schema,
                            "task": sample.task,
                            "task_type": sample.task_type,
                            "predicted_answer": sample.pred_answer,
                            "code_exec_status": sample.code_exec_status,
                            "model_output": sample.model_output,
                            "metrics": sample.metrics
                        })
                with open(os.path.dirname(__file__) + f"/results/predictions/{task}_{model_name.split('/')[1]}_{setup_type}_predictions.json",
                          "w") as file:
                    json.dump(results, file)