import json
import logging
from enum import Enum
from typing import Any
import ast
import inspect
from dotenv import load_dotenv

from generate_qa_pairs.tasks.utils import get_lm, invoke_llm


# initialize logging
logging.basicConfig(
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.DEBUG,
)

logger = logging.getLogger()

load_dotenv()

ZERO_SHOT_TEMPLATE = """
You will be given a JSON object as data which is a response from a REST API containing information returned from the API call.
Your task is to extract and return <<task_prefix>>

Write a Python function that:
    Starts the function with "def ".
    Takes only the entire api response as input and doesn't have any other input.
    Identifies the structure of the input data, ensuring it checks for relevant keys and data types.
    When comparing strings, it should always convert both sides of the comparison to lowercase.
    Processes the provided data.
    Iterates through the data to extract relevant information.
    Cleans numeric strings by removing non-numeric characters before converting them to integers.
    Performs proper checks to ensure a key exists and is not None before querying its value.
    Returns only the requested data as a string and no other extra information or words.
    Do not add any extra keys or terms to the output.

Final Check:
    The function must be formatted in Python markdown for direct execution.
    No explanations, comments, or additional text should be included.
    Do not include any example usage.

data = <<json_obj>>

Python Function:

"""


ZERO_SHOT_TEMPLATE_WITH_RESPONSE_SCHEMA = """
You will be given a JSON object as data which is a response from a REST API containing information returned from the API call.
You will be given a JSON schema of the response from the REST API returned from the API call.
Your task is to extract and return information from the JSON object which follows the JSON schema and answers the user query: <<task_prefix>>

You need to write a Python function that:
    Starts the function with "def ".
    Takes only the entire api response as input and doesn't have any other input.
    Identifies the structure of the input data, ensuring it checks for relevant keys and data types.
    When comparing strings, it should always convert both sides of the comparison to lowercase.
    Processes the provided data.
    Iterates through the data to extract relevant information.
    Cleans numeric strings by removing non-numeric characters before converting them to integers.
    Performs proper checks to ensure a key exists and is not None before querying its value.
    Returns only the requested data as a string and no other extra information or words.
    Do not add any extra keys or terms to the output.

Final Check:
    The function must be formatted in Python markdown for direct execution.
    No explanations, comments, or additional text should be included.
    Do not include any example usage data.

The JSON schema of the object given as data is as follows: <<json_schema>>

data = <<json_obj>>

Python Function:

"""

ZERO_SHOT_TEMPLATE_WITH_COT_RESPONSE_SCHEMA = """
You will be given a JSON object as data which is a response from a REST API containing information returned from the API call.
You will be given a JSON schema of the response from the REST API returned from the API call.
Your task is to extract and return information from the JSON object which follows the JSON schema and answers the user query: <<task_prefix>>


Think step-by-step:
    - First, analyze the structure of the JSON data using the schema.
    - Identify which fields are relevant to the task and understand their data types.
    - Consider edge cases like missing keys, null values, or unexpected types.
    - When comparing strings, normalize them to lowercase.
    - When handling numeric strings, remove non-numeric characters before converting to integers.
    - Use logical iteration and condition checks to extract the required information.
    - Ensure that only the expected value is returned, formatted strictly as a string.

You need to write a Python function that:
    Starts the function with "def ".
    Takes only the entire api response as input and doesn't have any other input.
    Identifies the structure of the input data, ensuring it checks for relevant keys and data types.
    Processes the provided data.
    Iterates through the data to extract relevant information.
    Cleans numeric strings by removing non-numeric characters before converting them to integers.
    Performs proper checks to ensure a key exists and is not None before querying its value.
    Returns only the requested data as a string and no other extra information or words.
    Do not add any extra keys or terms to the output.

Final Check:
    The function must be formatted in Python markdown for direct execution.
    No explanations, comments, or additional text should be included.
    Do not include any example usage data.

The JSON schema of the object given as data is as follows: <<json_schema>>

data = <<json_obj>>

Python Function:

"""

