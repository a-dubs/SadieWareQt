from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_classes import *
from db_managers import *

# Create the database engine
engine = create_engine("postgresql+psycopg2://postgres:letmein@localhost:5555/dev_sadieware_db")

# Create the tables
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()
