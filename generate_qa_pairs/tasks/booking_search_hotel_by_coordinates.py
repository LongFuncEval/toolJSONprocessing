from typing import Any

from . import evals
from .base import Task
from .data_structures import LongResponseQASample, TaskAttributes


class GetHotelNumReviews(Task):
    EVALUATION_CRITERIA = [evals.accuracy_string]
    TASK_ATTRIBUTES = [TaskAttributes.EXTRACTIVE]

    def get_question(self, hotel_name: str) -> str:
        return f'How many reviews does "{hotel_name}" have?'

    def get_answer(self, api_response: dict[Any, Any], hotel_name: str) -> str:
        for hotel in api_response["data"]["result"]:
            if hotel["hotel_name"].strip().lower() == hotel_name.strip().lower():
                return str(hotel["review_nr"])
        return "None"

    def get_qa_samples(
        self, api_response: dict[Any, Any]
    ) -> list[LongResponseQASample]:
        qa_samples: list[LongResponseQASample] = []
        hotel_names = []
        for hotel in api_response["data"]["result"]:
            hotel_name = hotel["hotel_name"]
            if hotel_name not in hotel_names:
                hotel_names.append(hotel_name)
                question = self.get_question(hotel_name=hotel_name)
                answer = self.get_answer(
                    api_response=api_response, hotel_name=hotel_name
                )

        if answer is not None and answer != "None" and len(qa_samples)<5:
            task = LongResponseQASample(
                api_response=api_response, question=question, gold_answer=answer
            )
            qa_samples.append(task)
        print(qa_samples)
        return qa_samples


class GetHotelRating(Task):
    EVALUATION_CRITERIA = [evals.accuracy_string]
    TASK_ATTRIBUTES = [TaskAttributes.EXTRACTIVE]

    def get_question(self, hotel_name: str) -> str:
        return f'What is the rating of "{hotel_name}"?'

    def get_answer(self, api_response: dict[Any, Any], hotel_name: str) -> str:
        for hotel in api_response["data"]["result"]:
            if hotel["hotel_name"].strip().lower() == hotel_name.strip().lower():
                return str(hotel["review_score"])
        return "None"

    def get_qa_samples(
        self, api_response: dict[Any, Any]
    ) -> list[LongResponseQASample]:
        qa_samples: list[LongResponseQASample] = []
        hotel_names = []
        for hotel in api_response["data"]["result"]:
            hotel_name = hotel["hotel_name"]
            if hotel_name not in hotel_names:
                hotel_names.append(hotel_name)
                question = self.get_question(hotel_name=hotel_name)
                answer = self.get_answer(
                    api_response=api_response, hotel_name=hotel_name
                )

            if answer is not None and answer != "None" and len(qa_samples)<5:
                task = LongResponseQASample(
                    api_response=api_response, question=question, gold_answer=answer
                )
                qa_samples.append(task)
        return qa_samples


class FilterReviewRating(Task):
    EVALUATION_CRITERIA = [evals.unordered_list_str_match]
    TASK_ATTRIBUTES = [TaskAttributes.FILTERING]

    def get_question(self, rating: float) -> str:
        return f'Show all hotels with rating greater than "{rating}". Output a comma separated list of hotel names : rating.'

    def get_answer(self, api_response: dict[Any, Any], rating: float) -> str:
        hotels_list = []
        at_least_one = False
        for hotel in api_response["data"]["result"]:
            try:
                if hotel["review_score"] >= rating:
                    hotels_list.append(
                        hotel["hotel_name"] + " : " + str(hotel["review_score"])
                    )
                    at_least_one = True
            except BaseException:
                continue
        if at_least_one:
            return ", ".join(hotels_list)
        else:
            return "None"

    def get_qa_samples(
        self, api_response: dict[Any, Any]
    ) -> list[LongResponseQASample]:
        qa_samples: list[LongResponseQASample] = []
        ratings_considered = [2.5, 3, 3.5, 4]

        for rating in ratings_considered:
            question = self.get_question(rating=rating)
            answer = self.get_answer(api_response=api_response, rating=rating)

            if answer is not None and answer != "None" and len(qa_samples)<5:
                task = LongResponseQASample(
                    api_response=api_response, question=question, gold_answer=answer
                )
                qa_samples.append(task)
        return qa_samples


class ListHotelParking(Task):
    EVALUATION_CRITERIA = [evals.unordered_list_str_match]
    TASK_ATTRIBUTES = [TaskAttributes.FILTERING]

    def get_question(self) -> str:
        return "Which hotels have free parking? Output a comma separated list of hotel names."

    def get_answer(self, api_response: dict[Any, Any]) -> str:
        hotels_list = []
        at_least_one = False
        for hotel in api_response["data"]["result"]:
            try:
                if hotel["has_free_parking"] == 1:
                    hotels_list.append(hotel["hotel_name"])
                    at_least_one = True
            except BaseException:
                continue
        if at_least_one:
            return ", ".join(hotels_list)
        else:
            return "None"

    def get_qa_samples(
        self, api_response: dict[Any, Any]
    ) -> list[LongResponseQASample]:
        qa_samples: list[LongResponseQASample] = []

        question = self.get_question()
        answer = self.get_answer(api_response=api_response)

        if answer is not None and answer != "None" and len(qa_samples)<5:
            task = LongResponseQASample(
                api_response=api_response, question=question, gold_answer=answer
            )
            qa_samples.append(task)
        return qa_samples


