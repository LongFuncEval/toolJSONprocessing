import os
import json

from generate_qa_pairs.tasks.utils import generate, get_lm

try:
    from dotenv import load_dotenv
    load_dotenv()
    print(os.getenv("LLM_PROVIDER"))
except ImportError:
    pass


TASK_ATTRIBUTE_CLASSIFIER_PROMPT = """
You will be given a natural language query and are tasked with classifying it into one of the following three categories:
- Extractive: returns a value in the JSON given a key
- Filtering: returns multiple entries corresponding to filtering criteria
- Aggregation: combines multiple entries by performing an aggregation operation

Return your final answer after "Final answer, category: "

Does the following natural language query belong to the "Extractive", "Filtering" or "Aggregation" category?
Natural language query: "{nl_query}"
Schema: "{schema}"
Final answer, category: 
"""

# def classify_with_llm(nl_query: str, schema: str, model_name: str, llm_parameters: dict) -> dict:
def classify_with_llm(dataset: list[dict], model_name: str, llm_parameters: dict) -> list[dict]:
    prompts = [
        TASK_ATTRIBUTE_CLASSIFIER_PROMPT.format(nl_query=sample['nl_query'], schema=sample['schema']) for sample in dataset
    ]
    llm = get_lm(model_name, parameters=llm_parameters)
    generations = generate(
        llm=llm, model_name=model_name, prompts=prompts, temperature=0
    )
    for i in range(len(generations)):
        dataset[i]["model_output"] = generations[i]
    return dataset

def output_parser(dataset: list[dict], model_name: str) -> list[dict]:
    for sample in dataset:
        try:
            # TODO: optimize and generalize to other models
            if "DeepSeek-V3" in model_name:
                model_response = sample["model_output"].lower()
            elif "llama-3-3-70b-instruct" in model_name:
                if "Reasoning" in sample["model_output"]:
                    model_response = sample["model_output"].split("Reasoning")[0].lower()
                elif "#" in sample["model_output"]:
                    model_response = sample["model_output"].split("#")[0].lower()
                elif "\n" in sample["model_output"]:
                    model_response = sample["model_output"].split("\n")[0].lower()
            elif "gpt" in model_name:
                if "category:" in sample["model_output"]:
                    model_response = sample["model_output"].split("category:")[1].lower()

            if "extractive" in model_response:
                sample["predicted_class"] = "extractive"
            elif "filtering" in model_response:
                sample["predicted_class"] = "filtering"
            elif "aggregation" in model_response:
                sample["predicted_class"] = "aggregation"
        except BaseException:
            sample["predicted_class"] = "parsing error"
    return dataset

if __name__ == "__main__":
    call_llm = False
    run_parser = False
    model_names = [
        "deepseek-ai/DeepSeek-V3",
        "meta-llama/llama-3-3-70b-instruct",
        "Azure/gpt-4o",
        "meta-llama/llama-4-maverick-17b-128e-instruct-fp8",
        "openai/gpt-oss-120b",
        "Qwen/Qwen3-235B-A22B-Instruct-2507",
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

    task_lists = [ #sorted by size
        "booking-com15.p.rapidapi.com_Search_Hotels_By_Coordinates",
        "booking-com15.p.rapidapi.com_Search_Car_Rentals",
        "booking-com15.p.rapidapi.com_Get_Seat_Map",
        "real-time-product-search.p.rapidapi.com_search?",
        "last10k-company-v1.p.rapidapi.com_v1_company_filings",
        "booking-com15.p.rapidapi.com_Get_Room_List_With_Availability",
    ]

    if call_llm:
        dataset = []
        for task in task_lists:
            task_file = "../generate_qa_pairs/data/qa_pairs/" + task + "_qa_pairs.json"
            with open(task_file, 'r') as file:
                qa_pairs = json.load(file)
            for sample in qa_pairs:
                with open("../generate_qa_pairs/data/" + sample['api_response_schema'], 'r', encoding='utf-8') as f:
                    schema = f.read()
                dataset.append({"nl_query": sample['question'],
                                "uid": sample['uid'],
                                "schema": schema,
                                "category": sample['task_type'],
                                "predicted_class": "",
                                "model_output": ""
                                })

    for model_name in model_names:
        model = model_name.split("/")[1]
        if call_llm:
            # Generate model predictions
            dataset = classify_with_llm(dataset=dataset, model_name=model_name, llm_parameters=llm_parameters)
            with open(os.path.dirname(__file__) + f"/results/classifier/{model}_classifier_predictions.json",
                      "w") as file:
                json.dump(dataset, file)
        else:
            with open(os.path.dirname(__file__) + f"/results/classifier/{model}_classifier_predictions.json", 'r',
                      encoding='utf-8') as file:
                dataset = json.load(file)

        # Parse model output
        if run_parser:
            dataset = output_parser(dataset=dataset,model_name=model_name)
            # for sample in dataset:
            #     output_dict = classify_with_llm(sample['nl_query'], sample['schema'], model_name, llm_parameters)
            #     sample["predicted_class"] = output_dict["prediction"]
            #     sample["model_output"] = output_dict["model_output"]
            with open(os.path.dirname(__file__) + f"/results/classifier/{model}_classifier_predictions.json",
                      "w") as file:
                json.dump(dataset, file)

        # evaluation (compare prediction to ground truth)
        total_acc = 0
        total_extr = 0
        total_filt = 0
        total_aggr = 0
        for sample in dataset:
            if sample["predicted_class"].lower() == sample['category'].lower():
                total_acc += 1
                if sample["category"] == "EXTRACTIVE":
                    total_extr += 1
                elif sample["category"] == "FILTERING":
                    total_filt += 1
                elif sample["category"] == "AGGREGATION":
                    total_aggr += 1
        print(f"{model}: {total_extr = }")
        print(f"{model}: {total_filt = }")
        print(f"{model}: {total_aggr = }")
        print(f"{model}: {total_acc = } / {str(len(dataset))}")