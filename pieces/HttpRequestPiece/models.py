from pydantic import BaseModel, Field, field_validator
from enum import Enum
from typing import List
import re


class MethodTypes(str, Enum):
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'


class InputModel(BaseModel):
    url: List[str] = Field(
        description="URL(s) to make requests to. Multiple URLs may be separated by commas, semicolons, or whitespace."
    )

    @field_validator('url', mode='before')
    @classmethod
    def split_delimited_string(cls, v):
        if isinstance(v, str):
            return [u.strip() for u in re.split(r'[\s,;]+', v) if u.strip()]
        if isinstance(v, list) and len(v) == 1 and isinstance(v[0], str):
            parts = [u.strip() for u in re.split(r'[\s,;]+', v[0]) if u.strip()]
            if len(parts) > 1:
                return parts
        return v
    method: MethodTypes = Field(
        default=MethodTypes.GET,
        description="HTTP method to use."
    )
    bearer_token: str = Field(
        default=None,
        description="Bearer token to use for authentication."
    )
    body_json_data: str = Field(
        default="""{
    "key_1": "value_1",
    "key_2": "value_2"
}
""",
        description="JSON data to send in the request body.",
        json_schema_extra={
            'widget': "codeeditor-json",
        }
    )


class OutputModel(BaseModel):
    base64_bytes_data: List[str] = Field(
        description='Output data as list of base64 encoded strings, one per input URL. Empty string for failed URLs.'
    )
