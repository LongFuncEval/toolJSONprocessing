import json

from generate_qa_pairs.tasks.data_structures import LongResponseQASample


def get_prompt(qa_sample: LongResponseQASample) -> str:

    prompt_template = (
        "You are given a response from an API call (in JSON format). "
        "Answer the question based on the information provided in the API response.\n\n"
        "```json\n{api_response}\n```\n\n"
        "Question: {question}\n\n"
        "Only respond with the answer. Do not include any other text or json in the response.\n\n"
        "Answer:"
    )

    prompt = prompt_template.format(
        api_response=json.dumps(qa_sample.api_response, indent=4),
        question=qa_sample.question,
    )

    return prompt


def get_prompt_schema(qa_sample: LongResponseQASample) -> str:

    prompt_template = (
        "You will be given a JSON object as data which is a response from a REST API containing information returned from the API call."
        "You are given a response from an API call (in JSON format). "
        "Answer the question based on the information provided in the API response.\n\n"
        "```json\n{api_response}\n```\n\n"
        "Question: {question}\n\n"
        "Only respond with the answer. Do not include any other text or json in the response.\n\n"
        "The JSON schema of the object given as data is as follows: <<json_schema>>"
        "Answer:"
    )

    prompt = prompt_template.format(
        api_response=json.dumps(qa_sample.api_response, indent=4),
        question=qa_sample.question,
        json_schema=qa_sample.schema
    )

    return prompt



def cot_get_prompt_schema(qa_sample: LongResponseQASample) -> str:

    prompt_template = (
        "You will be given a JSON object as data which is a response from a REST API containing information returned from the API call."
        "You are given a response from an API call (in JSON format). "
        "Answer the question based on the information provided in the API response.\n\n"
        "```json\n{api_response}\n```\n\n"
        "Question: {question}\n\n"
        "Think step-by-step about how the data relates to the question being asked."
        " Analyze the structure and contents of the JSON response. "
        "Identify which fields are relevant to the question. "
        "Then, reason through the data logically to derive the answer. "
        "Finally, provide the answer accurately.\n\n"
        "Only respond with the answer. Do not include any other text or json in the response.\n\n"
        "The JSON schema of the object given as data is as follows: <<json_schema>>"
        "Answer:"
    )

    prompt = prompt_template.format(
        api_response=json.dumps(qa_sample.api_response, indent=4),
        question=qa_sample.question,
        json_schema=qa_sample.schema
    )

    return prompt