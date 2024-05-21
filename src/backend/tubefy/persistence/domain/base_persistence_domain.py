from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase


class BasePersistenceDomain(AsyncAttrs, DeclarativeBase):

    pass
