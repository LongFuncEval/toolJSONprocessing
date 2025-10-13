import json
from datetime import datetime
from typing import Any

from . import evals
from .base import Task
from .data_structures import LongResponseQASample, TaskAttributes

"""
===========================================QUESTION 1============================================
"""


class GetFormType(Task):
    """
    Get the form type of the filing of a given accession number
    """

    EVALUATION_CRITERIA = [evals.accuracy_string]
    TASK_ATTRIBUTES = [TaskAttributes.EXTRACTIVE]

    # example answer: "8-K"
    def get_answer(self, acc_num: str, api_response: dict[Any, Any]) -> str:

        for forms in api_response["data"]["attributes"]["result"]:
            if forms["accessionNumber"] == acc_num:
                return str(forms["formType"])

        return "None"

    # example question: "What is form type of the filing with accession number 0001193125-11-273826?"
    def get_question(self, acc_num: str) -> str:
        return f"What is form type of the filing with accession number {acc_num}?"

    def get_qa_samples(
        self, api_response: dict[Any, Any]
    ) -> list[LongResponseQASample]:

        qa_samples: list[LongResponseQASample] = []
        for filings in api_response["data"]["attributes"]["result"]:
            acc_num = filings["accessionNumber"]
            question = self.get_question(acc_num=acc_num)
            answer = self.get_answer(acc_num=acc_num, api_response=api_response)

            if answer is not None and answer != "None" and len(qa_samples)<2:
                task = LongResponseQASample(
                    api_response=api_response, question=question, gold_answer=answer
                )
                qa_samples.append(task)

        return qa_samples


"""
===========================================QUESTION 2============================================
"""


class GetFilingDate(Task):
    """
    Get the filing date of a form of a particular accession number
    """

    EVALUATION_CRITERIA = [evals.accuracy_string]
    TASK_ATTRIBUTES = [TaskAttributes.EXTRACTIVE]

    # example answer: "2011-10-26"
    def get_answer(self, acc_num: str, api_response: dict[Any, Any]) -> str:

        for forms in api_response["data"]["attributes"]["result"]:
            if forms["accessionNumber"] == acc_num:
                date_obj = datetime.strptime(forms["filingDate"], "%Y-%m-%dT%H:%M:%S")
                date = date_obj.date()
                return str(date)

        return "None"

    # example question: "What is the filing date of a form with accession number 0001193125-11-282113?"
    def get_question(self, acc_num: str) -> str:
        return f"What is the filing date of a form with accession number {acc_num}? Don't include time."

    def get_qa_samples(
        self, api_response: dict[Any, Any]
    ) -> list[LongResponseQASample]:

        qa_samples: list[LongResponseQASample] = []
        for filings in api_response["data"]["attributes"]["result"]:
            acc_num = filings["accessionNumber"]
            question = self.get_question(acc_num=acc_num)
            answer = self.get_answer(acc_num=acc_num, api_response=api_response)

            if answer is not None and answer != "None" and len(qa_samples)<2:
                task = LongResponseQASample(
                    api_response=api_response, question=question, gold_answer=answer
                )
                qa_samples.append(task)

        return qa_samples


"""
===========================================QUESTION 3============================================
"""


class GetFilingName(Task):
    """
    Get the name of the filing
    """

    EVALUATION_CRITERIA = [evals.accuracy_string]
    TASK_ATTRIBUTES = [TaskAttributes.EXTRACTIVE]

    # example answer: "APRIL 2021 DIVIDEND Report"
    def get_answer(self, api_response: dict[Any, Any], id: str) -> str:

        for forms in api_response["data"]["attributes"]["result"]:
            if forms["accessionNumber"] == id:
                return str(forms["name"])

        return "None"

    # example question: "Find the name of the filing whose accession number is 0000080424-21-000059"
    def get_question(self, id: str) -> str:
        return f"Find the name of the filing whose accession number is {id}."

    def get_qa_samples(
        self, api_response: dict[Any, Any]
    ) -> list[LongResponseQASample]:

        qa_samples: list[LongResponseQASample] = []

        for filings in api_response["data"]["attributes"]["result"]:
            id = filings["accessionNumber"]
            question = self.get_question(id=id)
            answer = self.get_answer(api_response=api_response, id=id)

            if answer is not None and answer != "None" and len(qa_samples)<2:
                task = LongResponseQASample(
                    api_response=api_response, question=question, gold_answer=answer
                )
                qa_samples.append(task)

        return qa_samples


