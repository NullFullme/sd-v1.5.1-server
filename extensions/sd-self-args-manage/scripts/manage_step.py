import gradio as gr
from fastapi import FastAPI

from modules import script_callbacks
from server.db import init as init_db
from server.api import regsiter_apis

init_db()

def on_app_started(_: gr.Blocks, app: FastAPI) -> None:
    # 第一个参数是SD-WebUI传进来的gr.Blocks，但是不需要使用
    regsiter_apis(app)
    
script_callbacks.on_app_started(on_app_started)