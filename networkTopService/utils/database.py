from sqlalchemy import create_engine, Column, Integer, DateTime, JSON
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()
DATABASE_URL=os.getenv("DATABASE_URL")
engine=create_engine(DATABASE_URL)
sessionLocal=sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
class Graph(Base):
    __tablename__ = "graphs"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    graph= Column(JSON)

Base.metadata.create_all(bind=engine)