"""
===========================================QUESTION 4============================================
"""


class FilingsInAYear(Task):
    """
    Get the number of filings done in a specific year
    """

    EVALUATION_CRITERIA = [evals.approx_number_match]
    TASK_ATTRIBUTES = [TaskAttributes.AGGREGATION]

    # example answer: "80"
    def get_answer(self, api_response: dict[Any, Any], year: int) -> str:

        reports = 0
        for filings in api_response["data"]["attributes"]["result"]:
            date = datetime.strptime(filings["filingDate"], "%Y-%m-%dT%H:%M:%S")
            filing_year = date.year
            if filing_year == year:
                reports += 1

        return str(reports)

    # example question: "How many SEC filings are done in  year 2021 ?"
    def get_question(self, year: int) -> str:
        return f"How many SEC filings are done in year {year}?"

    def get_qa_samples(
        self, api_response: dict[Any, Any]
    ) -> list[LongResponseQASample]:

        qa_samples: list[LongResponseQASample] = []

        for year in range(2012, 2026):
            question = self.get_question(year=year)
            answer = self.get_answer(api_response=api_response, year=year)

            if answer is not None and answer != "None" and len(qa_samples)<2:
                task = LongResponseQASample(
                    api_response=api_response, question=question, gold_answer=answer
                )
                qa_samples.append(task)

        return qa_samples


"""
===========================================QUESTION 5============================================
"""


class FilingsOfSpecificFormType(Task):
    """
    Get the number of filings of specified form type
    """

    EVALUATION_CRITERIA = [evals.approx_number_match]
    TASK_ATTRIBUTES = [TaskAttributes.AGGREGATION]

    # example answer: "70"
    def get_answer(self, api_response: dict[Any, Any], form_type: str) -> str:

        forms = 0
        for filings in api_response["data"]["attributes"]["result"]:
            if "formType" in filings and filings["formType"] == form_type:
                forms += 1

        return str(forms)

    # example question: "Provide the number of filings which belong to form type :424B2."
    def get_question(self, form_type: str) -> str:
        return f"Provide the number of filings which belong to form type {form_type}."

    def get_qa_samples(
        self, api_response: dict[Any, Any]
    ) -> list[LongResponseQASample]:

        qa_samples: list[LongResponseQASample] = []

        form_types = []
        for filings in api_response["data"]["attributes"]["result"]:
            if "formType" in filings:
                form_types.append(filings["formType"])

        form_types = list(set(form_types))
        form_types.sort()
        for form in form_types:
            question = self.get_question(form_type=form)
            answer = self.get_answer(api_response=api_response, form_type=form)

            if answer is not None and answer != "None" and len(qa_samples)<2:
                task = LongResponseQASample(
                    api_response=api_response, question=question, gold_answer=answer
                )
                qa_samples.append(task)

        return qa_samples


"""
===========================================QUESTION 6============================================
"""


class FilingsOfSpecificName(Task):
    """
    Get the number of filings of specified name
    """

    EVALUATION_CRITERIA = [evals.approx_number_match]
    TASK_ATTRIBUTES = [TaskAttributes.AGGREGATION]

    # example answer: "70"
    def get_answer(self, api_response: dict[Any, Any], name: str) -> str:

        forms = 0
        for filings in api_response["data"]["attributes"]["result"]:
            if "name" in filings and filings["name"] == name:
                forms += 1

        return str(forms)

    # example question: "Provide the number of filings which has the name FWP Report ."
    def get_question(self, name: str) -> str:
        return f"Provide the number of filings which has the name {name}."

    def get_qa_samples(
        self, api_response: dict[Any, Any]
    ) -> list[LongResponseQASample]:

        qa_samples: list[LongResponseQASample] = []

        form_names = []
        for filings in api_response["data"]["attributes"]["result"]:
            if "name" in filings:
                form_names.append(filings["name"])

        form_names = list(set(form_names))
        form_names.sort()
        for name in form_names:
            question = self.get_question(name=name)
            answer = self.get_answer(api_response=api_response, name=name)

            if answer is not None and answer != "None" and len(qa_samples)<2:
                task = LongResponseQASample(
                    api_response=api_response, question=question, gold_answer=answer
                )
                qa_samples.append(task)

        return qa_samples


