import pytest
from jinja2 import Template, TemplateNotFound

from src.celery.utils import get_email_template
from src.celery.config import PathsConfig


def test_get_email_template_success() -> None:
    template: Template = get_email_template(path=PathsConfig.VERIFY_EMAIL)
    assert template.name == PathsConfig.VERIFY_EMAIL


def test_get_email_template_fail() -> None:
    with pytest.raises(TemplateNotFound):
        get_email_template(path='non existing path to template')
