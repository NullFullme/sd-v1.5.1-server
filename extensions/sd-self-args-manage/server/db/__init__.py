from pathlib import Path
from sqlalchemy import create_engine, inspect, text, String, Text

from .base import Base, metadata, db_file
from .app_state import AppStateKey, AppState, AppStateManager
from .style import Style, StyleManager

version = "1"

state_manager = AppStateManager()
style_manager = StyleManager()


def init():
    engine = create_engine(f"sqlite:///{db_file}")

    metadata.create_all(engine)

    state_manager.set_value(AppStateKey.Version, version)
    # check if app state exists
    if state_manager.get_value(AppStateKey.QueueState) is None:
        # create app state
        state_manager.set_value(AppStateKey.QueueState, "running")

    inspector = inspect(engine)
    with engine.connect() as conn:
        style_columns = inspector.get_columns("style")
        # add style_name column
        if not any(col["name"] == "style_name" for col in style_columns):
            conn.execute(text("ALTER TABLE style ADD COLUMN style_name VARCHAR(64)"))
        # add prompt_text column
        if not any(col["name"] == "prompt_text" for col in style_columns):
            conn.execute(text("ALTER TABLE style ADD COLUMN prompt_text TEXT"))
        # add negative_prompt_text column
        if not any(col["name"] == "negative_prompt_text" for col in style_columns):
            conn.execute(text("ALTER TABLE style ADD COLUMN negative_prompt_text TEXT"))
        

        conn.close()


__all__ = [
    "init",
    "Base",
    "metadata",
    "db_file",
    "AppStateKey",
    "AppState",
    "Style",
    "state_manager",
    "style_manager"
]
