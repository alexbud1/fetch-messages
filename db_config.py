from sqlalchemy import create_engine, MetaData, Table, Column, BigInteger, Date,  Integer, String, Boolean ,DateTime
from sqlalchemy.orm import declarative_base, registry, sessionmaker

engine = create_engine('postgresql://zyjydzupswlfrc:f308076f28f531f352d49eaf6394045ceaa58205891e7e3f4414f3e49ae52d7c@ec2-52-212-228-71.eu-west-1.compute.amazonaws.com/d5vdm7bq7rbg8d', echo=True)

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
