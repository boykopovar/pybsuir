from dataclasses import fields, is_dataclass
from datetime import datetime
from typing import Type, get_origin, get_args, Any, Dict
from typing import Optional, TypeVar, List, Union

T = TypeVar("T")



def dict_to_dataclass(data: dict, cls: Type[T]) -> T:
    if not is_dataclass(cls):
        raise ValueError(f"{cls} is not a dataclass")

    field_types = {f.name: f.type for f in fields(cls)}
    kwargs = {}

    for key, value in data.items():
        if value is None:
            kwargs[key] = None
            continue

        field_type = field_types.get(key)
        if not field_type:
            continue

        if is_dataclass(field_type):
            kwargs[key] = dict_to_dataclass(value, field_type)
            continue

        if _handle_list_field(field_type, value, kwargs, key):
            continue

        if _is_optional(field_type):
            sub_type = get_args(field_type)[0]
            if isinstance(value, str) and (sub_type is datetime or sub_type == datetime):
                kwargs[key] = _str_iso_to_datetime(value)
            elif is_dataclass(sub_type) and isinstance(value, dict):
                kwargs[key] = dict_to_dataclass(value, sub_type)
            else:
                kwargs[key] = value
            continue

        if field_type is datetime and isinstance(value, str):
            kwargs[key] = _str_iso_to_datetime(value)
        else:
            kwargs[key] = value

    return cls(**kwargs)

def _str_iso_to_datetime(s: str) -> Optional[datetime]:
    try:
        return datetime.fromisoformat(s.replace('Z', '+00:00'))
    except ValueError:
        chunks = s.split('.')
        if len(chunks) != 3:
            raise

        return datetime(int(chunks[2]), int(chunks[1]), int(chunks[0]))

def _handle_list_field(field_type: Any, value: Any, kwargs: Dict[str, Any], key: str) -> bool:
    origin = get_origin(field_type)
    if origin not in (list, List):
        return False

    args = get_args(field_type)
    if len(args) > 0 and is_dataclass(args[0]) and isinstance(value, list):
        kwargs[key] = [dict_to_dataclass(item, args[0]) for item in value if isinstance(item, dict)]
    else:
        kwargs[key] = value
    return True

def _is_optional(field_type: Any) -> bool:
    origin = get_origin(field_type)
    return origin is Union and type(None) in get_args(field_type)