ZERO_SHOT_TEMPLATE_WITH_NO_RESPONSE = """
Your task is to work with an already-loaded JSON object as a dictionary from a REST API response. 
Using the provided JSON schema, you need to extract and return information that directly answers the user's query: <<task_prefix>>

You need to write a Python function that:
    Starts the function with "def ".
    Takes only the entire api response as input and doesn't have any other input.
    Identifies the structure of the input data, ensuring it checks for relevant keys and data types.
    When comparing strings, it should always convert both sides of the comparison to lowercase.
    Processes the provided data.
    Iterates through the data to extract relevant information.
    Cleans numeric strings by removing non-numeric characters before converting them to integers.
    Performs proper checks to ensure a key exists and is not None before querying its value.
    Returns only the requested data as a string and no other extra information or words.
    Do not add any extra keys or terms to the output.

Final Check:
    The function must be formatted in Python markdown for direct execution.
    No explanations, comments, or additional text should be included.
    Do not include any example usage data.

The JSON schema of the object given as data is as follows: <<json_schema>>

Python Function:

"""

ZERO_SHOT_TEMPLATE_WITH_COMPACT_RESPONSE = """
You will be given a JSON object as data which is an example or compact version of the response from a REST API containing information returned from the API call.
You will be given a JSON schema of the response from the REST API returned from the API call.
Your task is to take reference and return information from the JSON object which follows the JSON schema and answers the user query: <<task_prefix>>

You need to write a Python function that:
    Starts the function with "def ".
    Takes only the entire api response as input and doesn't have any other input.
    Identifies the structure of the input data, ensuring it checks for relevant keys and data types.
    When comparing strings, it should always convert both sides of the comparison to lowercase. This is mandatory.
    Processes the provided data.
    Iterates through the data to extract relevant information.
    Cleans numeric strings by removing non-numeric characters before converting them to integers.
    Performs proper checks to ensure a key exists and is not None before querying its value.
    Returns only the requested data as a string and no other extra information or words.
    The data to be returned from the function should be in string.
    Do not add any extra keys or terms to the output.

Final Check:
    The function must be formatted in Python markdown for direct execution.
    There should be ```python in the beginning and the ending should be ```.
    No explanations, comments, or additional text should be included.
    Do not include any example usage data.

The JSON schema of the object given as data is as follows: <<json_schema>>

data = <<json_obj>>

Python Function:

"""


def extract_code_and_get_output(model_response: str, response_arr: Any) -> Any:
    try:
        start_idx = model_response.find("```python")
        if start_idx == -1:
            start_idx = model_response.find("def ")
            if start_idx == -1:
                raise ValueError("Python code block not found in response.")
            else:
                model_response_first_part = model_response
        else:
            model_response_first_part = model_response[start_idx + 9 :]

        end_idx = model_response_first_part.find("```")
        if end_idx != -1:
            code = model_response_first_part[:end_idx].strip()
        else:
            code = model_response_first_part.strip()

        if "# Example usage:" in code:
            logger.debug("Removing example usage section from code.")
            code = code.split("# Example usage:")[0]

        def_find = code.find("def")
        first_open_parenthesis = code.find("(")
        function_name = code[def_find +4:first_open_parenthesis].strip()

        tree = ast.parse(code)
        for node in tree.body:
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                compiled = compile(ast.Module(body=[node], type_ignores=[]), filename="<ast>", mode="exec")
                exec(compiled, globals())

        exec(
            code, globals()
        )  # Executes the function definition and adds in the globals namespace

        if function_name in globals():
            code_result = eval(
                f"{function_name}({response_arr})"
            )  # actual function call
            del globals()[function_name]  # Clean up global namespace
            return code_result
        else:
            raise ValueError(
                f"Function {function_name} not found after execution, code: {code}"
            )

    except Exception as e:
        logger.error(f"Error during code execution: {e}")
        print(f"Error during code execution: {e}")
        return "Code execution error"


