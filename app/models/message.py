from .base_model import BaseModel
from ..db_storage import db


class MESSAGE(BaseModel):
    __tablename__ = "message"
    sender_id = db.Column(db.String(300), nullable=False)
    content = db.Column(db.Text, nullable=False)
    recipient_id = db.Column(db.String(300), nullable=False)