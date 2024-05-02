from dataclasses import dataclass, asdict
from typing import Optional, Any, Dict, List


@dataclass(frozen=True)
class BaseModel:

    async def to_dict(
            self,
            exclude: Optional[List[str]] = None,
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


@dataclass
class UserModel(BaseModel):
    email: str
    password: str
    username: str

    # Optional args:
    id: Optional[int] = None
    email_confirmed: bool = False
