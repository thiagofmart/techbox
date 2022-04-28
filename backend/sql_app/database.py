from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json
import pydantic.json


def _custom_json_serializer(*args, **kwargs) -> str:
    """
    Encodes json in the same way that pydantic does.
    """
    return json.dumps(*args, default=pydantic.json.pydantic_encoder, **kwargs)

engine = create_engine("sqlite:///./sql_app/test.db", connect_args={"check_same_thread": False}, json_serializer=_custom_json_serializer)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()
