from typing import Any

from . import evals
from .base import Task
from .data_structures import LongResponseQASample, TaskAttributes


class GetInsurancePrice(Task):
    EVALUATION_CRITERIA = [evals.approx_number_match]
    TASK_ATTRIBUTES = [TaskAttributes.EXTRACTIVE]

    def get_question(self, insurance_plan: str) -> str:
        return f'What is the total price for the following travel insurance plan "{insurance_plan}"? Show the currency followed by the amount.'

    def get_answer(self, api_response: dict[Any, Any], insurance_plan: str) -> str:
        if api_response["data"]["travelInsurance"]["options"]["type"] == insurance_plan:
            return str(
                api_response["data"]["travelInsurance"]["options"]["priceBreakdown"][
                    "total"]["currencyCode"]) + " " + str(
                api_response["data"]["travelInsurance"]["options"]["priceBreakdown"][
                    "total"]["units"]
                + api_response["data"]["travelInsurance"]["options"]["priceBreakdown"][
                    "total"]["nanos"] / 1_000_000_000)
        return "None"

    def get_qa_samples(
        self, api_response: dict[Any, Any]
    ) -> list[LongResponseQASample]:
        qa_samples: list[LongResponseQASample] = []
        try:
            insurance_plan = api_response["data"]["travelInsurance"]["options"]["type"]

            question = self.get_question(insurance_plan=insurance_plan)
            answer = self.get_answer(
                api_response=api_response, insurance_plan=insurance_plan
            )

            if answer is not None and answer != "None" and len(qa_samples)<5:
                task = LongResponseQASample(
                    api_response=api_response,
                    question=question,
                    gold_answer=answer,
                )
                qa_samples.append(task)

        except BaseException:
            pass

        return qa_samples


class GetLuggageAllowance(Task):
    EVALUATION_CRITERIA = [evals.accuracy_string]
    TASK_ATTRIBUTES = [TaskAttributes.EXTRACTIVE]

    def get_question(self) -> str:
        return "What is the luggage allowance for this flight and the corresponding maximum weight? Return the type of allowance, weight and unit."

    def get_answer(self, api_response: dict[Any, Any]) -> str:
        if "checkedInBaggage" in api_response["data"]:
            return str(
                api_response["data"]["checkedInBaggage"]["options"][0][
                    "luggageAllowance"
                ]["luggageType"]
                + " "
                + str(
                    api_response["data"]["checkedInBaggage"]["options"][0][
                        "luggageAllowance"
                    ]["maxWeightPerPiece"]
                )
                + api_response["data"]["checkedInBaggage"]["options"][0][
                    "luggageAllowance"
                ]["massUnit"]
            )
        elif "cabinBaggagePerTraveller" in api_response["data"]:
            return str(
                api_response["data"]["cabinBaggagePerTraveller"]["luggageAllowance"][
                    "luggageType"
                ]
                + " "
                + str(
                    api_response["data"]["cabinBaggagePerTraveller"][
                        "luggageAllowance"
                    ]["maxWeightPerPiece"]
                )
                + api_response["data"]["cabinBaggagePerTraveller"]["luggageAllowance"][
                    "massUnit"
                ]
            )
        else:
            return "None"

    def get_qa_samples(
        self, api_response: dict[Any, Any]
    ) -> list[LongResponseQASample]:
        qa_samples: list[LongResponseQASample] = []
        try:
            question = self.get_question()
            answer = self.get_answer(api_response=api_response)

            if answer is not None and answer != "None" and len(qa_samples)<5:
                task = LongResponseQASample(
                    api_response=api_response,
                    question=question,
                    gold_answer=answer,
                )
                qa_samples.append(task)

        except BaseException:
            pass

        return qa_samples


