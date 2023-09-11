@echo off
chcp 65001
@echo 开始运行
set PYTHON=python\python.exe
set COMMANDLINE_ARGS=--xformers --opt-channelslast --api --api-log --autolaunch --listen --port 7789
set TRANSFORMERS_CACHE=.cache
python\python.exe launch.py
@echo 处理完毕
pause