class PromptStyle(Enum):
    ZERO_SHOT = ZERO_SHOT_TEMPLATE
    ZERO_SHOT_WITH_RESPONSE_SCHEMA = ZERO_SHOT_TEMPLATE_WITH_RESPONSE_SCHEMA
    ZERO_SHOT_WITH_NO_RESPONSE = ZERO_SHOT_TEMPLATE_WITH_NO_RESPONSE
    ZERO_SHOT_WITH_COMPACT_RESPONSE = ZERO_SHOT_TEMPLATE_WITH_COMPACT_RESPONSE
    ZERO_SHOT_WITH_COT_RESPONSE_SCHEMA=ZERO_SHOT_TEMPLATE_WITH_COT_RESPONSE_SCHEMA

def get_answer_from_json(
    api_response: dict[str, Any],
    query: str,
    llm_object: Any,
    model_name: str,
    prompt_style: Enum = PromptStyle.ZERO_SHOT,
    few_shots: str = "",
    json_schema: str = ""
) -> Any:

    print(f"Question: {query}")
    template = str(prompt_style.value)
    if "<<example>>" in template:
        template = template.replace("<<example>>", few_shots)

    if prompt_style == PromptStyle.ZERO_SHOT_WITH_RESPONSE_SCHEMA or prompt_style== PromptStyle.ZERO_SHOT_WITH_NO_RESPONSE or prompt_style==PromptStyle.ZERO_SHOT_WITH_COMPACT_RESPONSE or prompt_style==PromptStyle.ZERO_SHOT_WITH_COT_RESPONSE_SCHEMA:
        if json_schema is None or json_schema == "":
            raise ValueError("Json schema can not be None or empty for prompt style PromptStyle.ZERO_SHOT_WITH_RESPONSE_SCHEMA")
        template = template.replace("<<json_schema>>", json_schema)

    if prompt_style != PromptStyle.ZERO_SHOT_WITH_NO_RESPONSE:
        if prompt_style == PromptStyle.ZERO_SHOT_WITH_COMPACT_RESPONSE:
            def get_all_keys(obj, parent_keys=None):
                """
                Recursively gather all unique keys in a JSON structure.
                """
                if parent_keys is None:
                    parent_keys = set()
                if isinstance(obj, dict):
                    for k, v in obj.items():
                        parent_keys.add(k)
                        get_all_keys(v, parent_keys)
                elif isinstance(obj, list):
                    for item in obj:
                        get_all_keys(item, parent_keys)
                return parent_keys

            def reduce_json_by_unique_keys(obj, known_keys=None):
                """
                Reduce JSON structure but keep items in lists that add new keys.
                """
                if known_keys is None:
                    known_keys = set()

                if isinstance(obj, dict):
                    new_obj = {}
                    for k, v in obj.items():
                        reduced_value = reduce_json_by_unique_keys(v, known_keys)
                        new_obj[k] = reduced_value
                    return new_obj

                elif isinstance(obj, list):
                    reduced_list = []
                    for item in obj:
                        item_keys = get_all_keys(item)
                        if not item_keys.issubset(known_keys):
                            known_keys.update(item_keys)
                            reduced_list.append(reduce_json_by_unique_keys(item, known_keys))
                    return reduced_list

                else:
                    return obj

            reduced_data = reduce_json_by_unique_keys(api_response)


            prompt = template.replace("<<task_prefix>>", query.lower()).replace(
                "<<json_obj>>", str(reduced_data)
            )
        else:
            prompt = template.replace("<<task_prefix>>", query.lower()).replace(
                "<<json_obj>>", str(api_response)
            )
    else:
        prompt = template.replace("<<task_prefix>>", query.lower())

    logger.info(f"Model used: {model_name}")

    try:
        model_response = invoke_llm(llm_object, prompt, model_name)
        print("Model response:", model_response, "###########################")
        eval_output = extract_code_and_get_output(model_response, api_response)
        if eval_output == "Code execution error":
            code_output = None
        else:
            code_output = eval_output
        print("Code output:", code_output)
    except BaseException as e:
        print("Exception during code generation", e)
        return None


    return (model_response, code_output, eval_output)

