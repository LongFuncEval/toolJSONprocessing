from dataclasses import dataclass
from enum import Enum
from typing import Any, Union


class TaskAttributes(Enum):
    EXTRACTIVE = "EXTRACTIVE" # Simple extraction of answers from the API response
    FILTERING = "FILTERING" # Filtering of the API response based on some conditions, similar to a select operator in relational algebra
    AGGREGATION = "AGGREGATION" # Aggregation over the API response elements, such as lowest price, latest album


@dataclass
class LongResponseQASample:
    api_response: dict[Any, Any]
    question: str
    gold_answer: Any
    schema: str = ''
    pred_answer: Any = None
    model_output: Any = None
    code_exec_status: str = ''
    metrics: Any = None
    task: str = None
    task_type: Union[list[TaskAttributes], None] = None
    uid: str = None
