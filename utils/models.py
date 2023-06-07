from sqlalchemy import Column, BIGINT, BOOLEAN, ForeignKey, TIMESTAMP, SMALLINT

from .database import Base


class User(Base):
    id = Column(BIGINT, primary_key=True)
    is_blocked = Column(BOOLEAN, default=False)
    balance = Column(SMALLINT, default=0)


class UserReservation(Base):
    user_id = Column(BIGINT, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    date_reservation = Column(TIMESTAMP, nullable=False)
    number_of_quests = Column(SMALLINT, nullable=False, default=1)
