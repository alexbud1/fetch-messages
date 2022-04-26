from sqlalchemy import create_engine, MetaData, Table, Column, BigInteger, Date,  Integer, String, Boolean ,DateTime
from sqlalchemy.orm import declarative_base, registry, sessionmaker

engine = create_engine('', echo=True)

Base = declarative_base()

########################################################################
class QuickNews(Base):
    """"""
    __tablename__ = 'main_quicknews'
    # __table_args__ = {'autoload':True}
    id = Column(Integer, primary_key = True, autoincrement=True)
    text = Column(String, nullable = True)
    time = Column(String, nullable = True)
    creation_time = Column(DateTime)

    def __init__(self, text, time, creation_time):
        self.text = text
        self.time = time
        self.creation_time = creation_time


Base.metadata.create_all(engine)
