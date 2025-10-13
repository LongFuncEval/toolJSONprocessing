from typing import Any

from . import evals
from .base import Task
from .data_structures import LongResponseQASample, TaskAttributes


class GetCleanlinessRating(Task):
    EVALUATION_CRITERIA = [evals.accuracy_string]
    TASK_ATTRIBUTES = [TaskAttributes.EXTRACTIVE]

    def get_question(self, vehicle_id: str) -> str:
        return f'What is the cleanliness rating of "{vehicle_id}"?'

    def get_answer(self, api_response: dict[Any, Any], vehicle_id: str) -> str:
        for car in api_response["data"]["search_results"]:
            if car["vehicle_id"].strip().lower() == vehicle_id.strip().lower():
                return str(car["rating_info"]["cleanliness"])
        return "None"

    def get_qa_samples(
        self, api_response: dict[Any, Any]
    ) -> list[LongResponseQASample]:
        qa_samples: list[LongResponseQASample] = []
        vehicle_ids = []
        for car in api_response["data"]["search_results"]:
            vehicle_id = car["vehicle_id"]
            if vehicle_id not in vehicle_ids:
                vehicle_ids.append(vehicle_id)
                question = self.get_question(vehicle_id=vehicle_id)
                answer = self.get_answer(
                    api_response=api_response, vehicle_id=vehicle_id
                )

        if answer is not None and answer != "None" and len(qa_samples)<10:
            task = LongResponseQASample(
                api_response=api_response, question=question, gold_answer=answer
            )
            qa_samples.append(task)
        print(qa_samples)
        return qa_samples


class GetFuelPolicy(Task):
    EVALUATION_CRITERIA = [evals.accuracy_string]
    TASK_ATTRIBUTES = [TaskAttributes.EXTRACTIVE]

    def get_question(self, vehicle_id: str) -> str:
        return f'What is the fuel policy of "{vehicle_id}"?'

    def get_answer(self, api_response: dict[Any, Any], vehicle_id: str) -> str:
        for car in api_response["data"]["search_results"]:
            if car["vehicle_id"].strip().lower() == vehicle_id.strip().lower():
                return str(car["vehicle_info"]["fuel_policy"])
        return "None"

    def get_qa_samples(
        self, api_response: dict[Any, Any]
    ) -> list[LongResponseQASample]:
        qa_samples: list[LongResponseQASample] = []
        vehicle_ids = []
        for car in api_response["data"]["search_results"]:
            vehicle_id = car["vehicle_id"]
            if vehicle_id not in vehicle_ids:
                vehicle_ids.append(vehicle_id)
                question = self.get_question(vehicle_id=vehicle_id)
                answer = self.get_answer(
                    api_response=api_response, vehicle_id=vehicle_id
                )

        if answer is not None and answer != "None" and len(qa_samples)<10:
            task = LongResponseQASample(
                api_response=api_response, question=question, gold_answer=answer
            )
            qa_samples.append(task)
        return qa_samples


class ListCarInCurrency(Task):
    EVALUATION_CRITERIA = [evals.unordered_list_str_match]
    TASK_ATTRIBUTES = [TaskAttributes.FILTERING]

    def get_question(self, currency: str) -> str:
        return f'Show me cars with prices in "{currency}"? Output a comma separated list of vehicle IDs.'

    def get_answer(self, api_response: dict[Any, Any], currency: str) -> str:
        vehicle_list = []
        at_least_one = False
        for car in api_response["data"]["search_results"]:
            try:
                if car["pricing_info"]["base_currency"] == currency:
                    vehicle_list.append(car["vehicle_id"])
                    at_least_one = True
            except BaseException:
                continue
        if at_least_one:
            return ", ".join(vehicle_list)
        else:
            return "None"

    def get_qa_samples(
        self, api_response: dict[Any, Any]
    ) -> list[LongResponseQASample]:
        qa_samples: list[LongResponseQASample] = []
        currency_list = []
        for car in api_response["data"]["search_results"]:
            currency = car["pricing_info"]["base_currency"]
            if currency not in currency_list:
                currency_list.append(currency)
                question = self.get_question(currency=currency)
                answer = self.get_answer(api_response=api_response, currency=currency)

            if answer is not None and answer != "None" and len(qa_samples)<10:
                task = LongResponseQASample(
                    api_response=api_response, question=question, gold_answer=answer
                )
                qa_samples.append(task)
        return qa_samples


class ListCarFreeCancellation(Task):
    EVALUATION_CRITERIA = [evals.unordered_list_str_match]
    TASK_ATTRIBUTES = [TaskAttributes.FILTERING]

    def get_question(self) -> str:
        return "List all cars with a free cancellation policy? Output a comma separated list of vehicle IDs."

    def get_answer(self, api_response: dict[Any, Any]) -> str:
        vehicle_list = []
        at_least_one = False
        for car in api_response["data"]["search_results"]:
            try:
                if car["vehicle_info"]["free_cancellation"] == 1:
                    vehicle_list.append(car["vehicle_id"])
                    at_least_one = True
            except BaseException:
                continue
        if at_least_one:
            return ", ".join(vehicle_list)
        else:
            return "None"

    def get_qa_samples(
        self, api_response: dict[Any, Any]
    ) -> list[LongResponseQASample]:
        qa_samples: list[LongResponseQASample] = []
        question = self.get_question()
        answer = self.get_answer(api_response=api_response)

        if answer is not None and answer != "None" and len(qa_samples)<10:
            task = LongResponseQASample(
                api_response=api_response, question=question, gold_answer=answer
            )
            qa_samples.append(task)
        return qa_samples


