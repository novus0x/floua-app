########## Modules ##########
import enum

from datetime import datetime

from db.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, DateTime, ForeignKey, Enum, Integer, Text, Boolean, Float

##### Wallet #####
class Wallet_Status(enum.Enum):
    active = "active"
    frozen = "frozen"
    closed = "closed"

class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(String, primary_key=True, nullable=False)

    balance_total = Column(Float, default=0.0, nullable=False)
    balance_available = Column(Float, default=0.0, nullable=False)

    status = Column(Enum(Wallet_Status), default=Wallet_Status.active, nullable=False)

    user_id = Column(String, ForeignKey("users.id"), nullable=True)

    updated = Column(DateTime(timezone=True), default=datetime.utcnow)
    date = Column(DateTime(timezone=True), default=datetime.utcnow)

    ## Relationships ##
    user = relationship("User", back_populates="wallet")
    transactions = relationship("Transaction", back_populates="wallet")

##### Transaction #####
class Transaction_Type(enum.Enum):
    donation = "donation"
    withdraw = "withdraw"
    deposit = "deposit"
    transfer = "transfer"
    reward = "reward"

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(String, primary_key=True, nullable=False)
    wallet_id = Column(String, ForeignKey("wallets.id"), nullable=False)

    amount = Column(Float, nullable=False)
    type = Column(Enum(Transaction_Type), nullable=False)

    video_id = Column(String, ForeignKey("videos.id"), nullable=True)
    from_user_id = Column(String, ForeignKey("users.id"), nullable=True)
    to_user_id = Column(String, ForeignKey("users.id"), nullable=True)

    date = Column(DateTime(timezone=True), default=datetime.utcnow)

    ## Relationships ##
    wallet = relationship("Wallet", back_populates="transactions")
    video = relationship("Video", back_populates="transactions")
