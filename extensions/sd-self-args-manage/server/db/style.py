from typing import Union, List

from sqlalchemy import (
    Column,
    String,
    Text,
)
from sqlalchemy.orm import Session

from .base import BaseTableManager, Base
from ..models import StyleModel

class Style(StyleModel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    @staticmethod
    def from_table(table: "StyleTable"):
        return Style(
            id=table.id,
            style_name=table.style_name,
            prompt_text=table.prompt_text,
            negative_prompt_text=table.negative_prompt_text,
        )

    def to_table(self):
        return StyleTable(
            id=self.id,
            style_name=self.style_name,
            prompt_text=self.prompt_text,
            negative_prompt_text=self.negative_prompt_text,
        )

class StyleTable(Base):
    __tablename__ = "style"

    id = Column(String(64), primary_key=True)
    style_name = Column(String(64), nullable=False)
    prompt_text = Column(Text, nullable=True)
    negative_prompt_text = Column(Text, nullable=True)

    def __repr__(self):
        return f"Style(id={self.id!r}, style_name={self.style_name!r}, prompt_text={self.prompt_text!r}, negative_prompt_text={self.negative_prompt_text!r})"

class StyleManager(BaseTableManager):
    def get_style(self, id: str) -> Union[StyleTable, None]:
        session = Session(self.engine)
        try:
            style = session.get(StyleTable, id)

            return Style.from_table(style) if style else None
        except Exception as e:
            print(f"Exception getting style from database: {e}")
            raise e
        finally:
            session.close()

    #默认升序asc，若要降序则desc
    def get_style_list(
        self,
        limit: int = None,
        offset: int = None,
        order: str = "asc",
    ) -> List[StyleTable]:
        session = Session(self.engine)
        try:
            query = session.query(StyleTable)

            query = query.order_by(
                StyleTable.id.asc()
                if order == "asc"
                else StyleTable.id.desc()
            )

            if limit and limit != -1:
                query = query.limit(limit)

            if offset and offset != -1:
                query = query.offset(offset)

            all = query.all()
            return [Style.from_table(t) for t in all]
        except Exception as e:
            print(f"Exception getting style list from database: {e}")
            raise e
        finally:
            session.close()
        
    def add_style(self, style: Style) -> StyleTable:
        session = Session(self.engine)
        try:
            item = style.to_table()
            session.add(item)
            session.commit()
            return style
        except Exception as e:
            print(f"Exception adding style to database: {e}")
            raise e
        finally:
            session.close()

    def update_style(self, style: Style) -> StyleTable:
        session = Session(self.engine)
        try:
            current = session.get(StyleTable, style.id)
            if current is None:
                raise Exception(f"Style with id {id} not found")

            session.merge(style.to_table())
            session.commit()
            return style

        except Exception as e:
            print(f"Exception updating style in database: {e}")
            raise e
        finally:
            session.close()
    
    def delete_style(self, id: str):
        session = Session(self.engine)
        try:
            result = session.get(StyleTable, id)
            if result:
                session.delete(result)
                session.commit()
            else:
                raise Exception(f"Style with id {id} not found")
        except Exception as e:
            print(f"Exception deleting style from database: {e}")
            raise e
        finally:
            session.close()
