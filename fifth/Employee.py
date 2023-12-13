from sqlalchemy import Column, Integer, String, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()

class Employee(Base):
    __tablename__ = 'employee'
    __table_args__ = (UniqueConstraint('name', 'position', 'department', 'birthday', 'number'),)

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    position = Column(String(250), nullable=False)
    department = Column(String(250), nullable=False)
    birthday = Column(String(250), nullable=False)
    number = Column(String(250), nullable=False)

engine = create_engine('sqlite:///employees.db', echo=True)
Base.metadata.create_all(engine)
