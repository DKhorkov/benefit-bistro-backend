import pytest

from tests.config import FakeUserConfig
from src.users.domain.models import UserModel


@pytest.mark.anyio
async def test_user_model_can_protect_password() -> None:
    user: UserModel = UserModel(**FakeUserConfig().to_dict(to_lower=True))
    assert len(user.password) != 0
    await user.protect_password()
    assert len(user.password) == 0
