import json
from abc import ABC, abstractmethod
from typing import Any

import numpy as np
from generate_qa_pairs.tasks import evals

from generate_qa_pairs.tasks.data_structures import LongResponseQASample, TaskAttributes


class Task(ABC):

    EVALUATION_CRITERIA: list[Any] = []
    EVALUATION_METRICS: dict[Any] = {}
    TASK_ATTRIBUTES: list[TaskAttributes] = []

    @abstractmethod
    def get_qa_samples(
        self, api_response: dict[Any, Any]
    ) -> list[LongResponseQASample]:
        """
        Get a list of Long Response QA samples given an API response
        """
        raise NotImplementedError


    def evaluate_task(self, qa_task: LongResponseQASample) -> dict:
        """
        Evaluate the task results using the gold and predicted answers.
        The EVALUATION_CRITERIA variable defines the list of evaluation metrics
        """
        assert len(self.EVALUATION_CRITERIA) > 0, "Evaluation criteria not set for task"
        self.EVALUATION_METRICS = {}

        if self.EVALUATION_CRITERIA[0] is evals.accuracy_string:
            self.EVALUATION_METRICS["accuracy_string"] = evals.accuracy_string
        if self.EVALUATION_CRITERIA[0] is evals.unordered_list_str_match:
            self.EVALUATION_METRICS["unordered_list_str_match"] = evals.unordered_list_str_match
        if self.EVALUATION_CRITERIA[0] is evals.approx_number_match:
            self.EVALUATION_METRICS["approx_number_match"] = evals.approx_number_match

        self.EVALUATION_METRICS["contains"] = evals.contains
        self.EVALUATION_METRICS["code_exec_Passed"] = evals.code_exec_Passed

        eval_metrics = {
            eval_type: eval_criteria(qa_task) for eval_type,eval_criteria in self.EVALUATION_METRICS.items()
        }

        return eval_metrics

