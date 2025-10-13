import re
from typing import Any

from generate_qa_pairs.tasks.utils import generate
from sentence_transformers import SentenceTransformer, util
from pint import UnitRegistry

from generate_qa_pairs.tasks.data_structures import LongResponseQASample


def accuracy_string(task: LongResponseQASample, normalize: bool = True) -> bool:
    if not isinstance(task.gold_answer, str) or not isinstance(task.pred_answer, str):
        return False

    if normalize:
        gold_ans = task.gold_answer.strip().lower()
        pred_ans = task.pred_answer.strip().lower()
    else:
        gold_ans = task.gold_answer
        pred_ans = task.pred_answer

    if pred_ans.endswith("."):
        pred_ans = pred_ans[:-1]

    return (gold_ans == pred_ans)


def approx_number_match(task: LongResponseQASample, rounding: bool = True) -> bool:
    """We expect the gold answer to be a single number, but the model output can have multiple numbers.
    The match will return True if any of the numbers from the predicted answer matches the gold answer, with or without rounding.
    Likely that the model output will not match the exact number, can be rounded, with a $ sign etc.

    Parameters
    ----------
    task : LongResponseQASample
    rounding : bool, optional
        whether to account for rounding for the match, by default True

    Returns
    -------
    bool
        whether any of the numbers in the predicted answer matches the gold answer
    """
    if not isinstance(task.gold_answer, str) or not isinstance(task.pred_answer, str):
        return False

    pred_answers = re.findall(
        r"[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?", task.pred_answer
    )
    # if the task.pred_answer is "USD 1.8 is greater than 1.65", the pred_answers is [('1.8', '.8', ''), ('1.65', '.65', '')]
    for pred_ans_matches in pred_answers:
        pred_ans: str = pred_ans_matches[0]
        gold_answer = task.gold_answer.strip()
        gold_ans = (re.findall(
            r"[-+]?(?:\d+\.\d*|\.\d+|\d+)(?:[eE][-+]?\d+)?", task.gold_answer
        ))[0]
        if rounding:
            if abs(float(pred_ans) - float(gold_ans)) < 1:
                return True
        else:
            return (pred_ans == gold_ans)

    return False  # no number was found in the predicted answer


def unordered_list_str_match(
        task: LongResponseQASample, normalize: bool = True, deduplicate: bool = True
) -> bool:
    """The gold answer and predicted answer are assumed to be comma separated lists of strings.
    This metric checks if the unordered list matches.

    Parameters
    ----------
    task : LongResponseQASample
    normalize : bool, optional
        strip and ignore-case, by default True

    Returns
    -------
    bool
        match or not
    """
    if not isinstance(task.gold_answer, str) or not isinstance(task.pred_answer, str):
        return False

    def normalize_list_elements(elements: list[str]) -> list[str]:
        normalized_elements = []
        for element in elements:
            element = element.strip().lower()
            if element.endswith("."):
                element = element[:-1]
            normalized_elements.append(element)
        return normalized_elements

    if task.pred_answer.endswith("."):
        task.pred_answer = task.pred_answer[:-1]

    if normalize:
        gold_ans = task.gold_answer.strip().lower()
        pred_ans = task.pred_answer.strip().lower()
    else:
        gold_ans = task.gold_answer
        pred_ans = task.pred_answer

    gold_ans_elements = gold_ans.split(",")
    pred_ans_elements = pred_ans.split(",")

    if normalize:
        gold_ans_elements = normalize_list_elements(gold_ans_elements)
        pred_ans_elements = normalize_list_elements(pred_ans_elements)

    if deduplicate:
        return set(sorted(gold_ans_elements)) == set(sorted(pred_ans_elements))

    else:
        return (sorted(gold_ans_elements) == sorted(pred_ans_elements))


def contains(task: LongResponseQASample, normalize: bool = True) -> bool:
    if not isinstance(task.gold_answer, str) or not isinstance(task.pred_answer, str):
        return False

    if normalize:
        gold_ans = task.gold_answer.strip().lower()
        pred_ans = task.pred_answer.strip().lower()
    else:
        gold_ans = task.gold_answer
        pred_ans = task.pred_answer

    if pred_ans.endswith("."):
        pred_ans = pred_ans[:-1]

    return (gold_ans in pred_ans)


def response_length(task: LongResponseQASample, normalize: bool = True) -> tuple:
    if not isinstance(task.pred_answer, str):
        return (len(task.gold_answer), 0)

    if normalize:
        gold_ans = task.gold_answer.strip().lower()
        pred_ans = task.pred_answer.strip().lower()
    else:
        gold_ans = task.gold_answer
        pred_ans = task.pred_answer

    if pred_ans.endswith("."):
        pred_ans = pred_ans[:-1]

    return (len(gold_ans), len(pred_ans))


def check_data_type(task: LongResponseQASample, normalize: bool = True) -> bool:
    if (isinstance(task.gold_answer, str) and not isinstance(task.pred_answer, str)) or (
            not isinstance(task.gold_answer, str) and isinstance(task.pred_answer, str)):
        return False

    if (isinstance(task.gold_answer, float) and not isinstance(task.pred_answer, float)) or (
            not isinstance(task.gold_answer, float) and isinstance(task.pred_answer, float)):
        return False

    if (isinstance(task.gold_answer, int) and not isinstance(task.pred_answer, int)) or (
            not isinstance(task.gold_answer, int) and isinstance(task.pred_answer, int)):
        return False

    if (isinstance(task.gold_answer, list) and not isinstance(task.pred_answer, list)) or (
            not isinstance(task.gold_answer, list) and isinstance(task.pred_answer, list)):
        return False

    return True


