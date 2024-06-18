import tinydb
from fastapi import APIRouter, Depends, Query

from di import get_db
from enums import ResponseType
from schemas import SortedList, SortedListReturn

router = APIRouter()


@router.post(
    "/add",
    response_model=SortedList,
    summary="Add item to sorted list",
    tags=["lists"],
)
def save_list(sorted_list: SortedList, db: tinydb.TinyDB = Depends(get_db)):
    """Route for saving sorted list into database"""
    T = tinydb.Query()
    already_exists = (
        db.get(
            (T.items == sorted_list.items)
            or (T.sorted_items == sorted_list.sorted_items)
        )
        is not None
    )
    if already_exists:
        return SortedList(
            items=sorted_list.items, sorted_items=sorted_list.sorted_items
        )
    db.insert(
        {"items": sorted_list.items, "sorted_items": sorted_list.sorted_items}
    )
    return sorted_list


@router.get(
    "/get",
    response_model=SortedListReturn,
    summary="Get sorted list",
    tags=["lists"],
)
def get_list(
    find_list: list[float] = Query(
        ...,
        min_length=2,
        max_length=10,
        description="List to sort",
        example=[1, 2, 3],
    ),
    db: tinydb.TinyDB = Depends(get_db),
):
    """Route for getting sorted list from database"""
    T = tinydb.Query()
    result = db.get(T.items == find_list)

    if result is None:
        sorted_list = sorted(find_list)
        db.insert({"items": find_list, "sorted_items": sorted_list})
        sorted_list = SortedList(items=find_list, sorted_items=sorted_list)
        return SortedListReturn(
            items=sorted_list.items,
            sorted_items=sorted_list.sorted_items,
            mode=ResponseType.CALCULATED,
        )

    return SortedListReturn(
        items=result["items"],
        sorted_items=result["sorted_items"],
        mode=ResponseType.FOUND,
    )
