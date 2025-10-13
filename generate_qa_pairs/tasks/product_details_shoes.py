import json
import re
from typing import Any

from . import evals
from .base import Task
from .data_structures import LongResponseQASample, TaskAttributes

"""
===========================================QUESTION 1============================================
"""


class GetShoeDepartment(Task):
    """
    Get the department of the shoe
    """

    EVALUATION_CRITERIA = [evals.accuracy_string]
    TASK_ATTRIBUTES = [TaskAttributes.EXTRACTIVE]

    # example answer: "Women's"
    def get_answer(self, id: str, api_response: dict[Any, Any]) -> str:

        for products in api_response["data"]["products"]:
            if (
                id == products["product_id"]
                and "Department" in products["product_attributes"]
            ):
                attributes = products["product_attributes"]
                return str(attributes["Department"])

        return "None"

    # example question: "In which department does the shoe with id 7815766634275247088 belong to?"
    def get_question(self, id: str) -> str:
        return f"In which department does the shoe with ID {id} belong to?"

    def get_qa_samples(
        self, api_response: dict[Any, Any]
    ) -> list[LongResponseQASample]:

        qa_samples: list[LongResponseQASample] = []

        for product_details in api_response["data"]["products"]:
            id = product_details["product_id"]
            question = self.get_question(id=id)
            answer = self.get_answer(id=id, api_response=api_response)

            if answer is not None and answer != "None" and len(qa_samples)<5:
                task = LongResponseQASample(
                    api_response=api_response, question=question, gold_answer=answer
                )
                qa_samples.append(task)

        return qa_samples


"""
===========================================QUESTION 2============================================
"""


class GetProductRating(Task):
    """
    Get the product rating of the  shoe
    """

    EVALUATION_CRITERIA = [evals.accuracy_string]
    TASK_ATTRIBUTES = [TaskAttributes.EXTRACTIVE]

    # example answer: "4.5"
    def get_answer(self, id: str, api_response: dict[Any, Any]) -> str:

        for products in api_response["data"]["products"]:
            if id == products["product_id"]:
                return str(products["product_rating"])

        return "None"

    # example question: "What is the rating of the shoe with id 7815766634275247088?""
    def get_question(self, id: str) -> str:
        return f"What is the rating of the shoe with ID {id}?"

    def get_qa_samples(
        self, api_response: dict[Any, Any]
    ) -> list[LongResponseQASample]:

        qa_samples: list[LongResponseQASample] = []

        for product_details in api_response["data"]["products"]:
            id = product_details["product_id"]
            question = self.get_question(id=id)
            answer = self.get_answer(id=id, api_response=api_response)

            if answer is not None and answer != "None" and len(qa_samples)<5:
                task = LongResponseQASample(
                    api_response=api_response, question=question, gold_answer=answer
                )
                qa_samples.append(task)

        return qa_samples


"""
===========================================QUESTION 3============================================
"""


class GetProductTitle(Task):
    """
    Get the product title of the shoe
    """

    EVALUATION_CRITERIA = [evals.accuracy_string]
    TASK_ATTRIBUTES = [TaskAttributes.EXTRACTIVE]

    # example answer: "Nike Air Max Invigor Trainers Mens - Black/Volt/Grey"
    def get_answer(self, id: str, api_response: dict[Any, Any]) -> str:

        for products in api_response["data"]["products"]:
            if id == products["product_id"]:
                return str(products["product_title"])

        return "None"

    # example question: "What is the title for the shoe with id 13571232387326125139?"
    def get_question(self, id: str) -> str:
        return f"What is the title for the shoe with ID {id}?"

    def get_qa_samples(
        self, api_response: dict[Any, Any]
    ) -> list[LongResponseQASample]:

        qa_samples: list[LongResponseQASample] = []

        for product_details in api_response["data"]["products"]:
            id = product_details["product_id"]
            question = self.get_question(id=id)
            answer = self.get_answer(id=id, api_response=api_response)

            if answer is not None and answer != "None" and len(qa_samples)<5:
                task = LongResponseQASample(
                    api_response=api_response, question=question, gold_answer=answer
                )
                qa_samples.append(task)

        return qa_samples


