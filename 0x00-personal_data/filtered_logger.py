#!/usr/bin/env python3
"""Regex-ing module"""

import re
from typing import List
import logging
from logging import StreamHandler
import mysql.connector
import os


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.msg, self.SEPARATOR)
        return super().format(record)


PII_FIELDS = ("name", "email", "password", "ssn", "phone")


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Returns a connector to the MySQL database"""
    db_connect = mysql.connector.connect(
        user=os.getenv('PERSONAL_DATA_DB_USERNAME') or 'root',
        password=os.getenv('PERSONAL_DATA_DB_PASSWORD') or '',
        host=os.getenv('PERSONAL_DATA_DB_HOST') or 'localhost',
        database=os.getenv('PERSONAL_DATA_DB_NAME')
    )
    return db_connect


def get_logger() -> logging.Logger:
    """Returns a logger object named 'user_data'"""
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)

    handler = StreamHandler()

    formatter = RedactingFormatter(PII_FIELDS)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """Obfuscates specified fields in a log message"""
    for field in fields:
        message = re.sub(field+'=.*?'+separator,
                         field+'='+redaction+separator, message)
    return message


def main():
    """main function"""
    db = get_db()
    logger = get_logger()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    fields = cursor.column_names
    for row in cursor:
        message = "".join("{}={}; ".format(k, v) for k, v in zip(fields, row))
        logger.info(message.strip())
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
