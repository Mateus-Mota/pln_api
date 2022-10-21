from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from apps.api.api_v1.deps import get_db
from apps.core.security import get_current_user_is_admin
from apps.crud import accuracy_crud
from apps.schemas import accuracy_schema

router = APIRouter()


@router.post("/",
             status_code=status.HTTP_200_OK,
             response_model=accuracy_schema.AccuracyResponse)
def accuracy(accuracy_resquest: accuracy_schema.Accuracy,
             db: Session = Depends(get_db)):
    """
    Accuracy
    """
    accuracy = accuracy_crud.add_accuracy(db, accuracy_resquest)

    return accuracy


@router.get(
    "/",
    response_model=List[accuracy_schema.AccuracyResponse],
    status_code=status.HTTP_200_OK,
)
def list(limit: int = 10, db: Session = Depends(get_db)):
    """
    Home
    """

    accuracys = accuracy_crud.list_accuracy(db=db, limit=limit)

    if accuracys.count() == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found",
        )
    else:
        return list(accuracys)  # type: ignore