"""
===========================================QUESTION 4============================================
"""


class ShoeColours(Task):
    """
    Get the number of shoes which are available in a particular color
    """

    EVALUATION_CRITERIA = [evals.approx_number_match]
    TASK_ATTRIBUTES = [TaskAttributes.AGGREGATION]

    # example answer: "4"
    def get_answer(self, api_response: dict[Any, Any], color: str) -> str:

        total_shoes = 0
        for product_details in api_response["data"]["products"]:
            if "product_attributes" in product_details:
                attributes = product_details["product_attributes"]
                if "Color" in attributes and color in attributes["Color"]:
                    total_shoes += 1

        if total_shoes != 0:
            return str(total_shoes)
        else:
            return "None"

    # example question: "Provide the number of shoes which are available in black colour."
    def get_question(self, color: str) -> str:
        return f"Provide the number of shoes which are available in {color} colour."

    def get_qa_samples(
        self, api_response: dict[Any, Any]
    ) -> list[LongResponseQASample]:

        qa_samples: list[LongResponseQASample] = []
        all_colors = []
        for shoes in api_response["data"]["products"]:
            if "product_attributes" in shoes and "Color" in shoes["product_attributes"]:
                if "," in shoes["product_attributes"]["Color"]:
                    all_colors.extend(shoes["product_attributes"]["Color"].split(","))
                else:
                    all_colors.append(shoes["product_attributes"]["Color"])

        # Getting each individual color
        shoes_color = []
        for color in all_colors:
            if "/" in color:
                shoes_color.extend(color.split("/"))
            else:
                shoes_color.append(color)

        shoes_color = [item.strip() for item in shoes_color]
        shoes_color = list(set(shoes_color))
        if "" in shoes_color:
            shoes_color.remove("")

        shoes_color.sort()

        for color in shoes_color:
            question = self.get_question(color=color)
            answer = self.get_answer(api_response=api_response, color=color)

            if answer is not None and answer != "None" and len(qa_samples)<5:
                task = LongResponseQASample(
                    api_response=api_response, question=question, gold_answer=answer
                )
                qa_samples.append(task)

        return qa_samples


"""
===========================================QUESTION 5============================================
"""


class ShoesInEachDepartment(Task):
    """
    Get the number of shoes which belong to a particular department
    """

    EVALUATION_CRITERIA = [evals.approx_number_match]
    TASK_ATTRIBUTES = [TaskAttributes.AGGREGATION]

    # example answer: "4"
    def get_answer(self, api_response: dict[Any, Any], department: str) -> str:

        dept = 0
        for product_details in api_response["data"]["products"]:
            attributes = product_details["product_attributes"]
            if "Department" in attributes and department in attributes["Department"]:
                dept += 1

        if dept != 0:
            return str(dept)
        else:
            return "None"

    # example question: "Provide the number of shoes which are for Men."
    def get_question(self, department: str) -> str:
        return f"Provide the number of shoes which are for {department}."

    def get_qa_samples(
        self, api_response: dict[Any, Any]
    ) -> list[LongResponseQASample]:

        qa_samples: list[LongResponseQASample] = []
        departments_considered = ["Men", "Women", "Unisex", "Children"]

        for department in departments_considered:
            question = self.get_question(department=department)
            answer = self.get_answer(api_response=api_response, department=department)

            if answer is not None and answer != "None" and len(qa_samples)<5:
                task = LongResponseQASample(
                    api_response=api_response, question=question, gold_answer=answer
                )
                qa_samples.append(task)

        return qa_samples


"""
===========================================QUESTION 6============================================
"""


