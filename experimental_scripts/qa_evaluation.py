import os
import json
from multiprocessing import Pool

from generate_qa_pairs.tasks import evals
from generate_qa_pairs.tasks.data_structures import LongResponseQASample
from generate_qa_pairs.tasks.utils import convert_dict_to_list_of_objects, get_lm

try:
    from dotenv import load_dotenv
    load_dotenv()

except ImportError:
    pass

def calculate_exact_match(task: LongResponseQASample,normalize: bool = True,rounding: bool = True,deduplicate: bool = True) -> bool :
    if 'accuracy_string' in task.metrics:
        return evals.accuracy_string(task, normalize)
    elif 'approx_number_match' in task.metrics:
        return evals.approx_number_match(task, rounding)
    elif 'unordered_list_str_match' in task.metrics:
        return evals.unordered_list_str_match(task, normalize, deduplicate)
    else:
        return None

def evaluate_sample(args):
    i, sample, llm_as_a_judge_model = args
    get_llm_as_a_judge = get_lm(llm_as_a_judge_model, parameters={
        "max_new_tokens": 1000,
        "min_new_tokens": 1,
        "top_p": 0.1,
        "temperature": 0.0,
        "random_seed": 1,
        "decoding_method": "greedy",
        "stop_sequences": [],
    })
    result = evals.llm_as_a_judge(sample, get_llm_as_a_judge, llm_as_a_judge_model)
    return i, result



if __name__=="__main__":
    hallucination_test = True
    results_base_dir = os.path.join(os.path.dirname(__file__), "./results/")
    results_base_dir_pred = results_base_dir + "predictions"

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
    task_lists = [  # sorted by size
        "booking-com15.p.rapidapi.com_Search_Hotels_By_Coordinates",
        "booking-com15.p.rapidapi.com_Search_Car_Rentals",
        "booking-com15.p.rapidapi.com_Get_Seat_Map",
        "real-time-product-search.p.rapidapi.com_search?",
        "last10k-company-v1.p.rapidapi.com_v1_company_filings",
        "booking-com15.p.rapidapi.com_Get_Room_List_With_Availability",
    ]
    model_names = [
        "meta-llama/llama-4-maverick-17b-128e-instruct-fp8",
        "deepseek-ai/DeepSeek-V3",
        "deepseek-ai/DeepSeek-R1-Distill-Llama-70B",
        "mistralai/mixtral-8x22B-instruct-v0.1",
        "Qwen/Qwen3-Coder-480B-A35B-Instruct-FP8",
        "Qwen/Qwen3-235B-A22B-Instruct-2507",
        "Qwen/Qwen3-8B",
        "deepseek-ai/deepseek-r1",
        "mistralai/mistral-large",
        "meta-llama/llama-3-3-70b-instruct",
        "Azure/gpt-4o",
        "mistralai/Devstral-Small-2507",
        "GCP/claude-4-sonnet",
        "ibm-granite/granite-3.3-8b-instruct",
        "openai/gpt-oss-20b",
        "openai/gpt-oss-120b",
        "meta-llama/llama-3-405b-instruct",
    ]
    wLLM = False
    if wLLM:
        llm_as_a_judge_model = "meta-llama/llama-3-3-70b-instruct"
        get_llm_as_a_judge = get_lm(llm_as_a_judge_model, parameters={
            "max_new_tokens": 1000,
            "min_new_tokens": 1,
            "top_p": 0.1,
            "temperature": 0.0,
            "random_seed": 1,
            "decoding_method": "greedy",
            "stop_sequences": [],
        })
    num_processes = 50

    for model_name in model_names:
        for setup_type in setup_types:
            for task in task_lists:

                filename = task + "_" + model_name.split('/')[1] + "_" + setup_type + "_predictions.json"
                if filename.endswith(".json"):
                    if os.path.exists(os.path.join(results_base_dir + "evaluation",
                                                   filename.replace("_predictions.json", "") + "_eval.json")):
                        print("SKIPPED: " + filename)
                        continue
                    predictions_filepath = os.path.join(results_base_dir_pred, filename)
                    try:
                        with open(predictions_filepath, 'r') as f:
                            qa_samples_pred_dict = json.load(f)

                        qa_samples_obj = convert_dict_to_list_of_objects(qa_samples_pred_dict)
                    except BaseException:
                        print("FAILED: " + filename)
                        continue

                    for i in range(0, len(qa_samples_pred_dict)):
                        qa_samples_pred_dict[i]["metrics"]["exact_match"] = calculate_exact_match(qa_samples_obj[i])
                        qa_samples_pred_dict[i]["metrics"]["contains"] = evals.contains(qa_samples_obj[i])
                        if hallucination_test:
                            if 'direct_prompting' in filename:
                                qa_samples_pred_dict[i]["metrics"]["hallucination"] = evals.check_direct_prompt_hallucination(qa_samples_obj[i])
                            if 'code_generation' in filename:
                                qa_samples_pred_dict[i]["metrics"]["hallucination"] = evals.check_hallucinated_keys(qa_samples_obj[i]) or evals.check_codegen_hallucination(qa_samples_obj[i])
                        if num_processes == 0 and wLLM:
                            qa_samples_pred_dict[i]["metrics"]["llm_as_a_judge"] = evals.llm_as_a_judge(qa_samples_obj[i], get_llm_as_a_judge, llm_as_a_judge_model)
                    if wLLM:
                        if num_processes > 0:
                            with Pool(processes=num_processes) as pool:
                                args = [(i, qa_samples_obj[i], llm_as_a_judge_model) for i in
                                     range(len(qa_samples_obj))]
                                results = pool.map(
                                    evaluate_sample,
                                    args
                                )
                            for i, result in results:
                                qa_samples_pred_dict[i]["metrics"]["llm_as_a_judge"] = result
                    if wLLM:
                        suffix = "eval.json"
                    else:
                        suffix = "eval_woLLM.json"
                    with open(results_base_dir + "evaluation/" + filename.replace("predictions.json", "") + suffix, 'w') as f:
                        json.dump(qa_samples_pred_dict, f, indent=2)