def code_exec_passed(task: LongResponseQASample, normalize: bool = True) -> bool or None:
    if task.code_exec_status == "Code execution error":
        return False
    elif task.code_exec_status == "":
        return None
    else:
        return True


# Normalize and deduplicate text
def normalize_text(text):
    text = text.lower().strip()
    tokens = text.split()
    deduped = []
    for token in tokens:
        if not deduped or token != deduped[-1]:
            deduped.append(token)
    return ' '.join(deduped)


# Try to parse number + unit
def try_parse_quantity(text):
    ureg = UnitRegistry()
    Q_ = ureg.Quantity
    try:
        match = re.search(r'([\d\.]+)\s*([a-zA-Z]+)', text)
        if match:
            return Q_(text)
    except:
        pass
    return None


def get_all_json_keys(json_obj):
    keys = set()
    if isinstance(json_obj, dict):
        for k, v in json_obj.items():
            keys.add(k)
            keys.update(get_all_json_keys(v))
    elif isinstance(json_obj, list):
        for item in json_obj:
            keys.update(get_all_json_keys(item))
    return keys


def get_all_json_values(json_obj):
    values = []
    if isinstance(json_obj, dict):
        for v in json_obj.values():
            values.extend(get_all_json_values(v))
    elif isinstance(json_obj, list):
        for item in json_obj:
            values.extend(get_all_json_values(item))
    else:
        values.append(json_obj)
    return values


def check_direct_prompt_hallucination(task: LongResponseQASample, semantic_threshold=0.5, tolerance=0.01):
    model = SentenceTransformer('all-MiniLM-L6-v2')

    if task.pred_answer is not None:
        if task.gold_answer in task.pred_answer:
            return False
    else:
        return False

    predicted = normalize_text(task.pred_answer)
    gold = normalize_text(task.gold_answer)

    all_keys = get_all_json_keys(task.api_response)
    all_values = get_all_json_values(task.api_response)

    # Checking if the llm is extracting the answer from json response only but not from the correct place
    if predicted in all_keys or predicted in all_values:
        return False

    # Semantic similarity
    emb_pred = model.encode(predicted, convert_to_tensor=True)
    emb_exp = model.encode(gold, convert_to_tensor=True)
    similarity = util.pytorch_cos_sim(emb_pred, emb_exp).item()
    # keeping the semantic threshold as 50%
    semantically_similar = similarity >= semantic_threshold

    # Try numeric + unit comparison if applicable
    q_pred = try_parse_quantity(predicted)
    q_exp = try_parse_quantity(gold)

    numerically_equivalent = None
    if q_pred is not None and q_exp is not None:
        try:
            q_pred_converted = q_pred.to(q_exp.units)
            diff = abs(q_pred_converted.magnitude - q_exp.magnitude)
            numerically_equivalent = diff <= tolerance * q_exp.magnitude
        except:
            numerically_equivalent = False

    # Decide hallucination
    if numerically_equivalent is not None:
        hallucinated = semantically_similar and not numerically_equivalent
    else:
        hallucinated = not semantically_similar

    return hallucinated


def get_code_keys(model_output: str):
    # Getting the keys used in the code
    code_keys = {match
                 for match in re.findall(
            r"\[\s*['\"]([^'\"]+)['\"]\s*\]|\.get\(\s*['\"]([^'\"]+)['\"]\s*\)",
            model_output
        )
                 for match in match if match}
    return code_keys


def check_hallucinated_keys(task: LongResponseQASample):
    try:
        code_keys = get_code_keys(task.model_output)
        valid_keys = get_all_json_keys(task.api_response)
        hallucinated_keys = code_keys - valid_keys
        return bool(hallucinated_keys)
    except:
        print("No model output")
        return False
    # print(code_keys)



def check_codegen_hallucination(task: LongResponseQASample):
    try:
        printed_literals = re.findall(r'print\((["\'])(.*?)\1\)', task.model_output)
        # If there is any literal string printed, flag it as hallucinated
        if printed_literals:
            return True
    except:
        print("No model output")
        return False

    return False


def llm_as_a_judge(
        task: LongResponseQASample, eval_llm: Any, eval_model_name: str
) -> bool:
    from codegen_scripts.code_generation_for_json_query import (
        EVAL_PROMPT_TEMPLATE,
    )

    eval_prompt = EVAL_PROMPT_TEMPLATE.format(
        gold_answer=task.gold_answer, predicted_answer=task.pred_answer
    )

    llm_as_a_judge_outputs = generate(
        llm=eval_llm, model_name=eval_model_name, prompts=eval_prompt
    )
    if llm_as_a_judge_outputs[0].strip().lower().startswith("true"):
        llm_as_a_judge_output = True
    else:
        llm_as_a_judge_output = False
    return llm_as_a_judge_output


if __name__ == "__main__":
    task = LongResponseQASample(
        api_response={},
        question="",
        gold_answer="AA",
        pred_answer="  AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA, AA,",
    )
    print(unordered_list_str_match(task, deduplicate=True))