class ShoeSize(Task):
    """
    Get the number of shoes of particular size
    """

    EVALUATION_CRITERIA = [evals.approx_number_match]
    TASK_ATTRIBUTES = [TaskAttributes.AGGREGATION]

    # example answer: "7"
    def get_answer(self, api_response: dict[Any, Any], size: str) -> str:

        size_count = 0
        for product_details in api_response["data"]["products"]:
            attributes = product_details["product_attributes"]
            if "Size" in attributes and size in attributes["Size"]:
                size_count += 1

        if size_count != 0:
            return str(size_count)
        else:
            return "None"

    # example question: "How many number of shoes are present in size 4?"
    def get_question(self, size: str) -> str:
        return f"How many shoes are present in {size}?"

    def get_qa_samples(
        self, api_response: dict[Any, Any]
    ) -> list[LongResponseQASample]:

        qa_samples: list[LongResponseQASample] = []

        all_sizes = []
        for shoes in api_response["data"]["products"]:
            if "product_attributes" in shoes and "Size" in shoes["product_attributes"]:
                if "," in shoes["product_attributes"]["Size"]:
                    all_sizes.extend(shoes["product_attributes"]["Size"].split(","))
                else:
                    all_sizes.append(shoes["product_attributes"]["Size"])

        all_sizes = [item.strip() for item in all_sizes]
        all_sizes = list(set(all_sizes))
        all_sizes.sort()
        for size in all_sizes:
            question = self.get_question(size=size)
            answer = self.get_answer(api_response=api_response, size=size)

            if answer is not None and answer != "None" and len(qa_samples)<5:
                task = LongResponseQASample(
                    api_response=api_response, question=question, gold_answer=answer
                )
                qa_samples.append(task)

        return qa_samples


"""
===========================================QUESTION 7============================================
"""


class ShoeMaterialType(Task):
    """
    Get the number of shoes which are made up of particular material and belong to a particular shoe type
    """

    EVALUATION_CRITERIA = [evals.approx_number_match]
    TASK_ATTRIBUTES = [TaskAttributes.AGGREGATION]

    # example answer: "4"
    def get_answer(
        self, api_response: dict[Any, Any], material: str, shoe_type: str
    ) -> str:

        shoe_type_material = 0
        for product_details in api_response["data"]["products"]:
            attributes = product_details["product_attributes"]
            if "Material" in attributes and material in attributes["Material"]:
                if "Type" in attributes and shoe_type in attributes["Type"]:
                    shoe_type_material += 1

        if shoe_type_material != 0:
            return str(shoe_type_material)
        else:
            return "None"

    # example question: "How many number of shoes are present which are made up of Canvas and type Boots?"
    def get_question(self, material: str, shoe_type: str) -> str:
        return f"How many shoes are present which are made up of {material} and type {shoe_type}?"

    def get_qa_samples(
        self, api_response: dict[Any, Any]
    ) -> list[LongResponseQASample]:

        qa_samples: list[LongResponseQASample] = []

        all_types = []
        for shoes in api_response["data"]["products"]:
            if "product_attributes" in shoes and "Type" in shoes["product_attributes"]:
                if "," in shoes["product_attributes"]["Type"]:
                    all_types.extend(shoes["product_attributes"]["Type"].split(","))
                else:
                    all_types.append(shoes["product_attributes"]["Type"])

        all_types = [item.strip() for item in all_types]
        all_types = list(set(all_types))
        all_types.sort()

        materials = []
        for shoes in api_response["data"]["products"]:
            if (
                "product_attributes" in shoes
                and "Material" in shoes["product_attributes"]
            ):
                if "," in shoes["product_attributes"]["Material"]:
                    materials.extend(shoes["product_attributes"]["Material"].split(","))
                else:
                    materials.append(shoes["product_attributes"]["Material"])

        materials = [item.strip() for item in materials]
        materials = list(set(materials))
        materials.sort()

        for material in materials:
            for type in all_types:
                question = self.get_question(material=material, shoe_type=type)
                answer = self.get_answer(
                    api_response=api_response, material=material, shoe_type=type
                )

                if answer is not None and answer != "None" and len(qa_samples)<5:
                    task = LongResponseQASample(
                        api_response=api_response, question=question, gold_answer=answer
                    )
                    qa_samples.append(task)

        return qa_samples


"""
===========================================QUESTION 8============================================
"""


