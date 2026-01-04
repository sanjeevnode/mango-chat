from sqlalchemy import Column, Integer, DateTime, ForeignKey, UniqueConstraint
from datetime import datetime, timezone
from app.services.database import Base


class UserChannel(Base):
    __tablename__ = "user_channels"

    id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )

    channel_id = Column(
        Integer,
        ForeignKey("channels.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )   

    __table_args__ = (
        UniqueConstraint("user_id", "channel_id", name="uq_user_channel"),
    )
