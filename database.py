from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine=create_engine("mysql+mysqlconnector://root:t44P32LK_1@localhost/pms",
    echo=True
)

Base=declarative_base()

SessionLocal=sessionmaker(bind=engine)