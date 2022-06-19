from dataclasses import dataclass


@dataclass
class DBConfig:
    host: str
    port: int
    user: str
    dbname: str
    password: str


DefaultConfig = DBConfig("db", 5432, "postgres", "postgres", "123456")
CloudConfig = DBConfig("mydatabase-instance.czsr2ijvkrza.us-east-1.rds.amazonaws.com", 
                      5432, "postgres", "postgres", "Nangua1208")