class AvgHotelPrice(Task):
    EVALUATION_CRITERIA = [evals.approx_number_match]
    TASK_ATTRIBUTES = [TaskAttributes.AGGREGATION]

    def get_question(self) -> str:
        return "What is the average price reported for these hotels?"

    def get_answer(self, api_response: dict[Any, Any]) -> str:
        price_list = []
        for hotel in api_response["data"]["result"]:
            price_list.append(hotel["min_total_price"])
        return str(sum(price_list) / len(price_list))

    def get_qa_samples(
        self, api_response: dict[Any, Any]
    ) -> list[LongResponseQASample]:
        qa_samples: list[LongResponseQASample] = []

        question = self.get_question()
        answer = self.get_answer(api_response=api_response)

        if answer is not None and answer != "None" and len(qa_samples)<5:
            task = LongResponseQASample(
                api_response=api_response, question=question, gold_answer=answer
            )
            qa_samples.append(task)
        return qa_samples


class CountExtendedStay(Task):
    EVALUATION_CRITERIA = [evals.approx_number_match]
    TASK_ATTRIBUTES = [TaskAttributes.AGGREGATION]

    def get_question(self) -> str:
        return "How many hotels have extended checkin?"

    def get_answer(self, api_response: dict[Any, Any]) -> str:
        count = 0
        for hotel in api_response["data"]["result"]:
            if hotel["extended"] == 1:
                count += 1
        return str(count)

    def get_qa_samples(
        self, api_response: dict[Any, Any]
    ) -> list[LongResponseQASample]:
        qa_samples: list[LongResponseQASample] = []

        question = self.get_question()
        answer = self.get_answer(api_response=api_response)

        if answer is not None and answer != "None" and len(qa_samples)<5:
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
                "./data/api_responses/booking-com15.p.rapidapi.com_Search_Hotels_By_Coordinates.json"
            )
        )
    )
    )
    for app, endpoint_info in api_responses.items():
        for endpoint, query_info in endpoint_info.items():
            for query, api_response in query_info.items():

                task_obj = GetHotelNumReviews()
                qa_pairs = task_obj.get_qa_samples(api_response)
                if len(qa_pairs) > 0:
                    print("Question: " + qa_pairs[0].question)
                    print("Answer: " + str(qa_pairs[0].gold_answer))
                    print("Number of QA Pairs: " + str(len(qa_pairs)))
                len_qa_pairs.append(len(qa_pairs))

                # task_obj = GetHotelRating()
                # qa_pairs = task_obj.get_qa_samples(api_response)
                # if len(qa_pairs) > 0:
                #     print("Question: " + qa_pairs[0].question)
                #     print("Answer: " + str(qa_pairs[0].gold_answer))
                #     print("Number of QA Pairs: " + str(len(qa_pairs)))
                # len_qa_pairs.append(len(qa_pairs))
                #
                # task_obj = FilterReviewRating()
                # qa_pairs = task_obj.get_qa_samples(api_response)
                # if len(qa_pairs) > 0:
                #     print("Question: " + qa_pairs[0].question)
                #     print("Answer: " + str(qa_pairs[0].gold_answer))
                #     print("Number of QA Pairs: " + str(len(qa_pairs)))
                # len_qa_pairs.append(len(qa_pairs))
                #
                # task_obj = ListHotelParking()
                # qa_pairs = task_obj.get_qa_samples(api_response)
                # if len(qa_pairs) > 0:
                #     print("Question: " + qa_pairs[0].question)
                #     print("Answer: " + str(qa_pairs[0].gold_answer))
                #     print("Number of QA Pairs: " + str(len(qa_pairs)))
                # len_qa_pairs.append(len(qa_pairs))
                #
                # task_obj = AvgHotelPrice()
                # qa_pairs = task_obj.get_qa_samples(api_response)
                # if len(qa_pairs) > 0:
                #     print("Question: " + qa_pairs[0].question)
                #     print("Answer: " + str(qa_pairs[0].gold_answer))
                #     print("Number of QA Pairs: " + str(len(qa_pairs)))
                # len_qa_pairs.append(len(qa_pairs))
                #
                # task_obj = CountExtendedStay()
                # qa_pairs = task_obj.get_qa_samples(api_response)
                # if len(qa_pairs) > 0:
                #     print("Question: " + qa_pairs[0].question)
                #     print("Answer: " + str(qa_pairs[0].gold_answer))
                #     print("Number of QA Pairs: " + str(len(qa_pairs)))
                # len_qa_pairs.append(len(qa_pairs))