class OfferedProductPrice(Task):
    """
    Aggregation based on the price of the shoes
    """

    EVALUATION_CRITERIA = [evals.approx_number_match]
    TASK_ATTRIBUTES = [TaskAttributes.AGGREGATION]

    # example answer: "10"
    def get_answer(
        self, api_response: dict[Any, Any], price1: float, price2: float
    ) -> str:

        no_of_shoes = 0
        for products in api_response["data"]["products"]:
            if "offer" in products and "price" in products["offer"]:
                cost = products["offer"]["price"][1:].replace(",","")
                price = float(cost)
                if price >= price1 and price <= price2:
                    no_of_shoes += 1

        if no_of_shoes != 0:
            return str(no_of_shoes)
        else:
            return "0"

    # example question: "Get the number of shoes whose price is between 0 and 49 dollars, inclusive."
    def get_question(self, price1: float, price2: float) -> str:
        return f"Get the number of shoes whose price is between {price1} and {price2} dollars, inclusive."

    def get_qa_samples(
        self, api_response: dict[Any, Any]
    ) -> list[LongResponseQASample]:

        qa_samples: list[LongResponseQASample] = []
        prices = [0, 50, 100, 150, 200, 250, 300, 350, 400]

        for i in range(1, len(prices)):
            question = self.get_question(price1=prices[i - 1], price2=prices[i] - 1)
            answer = self.get_answer(
                api_response=api_response, price1=prices[i - 1], price2=prices[i] - 1
            )

            if answer is not None and answer != "None" and len(qa_samples)<5:
                task = LongResponseQASample(
                    api_response=api_response, question=question, gold_answer=answer
                )
                qa_samples.append(task)

        return qa_samples


"""
===========================================QUESTION 9============================================
"""


class ShoesInMultipleColours(Task):
    """Get the ids of the shoes which are available in a particular number of colors"""

    EVALUATION_CRITERIA = [evals.unordered_list_str_match]
    TASK_ATTRIBUTES = [TaskAttributes.FILTERING]

    # example answer: "147489686195998428","8498930582938164209"
    def get_answer(self, api_response: dict[Any, Any], no_of_colors: int) -> str:

        ids = []
        for product_details in api_response["data"]["products"]:
            attributes = product_details["product_attributes"]
            colors = []
            if "Color" in attributes:
                if "," in attributes["Color"]:
                    colors = attributes["Color"].split(",")
                else:
                    colors = list(attributes["Color"])
            if len(colors) == no_of_colors:
                ids.append(product_details["product_id"])

        if len(ids) != 0:
            return ", ".join(ids)
        else:
            return "None"

    # example question: "Give me the list of shoe's IDs which are present in 5 colour/s. Output a comma separated list of IDs."
    def get_question(self, no_of_colors: int) -> str:
        return f"Give me the list of shoe's IDs which are present in {no_of_colors} colour/s. Output a comma separated list of IDs."

    def get_qa_samples(
        self, api_response: dict[Any, Any]
    ) -> list[LongResponseQASample]:

        qa_samples: list[LongResponseQASample] = []
        for color_num in range(1, 20):
            question = self.get_question(no_of_colors=color_num)
            answer = self.get_answer(api_response=api_response, no_of_colors=color_num)

            if answer is not None and answer != "None" and len(qa_samples)<5:
                task = LongResponseQASample(
                    api_response=api_response, question=question, gold_answer=answer
                )
                qa_samples.append(task)

        return qa_samples


"""
===========================================QUESTION 10============================================
"""


