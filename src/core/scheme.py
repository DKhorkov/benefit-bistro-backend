from pydantic import BaseModel


class HTMLContextScheme(BaseModel):
    """
    Scheme of context of HTML templates for rendering in Objects-Relating Style.
    """

    title: str
