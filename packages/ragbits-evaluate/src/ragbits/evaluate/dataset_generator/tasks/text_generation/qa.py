from typing import Any

from distilabel.llms.base import LLM

from ...utils import get_closest_substring, get_passages_list
from .base import BaseDistilabelTask


class QueryGenTask(BaseDistilabelTask):
    """
    A task for generating a question based on a provided text chunk.
    """

    def __init__(self, llm: LLM, prompt_class: str):
        super().__init__(llm=llm, inputs=["chunk"], outputs=["question", "chunk"], prompt_class=prompt_class)

    def format_output(self, output: str, input: dict[str, Any] | None = None) -> dict[str, str | list[str]]:  # noqa: PLR6301
        """
        Formats the generated question into a structured dictionary with the original "chunk" input.

        Args:
            output: The generated question.
            input: Optional; contains "chunk" key with the original input chunk.

        Returns:
            A dictionary containing "chunk" and "question".
        """
        return {"chunk": input["chunk"], "question": output}  # type: ignore


class PassagesGenTask(BaseDistilabelTask):
    """
    A task for generating passages related to a specific question and answer from a text chunk.
    """

    should_get_matches: bool = False

    def __init__(self, llm: LLM, prompt_class: str):
        super().__init__(
            llm=llm,
            inputs=["chunk", "question", "basic_answer"],
            outputs=["question", "chunk", "passages"],
            prompt_class=prompt_class,
        )

    def format_output(self, output: str, input: dict[str, Any] | None = None) -> dict[str, str | list[str]]:
        """
        Formats the model's output into a structured dictionary with "question", "chunk", and "passages".
        If `get_matches` is `True`, attempts to find the closest matches for each passage within the
        provided chunk.

        Args:
            output: The raw output generated by the text generation model.
            input: Required if `get_matches` is `True`, containing "chunk" and "question".

        Returns:
            A dictionary with "chunk", "question", and a list of "passages".
        """
        passages: list[str] = get_passages_list(output) or []

        if self.should_get_matches:
            matched_passages: list[str] = []

            for passage in passages:
                if passage in input["chunk"]:  # type: ignore
                    matched_passages.append(passage)
                else:
                    matched_passage = get_closest_substring(input["chunk"], passage)  # type: ignore
                    matched_passages.append(matched_passage)

            return {"chunk": input["chunk"], "question": input["question"], "passages": matched_passages}  # type: ignore

        return {"chunk": input["chunk"], "question": input["question"], "passages": passages}  # type: ignore


class AnswerGenTask(BaseDistilabelTask):
    """
    A task for generating basic answers to questions based on a provided text chunk. This class extends
    the `TextGeneration` task from the `distilabel` package.
    """

    def __init__(self, llm: LLM, prompt_class: str):
        super().__init__(llm=llm, inputs=["chunk", "question"], outputs=["basic_answer"], prompt_class=prompt_class)

    def format_output(self, output: str, input: dict[str, Any] | None = None) -> dict[str, str | list[str]]:  # noqa: PLR6301
        """
        Formats the model's output into a structured dictionary with the "basic_answer" key.

        Args:
            output: The raw output generated by the text generation model.
            input: Optional; not typically used in this formatting.

        Returns:
            A dictionary with "basic_answer" as the key and the generated output as its value.
        """
        return {"basic_answer": output}
