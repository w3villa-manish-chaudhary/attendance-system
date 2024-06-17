from pydantic import BaseModel

class ImageData(BaseModel):
    images: list[str]
    username: str