class ListSeatOptions(Task):
    EVALUATION_CRITERIA = [evals.unordered_list_str_match]
    TASK_ATTRIBUTES = [TaskAttributes.FILTERING]

    def get_question(self) -> str:
        return "List the seat options for this flight. Create a comma separated list of row ID followed by column ID without any separator tokens (e.g., no white spaces, dashes, etc.)."

    def get_answer(self, api_response: dict[Any, Any]) -> str:
        seat_ids = []
        for seatMapOption in api_response["data"]["seatMap"]["seatMapOption"]:
            for cabin in seatMapOption["cabins"]:
                for row in cabin["rows"]:
                    for seat in row["seats"]:
                        seat_ids.append(str(row["id"]) + seat["colId"])
        return ", ".join(seat_ids)

    def get_qa_samples(
        self, api_response: dict[Any, Any]
    ) -> list[LongResponseQASample]:
        qa_samples: list[LongResponseQASample] = []
        try:
            question = self.get_question()
            answer = self.get_answer(
                api_response=api_response,
            )

            if answer is not None and answer != "None" and len(qa_samples)<5:
                task = LongResponseQASample(
                    api_response=api_response,
                    question=question,
                    gold_answer=answer,
                )
                qa_samples.append(task)

        except BaseException:
            pass

        return qa_samples


class ListSeatOptionsBySeatType(Task):
    EVALUATION_CRITERIA = [evals.unordered_list_str_match]
    TASK_ATTRIBUTES = [TaskAttributes.FILTERING]

    def get_question(self, seat_type: str) -> str:
        return f'List the seat row IDs of "{seat_type}" seats for this flight. Create a comma separated list of unique row IDs.'

    def get_answer(self, api_response: dict[Any, Any], seat_type: str) -> str:
        seat_ids = []
        for seatMapOption in api_response["data"]["seatMap"]["seatMapOption"]:
            for cabin in seatMapOption["cabins"]:
                seat_type_id = []
                for col in cabin["columns"]:
                    if seat_type in col["description"]:
                        seat_type_id.append(col["id"])
                for row in cabin["rows"]:
                    for seat in row["seats"]:
                        if seat["colId"] in seat_type_id:
                            seat_ids.append(str(row["id"]))
        seat_ids = set(seat_ids)
        return ", ".join(list(seat_ids))

    def get_qa_samples(
        self, api_response: dict[Any, Any]
    ) -> list[LongResponseQASample]:
        qa_samples: list[LongResponseQASample] = []
        try:
            for column in api_response["data"]["seatMap"]["seatMapOption"][0]["cabins"][
                0
            ]["columns"]:
                seat_type = column["description"][0]

                question = self.get_question(seat_type=seat_type)
                answer = self.get_answer(api_response=api_response, seat_type=seat_type)

                if answer is not None and answer != "None" and len(qa_samples)<5:
                    task = LongResponseQASample(
                        api_response=api_response,
                        question=question,
                        gold_answer=answer,
                    )
                    qa_samples.append(task)

        except BaseException:
            pass

        return qa_samples


class CountSeatOptions(Task):
    EVALUATION_CRITERIA = [evals.approx_number_match]
    TASK_ATTRIBUTES = [TaskAttributes.AGGREGATION]

    def get_question(self) -> str:
        return "How many seat options do I have for this flight?"

    def get_answer(self, api_response: dict[Any, Any]) -> str:
        seat_ids = []
        for seatMapOption in api_response["data"]["seatMap"]["seatMapOption"]:
            for cabin in seatMapOption["cabins"]:
                for row in cabin["rows"]:
                    for seat in row["seats"]:
                        seat_ids.append(str(row["id"]) + seat["colId"])
        return str(len(seat_ids))

    def get_qa_samples(
        self, api_response: dict[Any, Any]
    ) -> list[LongResponseQASample]:
        qa_samples: list[LongResponseQASample] = []
        try:
            question = self.get_question()
            answer = self.get_answer(
                api_response=api_response,
            )

            if answer is not None and answer != "None" and len(qa_samples)<5:
                task = LongResponseQASample(
                    api_response=api_response,
                    question=question,
                    gold_answer=answer,
                )
                qa_samples.append(task)

        except BaseException:
            pass

        return qa_samples