class GetShoesColorsAsPerDeptAndRating(Task):
    """
    Get the list of colors in which particular department shoes are available and has a rating and above.
    """

    EVALUATION_CRITERIA = [evals.unordered_list_str_match]
    TASK_ATTRIBUTES = [TaskAttributes.FILTERING]

    # example answer: "Midnight Navy,Pure Platinum,Clear,Orange,White,Black "
    def get_answer(
        self, api_response: dict[Any, Any], department: str, rating: float
    ) -> str:

        colors = []
        for product_details in api_response["data"]["products"]:
            attributes = product_details["product_attributes"]
            if "Department" in attributes and department in attributes["Department"]:
                if (
                    "product_rating" in product_details
                    and product_details["product_rating"] is not None
                    and product_details["product_rating"] >= rating
                ):

                    if "Color" in attributes:
                        if "," in attributes["Color"]:
                            colors.extend(attributes["Color"].split(","))
                        else:
                            colors.append(attributes["Color"])

        colors = [item.strip() for item in colors]
        colors = list(set(colors))
        if len(colors) != 0:
            return ", ".join(colors)
        else:
            return "None"

    # example question: "Give the list of colors in which Women shoes are available and has a rating of 3.5 and above.Output a comma separated list of colors."
    def get_question(self, department: str, rating: float) -> str:
        return f"Give the list of colors in which {department} shoes are available and has a rating of {rating} and above. Output a comma separated list of colors"

    def get_qa_samples(
        self, api_response: dict[Any, Any]
    ) -> list[LongResponseQASample]:

        qa_samples: list[LongResponseQASample] = []

        departments_considered = ["Men", "Women", "Unisex", "Children"]
        ratings_considered = [2.5, 3, 3.5, 4, 4.5]

        for dept in departments_considered:
            for ratings in ratings_considered:
                question = self.get_question(department=dept, rating=ratings)
                answer = self.get_answer(
                    api_response=api_response, department=dept, rating=ratings
                )

                if answer is not None and answer != "None" and len(qa_samples)<5:
                    task = LongResponseQASample(
                        api_response=api_response, question=question, gold_answer=answer
                    )
                    qa_samples.append(task)

        return qa_samples


"""
===========================================QUESTION 11============================================
"""


class GetProductIdOfTrainerShoes(Task):
    """
    Give the Product ids shoes which are of Trainer type which don't belong to a particular department and
    has a product rating and above.
    """

    EVALUATION_CRITERIA = [evals.unordered_list_str_match]
    TASK_ATTRIBUTES = [TaskAttributes.FILTERING]

    # example answer: "13571232387326125139,700729613184503582,4429409664881471740"
    def get_answer(
        self, api_response: dict[Any, Any], department: str, rating: float
    ) -> str:

        ids = []
        for product_details in api_response["data"]["products"]:
            attributes = product_details["product_attributes"]
            if "Trainer" in attributes and attributes["Trainer"] == "Yes":

                if (
                    "Department" in attributes
                    and department not in attributes["Department"]
                ):
                    if (
                        product_details["product_rating"] is not None
                        and float(product_details["product_rating"]) >= rating
                    ):
                        ids.append(product_details["product_id"])

        if len(ids) != 0:
            return ", ".join(ids)
        else:
            return "None"

    # example question: "Give the Product ids of the trainer shoes which don't belong to Children. Among them include only those shoes whose product rating is 4 and above.Output a comma separated list of IDs."
    def get_question(self, department: str, rating: float) -> str:
        return f"Give the Product IDs of the trainer shoes which don't belong to {department}. Among them include only those shoes whose product rating is {rating} and above. Output a comma separated list of IDs."

    def get_qa_samples(
        self, api_response: dict[Any, Any]
    ) -> list[LongResponseQASample]:

        qa_samples: list[LongResponseQASample] = []

        departments_considered = ["Men", "Women", "Unisex", "Children"]
        ratings_considered = [2.5, 3, 3.5, 4, 4.5]

        for dept in departments_considered:
            for ratings in ratings_considered:
                question = self.get_question(department=dept, rating=ratings)
                answer = self.get_answer(
                    api_response=api_response, department=dept, rating=ratings
                )

                if answer is not None and answer != "None" and len(qa_samples)<5:
                    task = LongResponseQASample(
                        api_response=api_response, question=question, gold_answer=answer
                    )
                    qa_samples.append(task)

        return qa_samples


"""
===========================================QUESTION 12============================================
"""


