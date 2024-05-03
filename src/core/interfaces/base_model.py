from dataclasses import dataclass, asdict
from typing import Optional, Any, Dict, Set


@dataclass
class BaseModel:

    async def to_dict(
            self,
            exclude: Optional[Set[str]] = None,
            include: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:

        data: Dict[str, Any] = asdict(self)
        if exclude:
            for key in exclude:
                try:
                    del data[key]
                except KeyError:
                    pass

        if include:
            data.update(include)

        return data
