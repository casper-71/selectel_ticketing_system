from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import (
    Column,
    String,
)
from sqlalchemy.sql.schema import ForeignKey

from src.db.postgresql import Base
from src.models.base_mixins import TimestampMixin, AuditMixin, BaseMixin


class CommentMixin(TimestampMixin, AuditMixin):
    """  """    
    email = Column(String, nullable=False)
    body = Column(String, nullable=False)


class Comment(Base, BaseMixin, CommentMixin):
    """[summary]

    Args:
        Base ([type]): [description]
        BaseMixin ([type]): [description]
        CommentMixin ([type]): [description]

    Returns:
        [type]: [description]
    """    
    ticket_id = Column(UUID(as_uuid=True), ForeignKey("tickets.id"), onupdate="CASCADE")

    def __repr__(self) -> str:
        return f"<Comment {self.id}>"
