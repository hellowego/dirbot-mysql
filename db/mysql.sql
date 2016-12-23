DROP TABLE IF EXISTS website;
CREATE TABLE website (
  guid CHAR(32) PRIMARY KEY,
  name TEXT,
  description TEXT,
  url TEXT,
  updated DATETIME
) DEFAULT CHARSET=utf8;

DROP TABLE if EXISTS investor;
CREATE TABLE investor (
  guid CHAR(32) PRIMARY KEY,
  name VARCHAR (100),
  name_abbr VARCHAR (50),
  city VARCHAR (20),
  status TINYINT DEFAULT 1,
  company_desc TEXT,
  introduce TEXT,
  detail_url VARCHAR (100),
  img_url VARCHAR (100),
  img_name VARCHAR (100),
  img_location VARCHAR (100),
  add_time DATETIME  DEFAULT NOW(),
  update_time DATETIME  DEFAULT NOW()
)DEFAULT CHARSET=utf8;

DROP TABLE if EXISTS investor_tem;
CREATE TABLE investor_tem (
  guid CHAR(32) PRIMARY KEY,
  name VARCHAR (100),
  name_abbr VARCHAR (50),
  city VARCHAR (20),
  status TINYINT DEFAULT 1,
  company_desc TEXT,
  introduce TEXT,
  detail_url VARCHAR (100),
  img_url VARCHAR (100),
  img_name VARCHAR (100),
  img_location VARCHAR (100),
  add_time DATETIME  DEFAULT NOW(),
  update_time DATETIME  DEFAULT NOW()
)DEFAULT CHARSET=utf8;

