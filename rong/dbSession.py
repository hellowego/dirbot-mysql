#!/usr/bin/env python
#-*- coding: UTF-8 -*- 
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

BaseModel = declarative_base()

engine = create_engine('mysql://root:root@localhost:3306/rong',connect_args={'charset':'utf8'}, pool_size=20, max_overflow=0)
DBSession = sessionmaker(bind=engine)


if __name__ == "__main__":
	print 'hi'