class ShoesOnSaleAndFreeDelivery(Task):
    """
    Get the IDs of the shoes which are on sale and has free delivery
    """

    EVALUATION_CRITERIA = [evals.unordered_list_str_match]
    TASK_ATTRIBUTES = [TaskAttributes.FILTERING]

    # example answer: "7196363252962315247,2856774367875385079,2991800802362867681,13118781327639094025,8626419197147424360"
    def get_answer(self, api_response: dict[Any, Any]) -> str:

        offer_id = []
        for products in api_response["data"]["products"]:
            if "offer" in products:
                offer = products["offer"]
                if (
                    "shipping" in offer
                    and "free delivery" in (offer["shipping"]).lower()
                ):
                    if "on_sale" in offer and offer["on_sale"]:
                        offer_id.append(offer["offer_id"])

        if len(offer_id) != 0:
            return ", ".join(offer_id)
        else:
            return "None"

    # example question: "Give the offer iDs of the shoes which are on sale and has free delivery.Output a comma separated list of IDs."
    def get_question(self) -> str:
        return "Give the offer IDs of the shoes which are on sale and has free delivery. Output a comma separated list of IDs."

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


"""
===========================================QUESTION 13============================================
"""


class ProductsIDsHavingDiscount(Task):
    """
    Get the IDs of the products having discount within certain range
    """

    EVALUATION_CRITERIA = [evals.unordered_list_str_match]
    TASK_ATTRIBUTES = [TaskAttributes.FILTERING]

    # example answer: "3668966513965198054,11224118251868226969,4944277187140173487"
    def get_answer(
        self, api_response: dict[Any, Any], discount1: float, discount2: float
    ) -> str:

        shoe_ids = []
        for products in api_response["data"]["products"]:
            if (
                "offer" in products
                and "coupon_discount_percent" in products["offer"]
                and products["offer"]["coupon_discount_percent"] is not None
            ):

                if re.fullmatch(
                    r"\d+% off", products["offer"]["coupon_discount_percent"]
                ):
                    coupon = products["offer"]["coupon_discount_percent"].split(" ")[0]
                    discount = float(coupon[:-1])
                    if discount >= discount1 and discount <= discount2:
                        shoe_ids.append(products["product_id"])

        if len(shoe_ids) != 0:
            return ", ".join(shoe_ids)
        else:
            return "None"

    # example question: "Give the product IDs of the shoes which have a discount percentage between 60% and 70%, inclusive. Output a comma separated list of IDs"
    def get_question(self, discount1: float, discount2: float) -> str:
        return f"Give the product IDs of the shoes which have a discount percentage between {discount1}% and {discount2}%, inclusive. Output a comma separated list of IDs."

    def get_qa_samples(
        self, api_response: dict[Any, Any]
    ) -> list[LongResponseQASample]:

        qa_samples: list[LongResponseQASample] = []
        discount = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]
        for i in range(1, len(discount)):

            question = self.get_question(
                discount1=discount[i - 1], discount2=discount[i]
            )
            answer = self.get_answer(
                api_response=api_response,
                discount1=discount[i - 1],
                discount2=discount[i],
            )

            if answer is not None and answer != "None" and len(qa_samples)<5:
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
                    "./data/api_responses/real-time-product-search-shoes.json",
                )
            )
        )
    )
    qa = 0
    for app, endpoint_info in api_responses.items():
        for endpoint, query_info in endpoint_info.items():
            for query, api_response in query_info.items():

                # # Question-1
                # task_obj = GetShoeDepartment()
                # qa_pairs = task_obj.get_qa_samples(api_response)
                # if len(qa_pairs) > 0:
                #     for qa_pair in qa_pairs:
                #         print(qa_pair.question, "\n", qa_pair.gold_answer, "\n")
                # len_qa_pairs.append(len(qa_pairs))

                # #Question-2
                # task_obj = GetProductRating()
                # qa_pairs = task_obj.get_qa_samples(api_response)
                # qa+=len(qa_pairs)
                # if len(qa_pairs) > 0:
                #     for qa_pair in qa_pairs:
                #         print(qa_pair.question, '\n', qa_pair.gold_answer, '\n')
                # len_qa_pairs.append(len(qa_pairs))

                # # Question-3
                # task_obj = GetProductTitle()
                # qa_pairs = task_obj.get_qa_samples(api_response)
                # qa += len(qa_pairs)
                # if len(qa_pairs) > 0:
                #     for qa_pair in qa_pairs:
                #         print(qa_pair.question, '\n', qa_pair.gold_answer, '\n')
                # len_qa_pairs.append(len(qa_pairs))

                # Question-4
                task_obj = ShoeColours()
                qa_pairs = task_obj.get_qa_samples(api_response)
                if len(qa_pairs) > 0:
                    for qa_pair in qa_pairs:
                        print(qa_pair.question, '\n', qa_pair.gold_answer, '\n')
                len_qa_pairs.append(len(qa_pairs))
                print(len_qa_pairs)

                # # Question-5
                # task_obj = ShoesInEachDepartment()
                # qa_pairs = task_obj.get_qa_samples(api_response)
                # if len(qa_pairs) > 0:
                #     for qa_pair in qa_pairs:
                #         print(qa_pair.question, '\n', qa_pair.gold_answer, '\n')
                # len_qa_pairs.append(len(qa_pairs))

                # # Question-6
                # task_obj = ShoeSize()
                # qa_pairs = task_obj.get_qa_samples(api_response)
                # if len(qa_pairs) > 0:
                #     for qa_pair in qa_pairs:
                #         print(qa_pair.question, '\n', qa_pair.gold_answer, '\n')
                # len_qa_pairs.append(len(qa_pairs))

                # # Question-7
                # task_obj = ShoeMaterialType()
                # qa_pairs = task_obj.get_qa_samples(api_response)
                # if len(qa_pairs) > 0:
                #     for qa_pair in qa_pairs:
                #         print(qa_pair.question, '\n', qa_pair.gold_answer, '\n')
                # len_qa_pairs.append(len(qa_pairs))

                # # Question-8
                # task_obj = OfferedProductPrice()
                # qa_pairs = task_obj.get_qa_samples(api_response)
                # if len(qa_pairs) > 0:
                #     for qa_pair in qa_pairs:
                #         print(qa_pair.question, '\n', qa_pair.gold_answer, '\n')
                # len_qa_pairs.append(len(qa_pairs))

                # # Question-9
                # task_obj = ShoesInMultipleColours()
                # qa_pairs = task_obj.get_qa_samples(api_response)
                # if len(qa_pairs) > 0:
                #     for qa_pair in qa_pairs:
                #         print(qa_pair.question, '\n', qa_pair.gold_answer, '\n')
                # len_qa_pairs.append(len(qa_pairs))

                # # Question-10
                # task_obj = GetShoesColorsAsPerDeptAndRating()
                # qa_pairs = task_obj.get_qa_samples(api_response)
                # if len(qa_pairs) > 0:
                #     for qa_pair in qa_pairs:
                #         print(qa_pair.question, '\n', qa_pair.gold_answer, '\n')
                # len_qa_pairs.append(len(qa_pairs))

                # # Question-11
                # task_obj = GetProductIdOfTrainerShoes()
                # qa_pairs = task_obj.get_qa_samples(api_response)
                # if len(qa_pairs) > 0:
                #     for qa_pair in qa_pairs:
                #         print(qa_pair.question, '\n', qa_pair.gold_answer, '\n')
                # len_qa_pairs.append(len(qa_pairs))

                # # Question-12
                # task_obj = ShoesOnSaleAndFreeDelivery()
                # qa_pairs = task_obj.get_qa_samples(api_response)
                # if len(qa_pairs) > 0:
                #     for qa_pair in qa_pairs:
                #         print(qa_pair.question, '\n', qa_pair.gold_answer, '\n')
                # len_qa_pairs.append(len(qa_pairs))

                # # Question-13
                # task_obj = ProductsIDsHavingDiscount()
                # qa_pairs = task_obj.get_qa_samples(api_response)
                # if len(qa_pairs) > 0:
                #     for qa_pair in qa_pairs:
                #         print(qa_pair.question, '\n', qa_pair.gold_answer, '\n')
                # len_qa_pairs.append(len(qa_pairs))