"""
===========================================QUESTION 7============================================
"""


class FilingsWithNameAndType(Task):
    """
    Get the number of filings of specific name and type
    """

    EVALUATION_CRITERIA = [evals.approx_number_match]
    TASK_ATTRIBUTES = [TaskAttributes.AGGREGATION]

    # example answer: "8"
    def get_answer(self, api_response: dict[Any, Any], name: str, form: str) -> str:

        reports = 0
        for filings in api_response["data"]["attributes"]["result"]:
            if "name" in filings and filings["name"] == name:
                if "formType" in filings and filings["formType"] == form:
                    reports += 1

        return str(reports)

    # example question: "How many SEC filings are done having name P&G HOLDING FRANCE GPSIECP 2024 Report and form type 11-K ?"
    def get_question(self, name: str, form: str) -> str:
        return f"How many SEC filings are done having name {name} and form type {form}?"

    def get_qa_samples(
        self, api_response: dict[Any, Any]
    ) -> list[LongResponseQASample]:

        qa_samples: list[LongResponseQASample] = []

        form_names = []
        for filings in api_response["data"]["attributes"]["result"]:
            if "name" in filings:
                form_names.append(filings["name"])

        form_names = list(set(form_names))
        form_names.sort()

        form_types = []
        for filings in api_response["data"]["attributes"]["result"]:
            if "formType" in filings:
                form_types.append(filings["formType"])

        form_types = list(set(form_types))
        form_types.sort()

        for name in form_names:
            for form in form_types:
                question = self.get_question(form=form, name=name)
                answer = self.get_answer(
                    api_response=api_response, form=form, name=name
                )

                if answer is not None and answer != "None" and len(qa_samples)<2:
                    task = LongResponseQASample(
                        api_response=api_response, question=question, gold_answer=answer
                    )
                    qa_samples.append(task)

        return qa_samples


"""
===========================================QUESTION 8============================================
"""


class FilingsAccordingToFilingDateAndPeriod(Task):
    """
    Get the number of filings where difference between period and filing is within certain number of days
    """

    EVALUATION_CRITERIA = [evals.approx_number_match]
    TASK_ATTRIBUTES = [TaskAttributes.AGGREGATION]

    # example answer: "7"
    def get_answer(
        self, api_response: dict[Any, Any], no_of_days1: int, no_of_days2: int
    ) -> str:

        date = 0
        for filings in api_response["data"]["attributes"]["result"]:
            if "period" in filings and "filingDate" in filings:
                filing_date = datetime.strptime(
                    filings["filingDate"], "%Y-%m-%dT%H:%M:%S"
                )
                period = datetime.strptime(filings["period"], "%Y-%m-%dT%H:%M:%S")
                if (abs(filing_date - period)).days >= no_of_days1 and (
                    abs(filing_date - period)
                ).days <= no_of_days2:
                    date += 1

        return str(date)

    # example question: "Provide the number of filings where the number of days between period and filing date is within 5 to 10 days"
    def get_question(self, no_of_days1: int, no_of_days2: int) -> str:
        return f"Provide the number of filings where the number of days between period and filing date is within {no_of_days1} to {no_of_days2} days, inclusive."

    def get_qa_samples(
        self, api_response: dict[Any, Any]
    ) -> list[LongResponseQASample]:

        qa_samples: list[LongResponseQASample] = []

        days = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]

        for i in range(1, len(days)):
            question = self.get_question(no_of_days1=days[i - 1], no_of_days2=days[i])
            answer = self.get_answer(
                api_response=api_response, no_of_days1=days[i - 1], no_of_days2=days[i]
            )

            if answer is not None and answer != "None" and len(qa_samples)<2:
                task = LongResponseQASample(
                    api_response=api_response, question=question, gold_answer=answer
                )
                qa_samples.append(task)

        return qa_samples


"""
===========================================QUESTION 9============================================
"""


