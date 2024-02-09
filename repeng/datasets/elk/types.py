from typing import Literal, get_args

from pydantic import BaseModel

Split = Literal["train", "train-hparams", "validation"]

DatasetId = Literal[
    "arc_challenge",
    "arc_easy",
    "got_cities",
    "got_sp_en_trans",
    "got_larger_than",
    "got_cities_cities_conj",
    "got_cities_cities_disj",
    "common_sense_qa",
    "open_book_qa",
    "race",
    "truthful_qa",
    "truthful_model_written",
    "true_false",
    "imdb",
    "amazon_polarity",
    "ag_news",
    "dbpedia_14",
    "rte",
    "copa",
    "boolq",
    "piqa",
    "open_book_qa/qa",
    "race/qa",
    "arc_challenge/qa",
    "arc_easy/qa",
    "common_sense_qa/qa",
]

DlkDatasetId = Literal[
    "imdb",
    "amazon_polarity",
    "ag_news",
    "dbpedia_14",
    "rte",
    "copa",
    "boolq",
    "piqa",
]

GroupedDatasetId = Literal[
    "arc_challenge",
    "arc_easy",
    "common_sense_qa",
    "open_book_qa",
    "race",
    "truthful_qa",
    "truthful_model_written",
    "true_false",
]


class BinaryRow(BaseModel, extra="forbid"):
    dataset_id: DatasetId
    split: Split
    text: str
    is_true: bool
    format_args: dict[str, str]
    group_id: str | None = None
    """
    Rows are grouped, for example by question, in order to allow for probes that take
    into account intra-group relationships.
    """
    answer_type: str | None = None
    """
    For example, 'true' and 'false' for answers to true/false questions, or 'A', 'B',
    'C', or 'D' for multiple choice questions.
    If not set, the prompt template doesn't include any consistent answer templates
    (e.g. it's just question-answer).
    """


RepeTemplateId = Literal["qa", "repe"]


def is_dataset_grouped(dataset_id: DatasetId) -> bool:
    return dataset_id in get_args(GroupedDatasetId)
