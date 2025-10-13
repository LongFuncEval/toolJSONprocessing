import json
import os
import pandas as pd


def aggregate_metric(criterion: str, data: list[dict]) -> dict:
    agg_metric = {
        f'exact_match_accuracy_{criterion}': 0,
        f'contains_accuracy_{criterion}': 0,
        f'llm_as_a_judge_accuracy_{criterion}': 0,
        f'code_exec_status_passed_{criterion}': 0
    }
    sample_count = 0
    for item in data:
        if 'task' in item:
            if item['task_type'] == criterion or item['task'] == criterion:
                sample_count += 1

                if item['metrics']['exact_match'] == True:
                    agg_metric[f'exact_match_accuracy_{criterion}'] += 1

                if item['metrics']['contains'] == True or item['metrics']['exact_match'] == True:
                    agg_metric[f'contains_accuracy_{criterion}'] += 1

                if item['metrics']['llm_as_a_judge'] == True:
                    agg_metric[f'llm_as_a_judge_accuracy_{criterion}'] += 1

                if item['code_exec_status'] != "Code execution error":
                    agg_metric[f'code_exec_status_passed_{criterion}'] += 1

    agg_metric['criterion'] = criterion
    agg_metric[f'total_samples_{criterion}'] = sample_count
    return agg_metric


def aggregate_endpoint(criteria: list[str], data: list[dict]) -> dict:
    records = {}

    count_context_exceeded = [1 if result['predicted_answer'] == "context length exceeded" else 0 for result in data]

    records.update({
        "task": task,
        "model": model_name,
        "setup_type": setup_type,
        "count_context_exceeded": sum(count_context_exceeded),
        "total_samples": 0,
        "total_exact_match": 0,
        "avg_exact_match": 0,
        "total_contains": 0,
        "avg_contains": 0,
        "total_llm_as_a_judge": 0,
        "avg_llm_as_a_judge": 0,
    })
    for criterion in criteria:
        aggregate_records = aggregate_metric(criterion, data)
        records['total_samples'] += aggregate_records[f'total_samples_{aggregate_records["criterion"]}']
        records['total_exact_match'] += aggregate_records[f'exact_match_accuracy_{aggregate_records["criterion"]}']
        records['total_contains'] += aggregate_records[f'contains_accuracy_{aggregate_records["criterion"]}']
        records['total_llm_as_a_judge'] += aggregate_records[
            f'llm_as_a_judge_accuracy_{aggregate_records["criterion"]}']
        records.update(
            {
                f"{aggregate_records['criterion']}_total_samples": aggregate_records[
                    f'total_samples_{aggregate_records["criterion"]}'],
                f"total_{aggregate_records['criterion']}_exact_match_accuracy": aggregate_records[
                    f'exact_match_accuracy_{aggregate_records["criterion"]}'],
                f"avg_{aggregate_records['criterion']}_exact_match_accuracy": aggregate_records[
                    f'exact_match_accuracy_{aggregate_records["criterion"]}'] / aggregate_records[f'total_samples_{aggregate_records["criterion"]}'],
                f"total_{aggregate_records['criterion']}_contains_accuracy": aggregate_records[
                    f'contains_accuracy_{aggregate_records["criterion"]}'],
                f"avg_{aggregate_records['criterion']}_contains_accuracy": aggregate_records[
                    f'contains_accuracy_{aggregate_records["criterion"]}'] / aggregate_records[f'total_samples_{aggregate_records["criterion"]}'],
                f"total_{aggregate_records['criterion']}_llm_as_a_judge_accuracy": aggregate_records[
                    f'llm_as_a_judge_accuracy_{aggregate_records["criterion"]}'],
                f"avg_{aggregate_records['criterion']}_llm_as_a_judge_accuracy": aggregate_records[
                    f'llm_as_a_judge_accuracy_{aggregate_records["criterion"]}'] / aggregate_records[f'total_samples_{aggregate_records["criterion"]}'],
                f"total_{aggregate_records['criterion']}_code_exec_status_accuracy": aggregate_records[
                    f'code_exec_status_passed_{aggregate_records["criterion"]}'],
                f"avg_{aggregate_records['criterion']}_code_exec_status_accuracy": aggregate_records[
                    f'code_exec_status_passed_{aggregate_records["criterion"]}'] / aggregate_records[f'total_samples_{aggregate_records["criterion"]}']
            }
        )
    records['avg_exact_match'] = records['total_exact_match'] / records['total_samples']
    records['avg_contains'] = records['total_contains'] / records['total_samples']
    records['avg_llm_as_a_judge'] = records['total_llm_as_a_judge'] / records['total_samples']
    return records