class FormTypes(Task):
    """
    Get the different type of forms
    """

    EVALUATION_CRITERIA = [evals.unordered_list_str_match]
    TASK_ATTRIBUTES = [TaskAttributes.FILTERING]

    # example answer: "8-K,10-K,DEF14A"
    def get_answer(self, api_response: dict[Any, Any]) -> str:

        form_type = []
        for filings in api_response["data"]["attributes"]["result"]:
            if "formType" in filings:
                form_type.append(filings["formType"])

        form_type = list(set(form_type))
        if len(form_type) != 0:
            return ", ".join(form_type)
        else:
            return "None"

    # example question: "List the different form types available."
    def get_question(self) -> str:
        return "List the different form types available. Output a comma separated list of form types and the elements should be unique."

    def get_qa_samples(
        self, api_response: dict[Any, Any]
    ) -> list[LongResponseQASample]:

        qa_samples: list[LongResponseQASample] = []
        question = self.get_question()
        answer = self.get_answer(api_response)

        if answer is not None and answer != "None" and len(qa_samples)<2:
            task = LongResponseQASample(
                api_response=api_response, question=question, gold_answer=answer
            )
            qa_samples.append(task)

        return qa_samples


"""
===========================================QUESTION 10============================================
"""


class AccessionNumberAsPerFormTypeAndDate(Task):
    """
    Get the accession number of the forms which are filed in a specific year and belong to a particular form type
    """

    EVALUATION_CRITERIA = [evals.unordered_list_str_match]
    TASK_ATTRIBUTES = [TaskAttributes.FILTERING]

    # example answer: "0001193125-12-006713,0001193125-12-006704,0001193125-12-023398,0000315066-12-002390"
    def get_answer(
        self, api_response: dict[Any, Any], year: int, form_type: str
    ) -> str:

        access_num = []
        for filings in api_response["data"]["attributes"]["result"]:
            if "filingDate" in filings:
                date = datetime.strptime(filings["filingDate"], "%Y-%m-%dT%H:%M:%S")
                filing_year = date.year
                if year == filing_year:
                    if "formType" in filings and filings["formType"] == form_type:
                        access_num.append(filings["accessionNumber"])

        if len(access_num) != 0:
            return ", ".join(access_num)
        else:
            return "None"

    # example question: "List the accession number of all the forms filed in 2019 which are of form type 8-K."
    def get_question(self, year: int, form_type: str) -> str:
        return f"List the accession number of all the forms filed in year {year} which are of form type {form_type}. Output a comma separated list of accession numbers."

    def get_qa_samples(
        self, api_response: dict[Any, Any]
    ) -> list[LongResponseQASample]:

        qa_samples: list[LongResponseQASample] = []

        form_types = []
        for filings in api_response["data"]["attributes"]["result"]:
            if "formType" in filings:
                form_types.append(filings["formType"])

        form_types = list(set(form_types))
        form_types.sort()
        for year in range(2012, 2026):
            for form in form_types:
                question = self.get_question(year=year, form_type=form)
                answer = self.get_answer(
                    api_response=api_response, year=year, form_type=form
                )

                if answer is not None and answer != "None" and len(qa_samples)<2:
                    task = LongResponseQASample(
                        api_response=api_response, question=question, gold_answer=answer
                    )
                    qa_samples.append(task)

        return qa_samples


"""
===========================================QUESTION 11============================================
"""


class AccessionNumberAsPerSameDate(Task):
    """
    Get the accession number of the filings whose filing date and period are on the same date
    """

    EVALUATION_CRITERIA = [evals.unordered_list_str_match]
    TASK_ATTRIBUTES = [TaskAttributes.FILTERING]

    # example answer: "0001181431-12-038301,0001193125-12-446915,0001193125-12-515422"
    def get_answer(self, api_response: dict[Any, Any]) -> str:

        acc_num = []
        for filings in api_response["data"]["attributes"]["result"]:
            if "period" in filings:
                filing_d = datetime.strptime(filings["filingDate"], "%Y-%m-%dT%H:%M:%S")
                filing_date = filing_d.date()
                period_d = datetime.strptime(filings["period"], "%Y-%m-%dT%H:%M:%S")
                period_date = period_d.date()

                if filing_date == period_date:
                    acc_num.append(filings["accessionNumber"])

        if len(acc_num) != 0:
            return ", ".join(acc_num)
        else:
            return "None"

    # example question: "Give the accession number of the filings whose filing date and period(if present) are on the same date."
    def get_question(self) -> str:
        return "Give the accession number of the filings whose filing date and period(if present) are on the same date. Output a comma separated list of accession numbers."

    def get_qa_samples(
        self, api_response: dict[Any, Any]
    ) -> list[LongResponseQASample]:

        qa_samples: list[LongResponseQASample] = []
        question = self.get_question()
        answer = self.get_answer(api_response)

        if answer is not None and answer != "None" and len(qa_samples)<2:
            task = LongResponseQASample(
                api_response=api_response, question=question, gold_answer=answer
            )
            qa_samples.append(task)

        return qa_samples


