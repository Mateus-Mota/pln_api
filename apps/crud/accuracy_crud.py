from email import message

from sqlalchemy.orm import Session

from apps.models.accuracy_models import AccuracyModel
from apps.pln.accuracy import accuracy_predict
from apps.schemas import accuracy_schema
from apps.schemas.accuracy_schema import AccuracyResponse
from apps.services.translate_message import translate


def add_accuracy(db: Session, accuracy_data: accuracy_schema.Accuracy):
    """
    Save accuracy
    """

    if accuracy_data.translate:
        message = translate(accuracy_data.message)
        accuracy = accuracy_predict(text=message)
    else:
        message = accuracy_data.message
        accuracy = accuracy_predict(text=message)

    if not accuracy_data.save:
        AccuracyResponse.message = message
        AccuracyResponse.accuracy = accuracy

        return AccuracyResponse
    else:
        db_accuracy = AccuracyModel(accuracy=accuracy, message=message)
        db.add(db_accuracy)
        db.commit()
        db.refresh(db_accuracy)
        return db_accuracy


def list_accuracy(db: Session, limit: int):
    return db.query(AccuracyModel).filter().limit(limit)
