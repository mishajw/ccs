from typing import Any

import datasets

from repeng.datasets.elk.types import BinaryRow, Split
from repeng.datasets.utils.shuffles import deterministic_shuffle

_DATASET_ID = "race"
# Taken from https://arxiv.org/abs/2310.01405 D.1.7.
_TEMPLATE = (
    "Consider the correctness of the answer to the following question based on the "
    "article:\n"
    "\n"
    "Article: {article}\n"
    "\n"
    "Question: {question}\n"
    "Answer: {answer}\n"
    "The probability of the answer being correct is"
)
_ANSWER_TO_INDEX = {"A": 0, "B": 1, "C": 2, "D": 3}


def get_race() -> dict[str, BinaryRow]:
    return {
        **_get_race_split("train"),
        **_get_race_split("validation"),
    }


def _get_race_split(split: Split) -> dict[str, BinaryRow]:
    dataset: Any = datasets.load_dataset("race", "all")
    results = {}
    for row in deterministic_shuffle(dataset[split], lambda row: row["example_id"]):
        group_id = row["example_id"]
        for option_idx, option in enumerate(row["options"]):
            format_args = dict(
                article=row["article"], question=row["question"], answer=option
            )
            results[f"{_DATASET_ID}-{group_id}-{option_idx}"] = BinaryRow(
                dataset_id=_DATASET_ID,
                split=split,
                group_id=group_id,
                text=_TEMPLATE.format(**format_args),
                is_true=_ANSWER_TO_INDEX[row["answer"]] == option_idx,
                format_args=format_args,
            )
    return results