class PercentSeatType(Task):
    EVALUATION_CRITERIA = [evals.approx_number_match]
    TASK_ATTRIBUTES = [TaskAttributes.AGGREGATION]

    def get_question(self, seat_type: str) -> str:
        return f'What percentage of seats are "{seat_type}" seats for this flight?'

    def get_answer(self, api_response: dict[Any, Any], seat_type: str) -> str:
        seat_ids = []
        all_seat_ids = []
        for seatMapOption in api_response["data"]["seatMap"]["seatMapOption"]:
            for cabin in seatMapOption["cabins"]:
                seat_type_id = []
                for col in cabin["columns"]:
                    if seat_type in col["description"]:
                        seat_type_id.append(col["id"])
                for row in cabin["rows"]:
                    for seat in row["seats"]:
                        all_seat_ids.append(str(row["id"]) + seat["colId"])
                        if seat["colId"] in seat_type_id:
                            seat_ids.append(str(row["id"]) + seat["colId"])
        return str(100 * len(seat_ids) / len(all_seat_ids))

    def get_qa_samples(
        self, api_response: dict[Any, Any]
    ) -> list[LongResponseQASample]:
        qa_samples: list[LongResponseQASample] = []
        try:
            for column in api_response["data"]["seatMap"]["seatMapOption"][0]["cabins"][
                0
            ]["columns"]:
                seat_type = column["description"][0]

                question = self.get_question(seat_type=seat_type)
                answer = self.get_answer(api_response=api_response, seat_type=seat_type)

                if answer is not None and answer != "None" and len(qa_samples)<5:
                    task = LongResponseQASample(
                        api_response=api_response,
                        question=question,
                        gold_answer=answer,
                    )
                    qa_samples.append(task)

        except BaseException:
            pass

        return qa_samples


if __name__ == "__main__":
    import json
    import os

    len_qa_pairs = []
    api_responses = json.load(
        open(os.path.expanduser("./data/api_responses/booking-com15.p.rapidapi.com_Get_Seat_Map.json"))
    )
    for app, endpoint_info in api_responses.items():
        for endpoint, query_info in endpoint_info.items():
            for query, api_response in query_info.items():
                task_obj = GetInsurancePrice()
                qa_pairs = task_obj.get_qa_samples(api_response)
                if len(qa_pairs) > 0:
                    print("Question: " + qa_pairs[0].question)
                    print("Answer: " + str(qa_pairs[0].gold_answer))
                    print("Number of QA Pairs: " + str(len(qa_pairs)))
                len_qa_pairs.append(len(qa_pairs))
                #
                # task_obj = GetLuggageAllowance()
                # qa_pairs = task_obj.get_qa_samples(api_response)
                # if len(qa_pairs) > 0:
                #     print("Question: " + qa_pairs[0].question)
                #     print("Answer: " + str(qa_pairs[0].gold_answer))
                #     print("Number of QA Pairs: " + str(len(qa_pairs)))
                # len_qa_pairs.append(len(qa_pairs))
                #
                # task_obj = ListSeatOptions()
                # qa_pairs = task_obj.get_qa_samples(api_response)
                # if len(qa_pairs) > 0:
                #     print("Question: " + qa_pairs[0].question)
                #     print("Answer: " + str(qa_pairs[0].gold_answer))
                #     print("Number of QA Pairs: " + str(len(qa_pairs)))
                # len_qa_pairs.append(len(qa_pairs))
                #
                # task_obj = ListSeatOptionsBySeatType()
                # qa_pairs = task_obj.get_qa_samples(api_response)
                # if len(qa_pairs) > 0:
                #     print("Question: " + qa_pairs[0].question)
                #     print("Answer: " + str(qa_pairs[0].gold_answer))
                #     print("Number of QA Pairs: " + str(len(qa_pairs)))
                # len_qa_pairs.append(len(qa_pairs))
                #
                # task_obj = CountSeatOptions()
                # qa_pairs = task_obj.get_qa_samples(api_response)
                # if len(qa_pairs) > 0:
                #     print("Question: " + qa_pairs[0].question)
                #     print("Answer: " + str(qa_pairs[0].gold_answer))
                #     print("Number of QA Pairs: " + str(len(qa_pairs)))
                # len_qa_pairs.append(len(qa_pairs))
                #
                # task_obj = PercentSeatType()
                # qa_pairs = task_obj.get_qa_samples(api_response)
                # if len(qa_pairs) > 0:
                #     print("Question: " + qa_pairs[0].question)
                #     print("Answer: " + str(qa_pairs[0].gold_answer))
                #     print("Number of QA Pairs: " + str(len(qa_pairs)))
                # len_qa_pairs.append(len(qa_pairs))
