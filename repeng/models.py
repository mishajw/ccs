from typing import Literal

from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    GPT2LMHeadModel,
    GPTNeoXForCausalLM,
    LlamaForCausalLM,
    PreTrainedTokenizerFast,
)

from repeng.hooks.points import Point, TupleTensorExtractor


def gpt2() -> (
    tuple[GPT2LMHeadModel, PreTrainedTokenizerFast, list[Point[GPT2LMHeadModel]]]
):
    model = AutoModelForCausalLM.from_pretrained("gpt2")
    tokenizer = AutoTokenizer.from_pretrained("gpt2")
    assert isinstance(tokenizer, PreTrainedTokenizerFast)
    return (
        model,
        tokenizer,
        [
            Point(
                f"h{i}",
                lambda model: model.transformer.h[i],
                tensor_extractor=TupleTensorExtractor(0),
            )
            for i in range(11)
        ],
    )


def pythia(
    size: Literal["70m", "160m", "410m", "1b", "1.4b", "2.8b", "6.9b", "12b"]
) -> tuple[
    GPTNeoXForCausalLM, PreTrainedTokenizerFast, list[Point[GPTNeoXForCausalLM]]
]:
    model = GPTNeoXForCausalLM.from_pretrained(
        f"EleutherAI/pythia-{size}",
        revision="step3000",
    )
    assert isinstance(model, GPTNeoXForCausalLM)
    tokenizer = AutoTokenizer.from_pretrained(
        f"EleutherAI/pythia-{size}",
        revision="step3000",
    )
    assert isinstance(tokenizer, PreTrainedTokenizerFast)
    return (
        model,
        tokenizer,
        [
            Point(
                f"h{i}",
                lambda model: model.gpt_neox.layers[i],
                tensor_extractor=TupleTensorExtractor(0),
            )
            for i in range(len(model.gpt_neox.layers))
        ],
    )


def llama2_13b(
    size: Literal["7b", "13b", "70b"],
    *,
    chat: bool,
) -> tuple[LlamaForCausalLM, PreTrainedTokenizerFast, list[Point[LlamaForCausalLM]]]:
    if chat:
        model_str = f"meta-llama/Llama-2-{size}-chat-hf"
    else:
        model_str = f"meta-llama/Llama-2-{size}-hf"
    model = AutoModelForCausalLM.from_pretrained(model_str)
    assert isinstance(model, LlamaForCausalLM)
    tokenizer = AutoTokenizer.from_pretrained(model_str)
    assert isinstance(tokenizer, PreTrainedTokenizerFast)
    return (
        model,
        tokenizer,
        [
            Point(
                f"h{i}",
                lambda model: model.model.layers[i],
                tensor_extractor=TupleTensorExtractor(0),
            )
            for i in range(len(model.model.layers))
        ],
    )
