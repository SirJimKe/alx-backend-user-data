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
        super().__init__()  # Corrected super() call
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.msg, self.SEPARATOR)  # Used imported filter_datum
        return super().format(record)


PII_FIELDS = ("name", "email", "password", "ssn", "phone")


def get_db() -> mysql.connector.MySQLConnection:
    """Returns a connector to the MySQL database"""
    db_connect = mysql.connector.connect(
        user=os.getenv('PERSONAL_DATA_DB_USERNAME', 'root'),
        password=os.getenv('PERSONAL_DATA_DB_PASSWORD', ''),
        host=os.getenv('PERSONAL_DATA_DB_HOST', 'localhost'),
        database=os.getenv('PERSONAL_DATA_DB_NAME')
    )
    return db_connect


def get_logger() -> logging.Logger:
    """Returns a logger object named 'user_data'"""
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)

    handler = StreamHandler()
    formatter = RedactingFormatter(fields=list(PII_FIELDS))
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False

    return logger


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """Obfuscates specified fields in a log message"""
    for field in fields:
        message = re.sub(fr'{field}\s*=\s*(.*?){separator}',
                         f'{field}={redaction}{separator}', message)
    return message