class CountCarsByTransmission(Task):
    EVALUATION_CRITERIA =[evals.approx_number_match]
    TASK_ATTRIBUTES = [TaskAttributes.AGGREGATION]

    def get_question(self, transmission_type: str) -> str:
        return f'How many cars have an "{transmission_type}" transmission?'

    def get_answer(self, api_response: dict[Any, Any], transmission_type: str) -> str:
        car_count = 0
        for car in api_response["data"]["search_results"]:
            if (
                car["vehicle_info"]["transmission"].strip().lower()
                == transmission_type.strip().lower()
            ):
                car_count += 1
        return str(car_count)

    def get_qa_samples(
        self, api_response: dict[Any, Any]
    ) -> list[LongResponseQASample]:
        qa_samples: list[LongResponseQASample] = []
        transmission_type_list = []
        for car in api_response["data"]["search_results"]:
            transmission_type = car["vehicle_info"]["transmission"]
            if transmission_type not in transmission_type_list:
                transmission_type_list.append(transmission_type)
                question = self.get_question(transmission_type=transmission_type)
                answer = self.get_answer(
                    api_response=api_response, transmission_type=transmission_type
                )

        if answer is not None and answer != "None" and len(qa_samples)<10:
            task = LongResponseQASample(
                api_response=api_response, question=question, gold_answer=answer
            )
            qa_samples.append(task)
        return qa_samples


class CheapestCar(Task):
    EVALUATION_CRITERIA = [evals.approx_number_match]
    TASK_ATTRIBUTES = [TaskAttributes.AGGREGATION]

    def get_question(self) -> str:
        return "What is the cheapest base price available?"

    def get_answer(self, api_response: dict[Any, Any]) -> str:
        car_price = []
        for car in api_response["data"]["search_results"]:
            car_price.append(car["pricing_info"]["base_price"])
        return str(min(car_price))

    def get_qa_samples(
        self, api_response: dict[Any, Any]
    ) -> list[LongResponseQASample]:
        qa_samples: list[LongResponseQASample] = []
        question = self.get_question()
        answer = self.get_answer(api_response=api_response)

        if answer is not None and answer != "None" and len(qa_samples)<10:
            task = LongResponseQASample(
                api_response=api_response, question=question, gold_answer=answer
            )
            qa_samples.append(task)
        return qa_samples


if __name__ == "__main__":
    import json
    import os

    len_qa_pairs = []
    api_responses = json.load(
        open(
            os.path.abspath(
                os.path.join(
                    os.path.dirname(__file__),
                    "./data/api_responses/booking-com15.p.rapidapi.com_Search_Car_Rentals.json"
                )
        )
    )
    )
    for app, endpoint_info in api_responses.items():
        for endpoint, query_info in endpoint_info.items():
            for query, api_response in query_info.items():

                task_obj = GetCleanlinessRating()
                qa_pairs = task_obj.get_qa_samples(api_response)
                if len(qa_pairs) > 0:
                    print("Question: " + qa_pairs[0].question)
                    print("Answer: " + str(qa_pairs[0].gold_answer))
                    print("Number of QA Pairs: " + str(len(qa_pairs)))
                len_qa_pairs.append(len(qa_pairs))

                # task_obj = GetFuelPolicy()
                # qa_pairs = task_obj.get_qa_samples(api_response)
                # if len(qa_pairs) > 0:
                #     print("Question: " + qa_pairs[0].question)
                #     print("Answer: " + str(qa_pairs[0].gold_answer))
                #     print("Number of QA Pairs: " + str(len(qa_pairs)))
                # len_qa_pairs.append(len(qa_pairs))
                #
                # task_obj = ListCarInCurrency()
                # qa_pairs = task_obj.get_qa_samples(api_response)
                # if len(qa_pairs) > 0:
                #     print("Question: " + qa_pairs[0].question)
                #     print("Answer: " + str(qa_pairs[0].gold_answer))
                #     print("Number of QA Pairs: " + str(len(qa_pairs)))
                # len_qa_pairs.append(len(qa_pairs))
                #
                # task_obj = ListCarFreeCancellation()
                # qa_pairs = task_obj.get_qa_samples(api_response)
                # if len(qa_pairs) > 0:
                #     print("Question: " + qa_pairs[0].question)
                #     print("Answer: " + str(qa_pairs[0].gold_answer))
                #     print("Number of QA Pairs: " + str(len(qa_pairs)))
                # len_qa_pairs.append(len(qa_pairs))
                #
                # task_obj = CountCarsByTransmission()
                # qa_pairs = task_obj.get_qa_samples(api_response)
                # if len(qa_pairs) > 0:
                #     print("Question: " + qa_pairs[0].question)
                #     print("Answer: " + str(qa_pairs[0].gold_answer))
                #     print("Number of QA Pairs: " + str(len(qa_pairs)))
                # len_qa_pairs.append(len(qa_pairs))
                #
                # task_obj = CheapestCar()
                # qa_pairs = task_obj.get_qa_samples(api_response)
                # if len(qa_pairs) > 0:
                #     print("Question: " + qa_pairs[0].question)
                #     print("Answer: " + str(qa_pairs[0].gold_answer))
                #     print("Number of QA Pairs: " + str(len(qa_pairs)))
                # len_qa_pairs.append(len(qa_pairs))
