from pydantic import BaseModel


class HTMLContextScheme(BaseModel):
    """
    Scheme of HTML context for rendering HTML templates in Objects-Relating Style.
    """

    title: str
