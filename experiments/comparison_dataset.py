import torch

from repeng.datasets.activations.creation import create_activations_dataset
from repeng.datasets.elk.utils.collections import (
    DatasetCollectionId,
    resolve_dataset_ids,
)
from repeng.datasets.elk.utils.limits import Limits, SplitLimits

"""
18 datasets
 * 20 layers
 * 1 token
 * (400 + 400 + 800) questions
 * 3 answers
 * 5120 hidden dim size
 * 2 bytes
= 17GB
"""

collections: list[DatasetCollectionId] = ["dlk", "repe", "got"]
create_activations_dataset(
    tag="datasets_2024-02-13_v1",
    llm_ids=["Llama-2-13b-chat-hf"],
    dataset_ids=[
        dataset_id
        for collection in collections
        for dataset_id in resolve_dataset_ids(collection)
    ],
    group_limits=Limits(
        default=SplitLimits(
            train=400,
            train_hparams=400,
            validation=800,
        ),
        by_dataset={
            "truthful_qa": SplitLimits(
                train=0,
                train_hparams=0,
                validation=800,
            )
        },
    ),
    num_tokens_from_end=1,
    device=torch.device("cuda"),
    layers_start=1,
    layers_end=None,
    layers_skip=2,
)
