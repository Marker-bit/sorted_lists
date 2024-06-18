from pydantic import BaseModel, Field, model_validator
from typing_extensions import Self

from enums import ResponseType


class SortedList(BaseModel):
    items: list[float] = Field(
        ...,
        min_length=2,
        max_length=10,
        example=[2, 1, 3],
        description="List to sort",
    )
    sorted_items: list[float] = Field(
        ...,
        min_length=2,
        max_length=10,
        example=[1, 2, 3],
        description="Sorted list",
    )

    @model_validator(mode="after")
    def verify_arrays(self) -> Self:
        if len(self.items) != len(self.sorted_items):
            raise ValueError("Lengths of items and sorted_items must match")
        for i in self.items:
            if i not in self.sorted_items:
                raise ValueError(f"{i} is not in sorted_items")
        for i in self.sorted_items:
            if i not in self.items:
                raise ValueError(f"{i} is not in items")
        for i in range(len(self.sorted_items) - 1):
            if self.sorted_items[i] > self.sorted_items[i + 1]:
                raise ValueError("sorted_items must be strictly increasing")

        return self


class SortedListReturn(SortedList):
    mode: ResponseType = Field(..., description="Mode of response")
