########## Modules ##########
import json, uuid, random, string, datetime
from types import SimpleNamespace

from fastapi import Request

########## Read Json body ##########
async def read_json_body(request: Request):
    try:
        body = await request.body()
        data = json.loads(body)
        obj = SimpleNamespace(**data)
        return obj, None
    except json.JSONDecodeError:
        return None, "Invalid Json"

########## Validate required fields  ##########
def validate_required_fields(data: dict, fields: list):
    required_fields = []

    for field in fields:
        if not hasattr(data, field):
            required_fields.append({"field": field, "message": field + " is required"})
        else:
            value = getattr(data, field)
            if not isinstance(value, str) or value.strip() == "":
                required_fields.append({"field": field, "message": field + " is required"})
    
    if len(required_fields) > 0:
        return required_fields, True

    return None, False
