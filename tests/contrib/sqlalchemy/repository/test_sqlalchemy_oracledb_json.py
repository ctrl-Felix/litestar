"""Unit tests for the SQLAlchemy Repository implementation for psycopg."""
from __future__ import annotations

import platform
import sys

import pytest
from sqlalchemy import Engine
from sqlalchemy.dialects import oracle
from sqlalchemy.schema import CreateTable

from tests.contrib.sqlalchemy.models_uuid import UUIDEventLog

pytestmark = [
    pytest.mark.skipif(sys.platform != "linux", reason="docker not available on this platform"),
    pytest.mark.skipif(platform.uname()[4] != "x86_64", reason="oracle not available on this platform"),
    pytest.mark.sqlalchemy_integration,
]


def test_json_constraint_generation(oracle_engine: Engine) -> None:
    ddl = str(CreateTable(UUIDEventLog.__table__).compile(oracle_engine, dialect=oracle.dialect()))  # type: ignore
    assert "BLOB" in ddl.upper()
    assert "JSON" in ddl.upper()
    with oracle_engine.begin() as conn:
        UUIDEventLog.metadata.create_all(conn)
