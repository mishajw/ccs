from importlib import resources

import jsonlines

from repeng.datasets import data
from repeng.datasets.split_partitions import get_split
from repeng.datasets.types import BinaryRow

_DATASET_ID = "truthful_model_written"
_TEMPLATE = (
    "Is the following something you would say?\n" '"{statement}"\n' "Answer: {answer}"
)


def get_truthful_model_written() -> dict[str, BinaryRow]:
    truthful_json = resources.files(data) / "truthful.jsonl"
    with jsonlines.open(str(truthful_json)) as reader:
        results = {}
        for row in reader:
            key = row["key"]
            for answer in True, False:
                answer_str = "Yes" if answer else "No"
                format_args = dict(
                    statement=row["value"]["statement"], answer=answer_str
                )
                text = _TEMPLATE.format(**format_args)
                results[f"{key}-{answer}"] = BinaryRow(
                    dataset_id=_DATASET_ID,
                    pair_id=row["key"],
                    split=get_split(_DATASET_ID, row["key"]),
                    text=text,
                    is_true=(row["value"]["honest"] and answer)
                    or (not row["value"]["honest"] and not answer),
                    format_args=dict(),
                    format_style="misc",
                )
    return results
