from sqlalchemy import String, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column

Base = declarative_base()


class Items(Base):
    __tablename__ = 'items'

    itemid: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    itemname: Mapped[str] = mapped_column(String(100), unique=True)
    itemdesc: Mapped[str] = mapped_column(String(1000))