if __name__ == "__main__":
    # Build the relative path to the JSON file
    results_base_dir = os.path.join(os.path.dirname(__file__), "./results/")
    results_base_dir_evals = results_base_dir + "evaluation"

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
    models = [ # Sort by size
        "granite-3.3-8b-instruct", # 8B
        "llama-4-maverick-17b-128e-instruct-fp8", # 17B
        "gpt-oss-20b", # 20B
        "Devstral-Small-2507", # 24B
        "DeepSeek-V3", # 37B
        "mixtral-8x22B-instruct-v0.1", # 39.1B
        "llama-3-3-70b-instruct", # 70B
        "DeepSeek-R1-Distill-Llama-70B", # 70B
        "gpt-oss-120b", # 120B
        "mistral-large", # 123B
        "Qwen3-235B-A22B-Instruct-2507", # 235B
        "Llama-3-405B-Instruct", # 405B
        "Qwen3-Coder-480B-A35B-Instruct-FP8", # 480B
        "gpt-4o",
        "claude-4-sonnet",
    ]

    all_results_per_endpoint = []
    all_results_per_model_setup = []
    task_types = ['EXTRACTIVE', 'FILTERING', 'AGGREGATION']
    metrics = ['exact_match', 'contains', 'llm_as_a_judge', 'code_exec_status']

    for model_name in models:
        for setup_type in setup_types:
            tmp_results_per_task = []
            for task in task_lists:
                file_name = f"{task}_{model_name}_{setup_type}_eval.json"
                json_path = os.path.join(results_base_dir_evals, file_name)
                try:
                    with open(json_path, 'r') as file:
                        data = json.load(file)
                    none_count = 0
                    for i in range(len(data) -1, -1, -1):
                        if data[i]['predicted_answer'] is None and data[i]['model_output'] is None:
                            data.pop(i)
                            none_count += 1
                except BaseException as e:
                    print(e)
                    print("FAILED:" + file_name)
                    continue

                criteria = task_types
                records = aggregate_endpoint(criteria, data)
                tmp_results_per_task.append(records)
                all_results_per_endpoint.append(records)
            grouped_records = {}
            grouped_records.update({
                "model": model_name,
                "setup_type": setup_type,
                "total_samples": 0,
            })
            for metric in metrics:
                grouped_records.update({
                    f'total_{metric}_accuracy': 0,
                    f'avg_{metric}_accuracy': 0
                })
            for task_type in task_types:
                grouped_records.update({
                    f'{task_type}_total_samples': 0
                })
                for metric in metrics:
                    grouped_records.update({
                        f'total_{task_type}_{metric}_accuracy': 0
                    })
            for row in tmp_results_per_task:
                for task_type in task_types:
                    grouped_records['total_samples'] += row[f'{task_type}_total_samples']
                    grouped_records[f'{task_type}_total_samples'] += row[f'{task_type}_total_samples']
                for metric in metrics:
                    for task_type in task_types:
                        grouped_records[f'total_{metric}_accuracy'] += row[f'total_{task_type}_{metric}_accuracy']
                        grouped_records[f'total_{task_type}_{metric}_accuracy'] += row[f'total_{task_type}_{metric}_accuracy']
                        grouped_records.update({
                            f'avg_{task_type}_{metric}_accuracy': grouped_records[
                                                                      f'total_{task_type}_{metric}_accuracy'] /
                                                                  grouped_records[f'{task_type}_total_samples']
                        })

                    grouped_records[f'avg_{metric}_accuracy'] = grouped_records[f'total_{metric}_accuracy'] / grouped_records['total_samples']


            all_results_per_model_setup.append(grouped_records)
    df1 = pd.DataFrame.from_records(all_results_per_endpoint)
    df2 = pd.DataFrame.from_records(all_results_per_model_setup)
    with pd.ExcelWriter(os.path.join(os.path.dirname(__file__),
                                     "results/metric_aggregation/all_results.xlsx"), engine='openpyxl') as writer:
        df1.to_excel(writer, sheet_name='per_endpoint', index=False)
        df2.to_excel(writer, sheet_name='per_model_setup', index=False)
