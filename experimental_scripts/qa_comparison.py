import os

import pandas as pd
import json
import numpy as np


results_base_dir = os.path.join(os.path.dirname(__file__), "./results/comparisons")
results_base_dir_out = os.path.join(os.path.dirname(__file__), "./results/evaluation")

def compare_across_setups(file_prefix: str, setup1: str, setup2: str, model: str, metric: str, task_type: str):
    file_name_setup1 = f"{file_prefix}_{model}_{setup1}_eval.json"
    file_name_setup2 = f"{file_prefix}_{model}_{setup2}_eval.json"
    print(file_name_setup1, file_name_setup2)
    file_path_1 = os.path.join(results_base_dir_out, file_name_setup1)

    file_path_2 = os.path.join(results_base_dir_out, file_name_setup2)

    with open(file_path_1, 'r') as file1:
        data1 = json.load(file1)
    with open(file_path_2, 'r') as file2:
        data2 = json.load(file2)

    count_TT, count_TF, count_FT, count_FF = 0, 0, 0, 0
    for items1 in data1:
        for items2 in data2:
            if items1['question'] == items2['question'] and items1['task_type'] == task_type and items2['task_type'] == task_type:
                if items1["metrics"][metric] == True and items2["metrics"][metric] == True:
                    count_TT += 1
                elif items1["metrics"][metric] == True and items2["metrics"][metric] == False:
                    count_TF += 1
                elif items1["metrics"][metric] == False and items2["metrics"][metric] == True:
                    count_FT += 1
                elif items1["metrics"][metric] == False and items2["metrics"][metric] == False:
                    count_FF += 1

                break

    return count_TT, count_TF, count_FT, count_FF



if __name__ == "__main__":
    api_endpoints = [
        "booking-com15.p.rapidapi.com_Search_Hotels_By_Coordinates",
        "booking-com15.p.rapidapi.com_Search_Car_Rentals",
        "booking-com15.p.rapidapi.com_Get_Seat_Map",
        "real-time-product-search.p.rapidapi.com_search?",
        "last10k-company-v1.p.rapidapi.com_v1_company_filings",
        "booking-com15.p.rapidapi.com_Get_Room_List_With_Availability"
    ]
    setup_types = [
        # ["direct_prompting", "code_generation"],
        # ["cot_direct_prompting_schema", "cot_code_generation_schema"],
        ["direct_prompting_schema", "code_generation_schema"],
        # ["direct_prompting_schema_cf", "code_generation_schema_cf"]
    ]
    models = [
        # "DeepSeek-V3",
        # "DeepSeek-R1-Distill-Llama-70B",
        # "llama-3-3-70b-instruct",
        # "llama-4-maverick-17b-128e-instruct-fp8",
        "gpt-4o",
        # "mixtral-8x22B-instruct-v0.1",
        # "mistral-large",
        # "granite-3.2-8b-instruct",
    ]
    metrics = [
        "exact_match",
        # "contains",
        # "llm_as_a_judge"
    ]
    task_types = [
        "EXTRACTIVE",
        "AGGREGATION",
        "FILTERING"
    ]
    results_records = []

    for model in models:
        for setup_type in setup_types:
            for metric in metrics:
                for task_type in task_types:
                    flow_values = [0, 0, 0, 0]
                    for api_endpoint in api_endpoints:
                        counts = compare_across_setups(api_endpoint, setup_type[0], setup_type[1], model, metric, task_type)
                        flow_values = np.array(counts) + np.array(flow_values)
                        results_records.append({
                            "Endpoint": api_endpoint,
                            "model_name": model,
                            "metric": metric,
                            "Task type": task_type,
                            "Setup_1": setup_type[0],
                            "Setup_2": setup_type[1],
                            "count_TT": counts[0],
                            "count_TF": counts[1],
                            "count_FT": counts[2],
                            "count_FF": counts[3]
                        })
    df = pd.DataFrame.from_records(results_records)
    df.to_csv(
        os.path.join(os.path.dirname(__file__), f"results/comparisons/comparisons_results_compilation.csv"),
        index=False,
    )
