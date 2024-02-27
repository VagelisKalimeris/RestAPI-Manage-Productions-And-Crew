from sqlalchemy import Column, ForeignKey, Integer, String, Date, CheckConstraint
from sqlalchemy import engine # noqa
from .sqlite_db import Base


class ProdCrew(Base):
    __tablename__ = 'prod_crew'

    # Note: SQLite by default ignores the following foreign key constraints
    prod_id = Column(Integer, ForeignKey('production.id'), primary_key=True)
    crew_id = Column(Integer, ForeignKey('crew.id'), primary_key=True)


class Production(Base):
    __tablename__ = 'production'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    start = Column(Date, index=True)
    end = Column(Date, CheckConstraint('end >= start'), index=True)


class Crew(Base):
    __tablename__ = 'crew'

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    role = Column(String, index=True)
    hire_date = Column(Date, index=True)
    fire_date = Column(Date, CheckConstraint('fire_date > hire_date'), index=True)
