import os
import re
import json

from generate_qa_pairs.task_list import (
    BookingGetRoomListWithAvailability,
    BookingSearchHotelByCoordinatesTaskList,
    BookingSearchCarRentalsTaskList,
    BookingGetSeatMapTaskList,
    SECFilingsTaskList,
    ProductDetailsShoesTaskList,
)


def deduplicate_question_answers(qa_pairs):
    seen_questions_answers = []
    deduplicated_qa_pairs = []
    for qa_sample in qa_pairs:
        if f"{qa_sample['question']}_{qa_sample['gold_answer']}" not in seen_questions_answers:
            deduplicated_qa_pairs.append(qa_sample)
            seen_questions_answers.append(f"{qa_sample['question']}_{qa_sample['gold_answer']}")
    return deduplicated_qa_pairs


def generate_qa_pairs(task_lists, directory_path: str):

    for task_list in task_lists:
        i = 0
        for app, endpoint_info in task_list.api_response.items():
            all_qa_pairs = []
            for endpoint, query_info in endpoint_info.items():
                try:
                    if "/" in endpoint:
                        schema_path = "schemas/" + app + "_" + endpoint.replace("/", "_") + "_schema.txt"
                    else:
                        schema_path = "schemas/" + app + "_" + endpoint + "_schema.txt"
                    with open("generate_qa_pairs/data/" + schema_path, "w") as file:
                        file.write(task_list.response_json_schema)
                except BaseException:
                    print("Schema does not exist for endpoint: " + app + " " + endpoint)
                for query, api_response in query_info.items():
                    for task in task_list.task_list:
                        task_obj = task()  # type:ignore
                        qa_pairs = task_obj.get_qa_samples(api_response)
                        task_name = re.search(r"\.([A-Za-z_][A-Za-z0-9_]*)'>", str(task))
                        metric = re.search(r"<function (\w+)", str(task_obj.EVALUATION_CRITERIA))

                        for qa in qa_pairs:
                            i += 1
                            all_qa_pairs.append({
                                "uid": task_list.__class__.__name__+"_"+str(i),
                                "question": qa.question,
                                "gold_answer": qa.gold_answer,
                                "api_response_path": "api_responses/" + app + "_" + endpoint + ".json",
                                "api_response_schema": schema_path,
                                "app": app,
                                "endpoint": endpoint,
                                "api_query": query,
                                "task": task_name.group(1),
                                "task_type": task_obj.TASK_ATTRIBUTES[0].value,
                                "predicted_answer": None,
                                "model_output": None,
                                "code_exec_status": None,
                                "metrics": {"exact_match_metric": metric.group(1), "exact_match": None, "contains": None, "llm_as_a_judge": None}
                            })


            all_qa_pairs_unique = deduplicate_question_answers(all_qa_pairs)
            if "/" in endpoint:
                tmp = endpoint.replace("/","_")
                file_name = f"/{app}_{tmp}_qa_pairs"
            else:
                file_name = f"/{app}_{endpoint}_qa_pairs"
            with open(os.path.dirname(__file__) + "/" + directory_path + file_name + ".json", "w") as file:
                json.dump(all_qa_pairs_unique, file)

def generate_public_dataset():
    task_list = [
        BookingGetRoomListWithAvailability(
            os.path.join(
                os.path.dirname(__file__),
                "data/api_responses/booking-com15.p.rapidapi.com_Get_Room_List_With_Availability.json"
            )
        ),
        BookingSearchHotelByCoordinatesTaskList(
            os.path.join(
                os.path.dirname(__file__),
                "data/api_responses/booking-com15.p.rapidapi.com_Search_Hotels_By_Coordinates.json",
            )
        ),
        BookingSearchCarRentalsTaskList(
            os.path.join(
                os.path.dirname(__file__),
                "data/api_responses/booking-com15.p.rapidapi.com_Search_Car_Rentals.json",
            )
        ),
        BookingGetSeatMapTaskList(
            os.path.join(
                os.path.dirname(__file__),
                "data/api_responses/booking-com15.p.rapidapi.com_Get_Seat_Map.json",
            )
        ),
        SECFilingsTaskList(
            os.path.join(
                os.path.dirname(__file__),
                "data/api_responses/last10k-company-v1.p.rapidapi.com_v1_company_filings.json",
            )
        ),
        ProductDetailsShoesTaskList(
            os.path.join(
                os.path.dirname(__file__),
                "data/api_responses/real-time-product-search.p.rapidapi.com_search?.json",
            )
        )
    ]
    generate_qa_pairs(task_list, "data/qa_pairs")


if __name__ == "__main__":
    generate_public_dataset()