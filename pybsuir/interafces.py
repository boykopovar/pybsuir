from dataclasses import asdict, is_dataclass
from datetime import datetime
import json

class IPrintable:
    def _convert_to_serializable(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if is_dataclass(obj):
            return asdict(obj, dict_factory=lambda x: {k: self._convert_to_serializable(v) for k, v in x})
        if isinstance(obj, list):
            return [self._convert_to_serializable(item) for item in obj]
        return obj

    def __str__(self):
        if not is_dataclass(self):
            return super().__str__()
        data = asdict(self, dict_factory=lambda x: {k: self._convert_to_serializable(v) for k, v in x})
        return json.dumps(data, indent=4, ensure_ascii=False)

    def __repr__(self):
        return self.__str__()