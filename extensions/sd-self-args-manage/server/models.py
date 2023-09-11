from typing import List, Optional
from pydantic import BaseModel, Field



class StyleModel(BaseModel):
    id: str = Field(title="Style Id")
    style_name: str = Field(titles="Style Name")
    prompt_text: Optional[str] = Field(titles="Style Prompt Text")
    negative_prompt_text: Optional[str] = Field(titles="Style Negative Prompt Text")

class StyleManagerResponse(BaseModel):
    StyleList: List[StyleModel] = Field(titles="Style List")

