#!/usr/bin/env python3
"""Regex-ing module"""

import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """Obfuscates specified fields in a log message"""
    return re.sub(r'({})'.format('|'.join(fields)), redaction, message)
