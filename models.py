from sqlalchemy.sql.expression import null
from database import Base
from sqlalchemy import String,Boolean,Integer,Column,Text


class complexity(Base):
    __tablename__='complexity'
    complexity_id=Column(Integer,primary_key=True)
    uppercase=Column(Integer,nullable=False)
    lowercase = Column(Integer, nullable=False)
    symbols = Column(Integer, nullable=False)
    numbers = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<Uppercase={self.uppercase} Lowercase={self.lowercase} Symbols={self.symbols} Numbers={self.numbers}>"