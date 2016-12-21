#!/usr/bin/env python
#-*- coding: UTF-8 -*-

from dbSession import BaseModel, DBSession
from sqlalchemy import Column, String, Integer

from sqlalchemy.dialects.mysql import \
    BIGINT, BINARY, BIT, BLOB, BOOLEAN, CHAR, DATE, \
    DATETIME, DECIMAL, DECIMAL, DOUBLE, ENUM, FLOAT, INTEGER, \
    LONGBLOB, LONGTEXT, MEDIUMBLOB, MEDIUMINT, MEDIUMTEXT, NCHAR, \
    NUMERIC, NVARCHAR, REAL, SET, SMALLINT, TEXT, TIME, TIMESTAMP, \
    TINYBLOB, TINYINT, TINYTEXT, VARBINARY, VARCHAR, YEAR

class InvestorModel(BaseModel):
    """
    Investor model
    """
    __tablename__ = "Investor"

    guid = Column(String(30), primary_key = True, nullable = False)	# guid
    name = Column(String(100), nullable = True)
    name_abbr = Column(String(20), nullable = True)
    city = Column(String(20), nullable = True)
    status = Column(TINYINT, nullable = True)
    company_desc = Column(TEXT, nullable = False)
    introduce = Column(TEXT, nullable = False)
    detail_url = Column(String(100), nullable = True)
    img_url = Column(String(100), nullable = True)
    img_name = Column(String(100), nullable = True)
    img_location = Column(String(100), nullable = True)
    add_time  = Column(DATETIME, nullable = False)
    update_time  = Column(DATETIME, nullable = False)