"""
===========================================QUESTION 12============================================
"""


class FilingsName(Task):
    """
    Get the different type of names of filings
    """

    EVALUATION_CRITERIA = [evals.unordered_list_str_match]
    TASK_ATTRIBUTES = [TaskAttributes.FILTERING]

    # example answer: "FY2324 Q3 JFM 8-K Report,THE PROCTER & GAMBLE SAVINGS PLAN 2023 Report"
    def get_answer(self, api_response: dict[Any, Any]) -> str:

        names = []
        for filings in api_response["data"]["attributes"]["result"]:
            if "name" in filings:
                names.append(filings["name"])

        names = list(set(names))
        if len(names) != 0:
            return ", ".join(names)
        else:
            return "None"

    # example question: "List the names of all types of filings."
    def get_question(self) -> str:
        return "List the names of all types of filings. Output a comma separated list of names and the elements should be unique."

    def get_qa_samples(
        self, api_response: dict[Any, Any]
    ) -> list[LongResponseQASample]:

        qa_samples: list[LongResponseQASample] = []
        question = self.get_question()
        answer = self.get_answer(api_response)

        if answer is not None and answer != "None" and len(qa_samples)<2:
            task = LongResponseQASample(
                api_response=api_response, question=question, gold_answer=answer
            )
            qa_samples.append(task)

        return qa_samples


"""
===========================================QUESTION 13============================================
"""


class AccessionNumberAsPerDateName(Task):
    """
    Get the accession number of all the filings under a specific name and are filed in a specific year
    """

    EVALUATION_CRITERIA = [evals.unordered_list_str_match]
    TASK_ATTRIBUTES = [TaskAttributes.FILTERING]

    # example answer: "0000104169-22-000088,0000104169-22-000085,0000104169-22-000080"
    def get_answer(self, api_response: dict[Any, Any], year: int, name: str) -> str:

        records = []
        for filings in api_response["data"]["attributes"]["result"]:
            if "filingDate" in filings and "name" in filings:
                date = datetime.strptime(filings["filingDate"], "%Y-%m-%dT%H:%M:%S")
                filing_year = date.year
                if filing_year == year and filings["name"] == name:
                    records.append(filings["accessionNumber"])

        if len(records) != 0:
            return ", ".join(records)
        else:
            return "None"

    # example question: "Give the accession number of all the filings under the name FWP Report and are filed in the year 2023."
    def get_question(self, year: int, name: str) -> str:
        return f"Give the accession number of all the filings under the name {name} and are filed in the year {year}. Output a comma separated list of accession numbers."

    def get_qa_samples(
        self, api_response: dict[Any, Any]
    ) -> list[LongResponseQASample]:

        qa_samples: list[LongResponseQASample] = []

        form_names = []
        for filings in api_response["data"]["attributes"]["result"]:
            if "name" in filings:
                form_names.append(filings["name"])

        form_names = list(set(form_names))
        form_names.sort()

        for year in range(2012, 2026):
            for name in form_names:

                question = self.get_question(year=year, name=name)
                answer = self.get_answer(
                    api_response=api_response, year=year, name=name
                )
                if answer is not None and answer != "None" and len(qa_samples)<2:
                    task = LongResponseQASample(
                        api_response=api_response, question=question, gold_answer=answer
                    )
                    qa_samples.append(task)

        return qa_samples


