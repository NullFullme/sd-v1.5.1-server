import io
import os
import json
import requests
import threading
from uuid import uuid4
from zipfile import ZipFile
from pathlib import Path
from typing import Optional, Dict, List
from gradio.routes import App

from pydantic import BaseModel



from .db import Style, style_manager
from .models import (
    StyleModel,
    StyleManagerResponse,
)
from .logging import log, request_with_retry


def regsiter_apis(app: App):
    log.info("[self-args-manage] Registering APIs")

    @app.get(
        "/sdapi/custom/style_list", 
        # response_model=StyleManagerResponse
    )
    def get_style(limit: int = -1, offset: int = -1):
        style_list =  style_manager.get_style_list(
            limit=limit, offset=offset
        )
        # print("style_list", style_list)
        return {"success": True, "data": StyleManagerResponse(StyleList=style_list)}

    class SetStyleReq(BaseModel):
        style_name: str
        prompt_text: str
        negative_prompt_text: str

    @app.post(
        "/sdapi/custom/style_add",
        # response_model=StyleManagerResponse
    )
    def set_style(req: SetStyleReq):
        while True:
            id = str(uuid4())
            # print(id)
            if style_manager.get_style(id) is None:
                style = style_manager.add_style(Style(id=id, style_name=req.style_name, prompt_text=req.prompt_text, negative_prompt_text=req.negative_prompt_text))
                # return {"success": True, "message": "Task requeued"}
                return {"success": True, "data": style}

    @app.post(
        "/sdapi/custom/style_edit",
        # response_model=StyleManagerResponse
    )
    def edit_style(style: Style):
        style = style_manager.update_style(style)
        return {"success": True, "data": style}
    
    class DelStyleReq(BaseModel):
        style_id: str

    @app.delete("/sdapi/custom/style_del")
    def delete_style(req: DelStyleReq):
        style_manager.delete_style(req.style_id)
        return {"success": True, "message": "Style deleted"}