if __name__ == "__main__":
    import os

    len_qa_pairs = []
    api_responses = json.load(
        open(
            os.path.abspath(
                os.path.join(
                    os.path.dirname(__file__),
                    "./data/api_responses/SEC_filings.json",
                )
            )
        )
    )

    for app, endpoint_info in api_responses.items():
        for endpoint, query_info in endpoint_info.items():
            for query, api_response in query_info.items():

                # Question-1
                task_obj = GetFormType()
                qa_pairs = task_obj.get_qa_samples(api_response)
                if len(qa_pairs) > 0:
                    for qa_pair in qa_pairs:
                        print(qa_pair.question, "\n", qa_pair.gold_answer, "\n")
                len_qa_pairs.append(len(qa_pairs))

                # # Question-2
                # task_obj = GetFilingDate()
                # qa_pairs = task_obj.get_qa_samples(api_response)
                # if len(qa_pairs) > 0:
                #     for qa_pair in qa_pairs:
                #         print(qa_pair.question, "\n", qa_pair.gold_answer, "\n")
                # len_qa_pairs.append(len(qa_pairs))

                # # Question-3
                # task_obj = GetFilingName()
                # qa_pairs = task_obj.get_qa_samples(api_response)
                # if len(qa_pairs) > 0:
                #     for qa_pair in qa_pairs:
                #         print(qa_pair.question, "\n", qa_pair.gold_answer, "\n")
                # len_qa_pairs.append(len(qa_pairs))

                # # Question-4
                # task_obj = FilingsInAYear()
                # qa_pairs = task_obj.get_qa_samples(api_response)
                # if len(qa_pairs) > 0:
                #     for qa_pair in qa_pairs:
                #         print(qa_pair.question, "\n", qa_pair.gold_answer, "\n")
                # len_qa_pairs.append(len(qa_pairs))

                # # Question-5
                # task_obj = FilingsOfSpecificFormType()
                # qa_pairs = task_obj.get_qa_samples(api_response)
                # if len(qa_pairs) > 0:
                #     for qa_pair in qa_pairs:
                #         print(qa_pair.question, "\n", qa_pair.gold_answer, "\n")
                # len_qa_pairs.append(len(qa_pairs))

                # # Question-6
                # task_obj = FilingsOfSpecificName()
                # qa_pairs = task_obj.get_qa_samples(api_response)
                # if len(qa_pairs) > 0:
                #     for qa_pair in qa_pairs:
                #         print(qa_pair.question, "\n", qa_pair.gold_answer, "\n")
                # len_qa_pairs.append(len(qa_pairs))

                # # Question-7
                # task_obj = FilingsWithNameAndType()
                # qa_pairs = task_obj.get_qa_samples(api_response)
                # if len(qa_pairs) > 0:
                #     for qa_pair in qa_pairs:
                #         print(qa_pair.question, "\n", qa_pair.gold_answer, "\n")
                # len_qa_pairs.append(len(qa_pairs))

                # # Question-8
                # task_obj = FilingsAccordingToFilingDateAndPeriod()
                # qa_pairs = task_obj.get_qa_samples(api_response)
                # if len(qa_pairs) > 0:
                #     for qa_pair in qa_pairs:
                #         print(qa_pair.question, "\n", qa_pair.gold_answer, "\n")
                # len_qa_pairs.append(len(qa_pairs))

                # # Question-9
                # task_obj = FormTypes()
                # qa_pairs = task_obj.get_qa_samples(api_response)
                # if len(qa_pairs) > 0:
                #     for qa_pair in qa_pairs:
                #         print(qa_pair.question, "\n", qa_pair.gold_answer, "\n")
                # len_qa_pairs.append(len(qa_pairs))

                # # Question-10
                # task_obj = AccessionNumberAsPerFormTypeAndDate()
                # qa_pairs = task_obj.get_qa_samples(api_response)
                # if len(qa_pairs) > 0:
                #     for qa_pair in qa_pairs:
                #         print(qa_pair.question, "\n", qa_pair.gold_answer, "\n")
                # len_qa_pairs.append(len(qa_pairs))

                # # Question-11
                # task_obj = AccessionNumberAsPerSameDate()
                # qa_pairs = task_obj.get_qa_samples(api_response)
                # if len(qa_pairs) > 0:
                #     for qa_pair in qa_pairs:
                #         print(qa_pair.question, "\n", qa_pair.gold_answer, "\n")
                # len_qa_pairs.append(len(qa_pairs))

                # # Question-12
                # task_obj = FilingsName()
                # qa_pairs = task_obj.get_qa_samples(api_response)
                # if len(qa_pairs) > 0:
                #     for qa_pair in qa_pairs:
                #         print(qa_pair.question, "\n", qa_pair.gold_answer, "\n")
                # len_qa_pairs.append(len(qa_pairs))

                # # Question-13
                # task_obj = AccessionNumberAsPerDateName()
                # qa_pairs = task_obj.get_qa_samples(api_response)
                # if len(qa_pairs) > 0:
                #     for qa_pair in qa_pairs:
                #         print(qa_pair.question, "\n", qa_pair.gold_answer, "\n")
                # len_qa_pairs.append(len(qa_pairs))
