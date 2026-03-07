import os
import subprocess
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]


def _has_db_config() -> bool:
    required = ["DB_HOST", "DB_PORT", "DB_NAME", "DB_USER", "DB_PASSWORD"]
    return all(os.getenv(k) for k in required)


@pytest.mark.integration
def test_migrate_script_runs_when_db_available():
    """
    Smoke-test: database/migrate.py should complete without error
    when a PostgreSQL instance is available and .env is configured.
    """
    if not _has_db_config():
        pytest.skip("Database environment variables are not configured")

    result = subprocess.run(
        [sys.executable, str(ROOT / "database" / "migrate.py")],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"migrate.py failed: {result.stderr}"


@pytest.mark.integration
def test_generate_data_script_runs_when_db_available():
    """
    Smoke-test: ingestion/generate_data.py should complete without error
    when a PostgreSQL instance is available and .env is configured.
    """
    if not _has_db_config():
        pytest.skip("Database environment variables are not configured")

    result = subprocess.run(
        [sys.executable, str(ROOT / "ingestion" / "generate_data.py")],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"generate_data.py failed: {result.stderr}"


@pytest.mark.integration
def test_demand_forecasting_training_runs_when_db_available():
    """
    Smoke-test: ml/demand_forecasting/train.py should complete without error
    when a PostgreSQL instance is available and .env is configured.
    """
    if not _has_db_config():
        pytest.skip("Database environment variables are not configured")

    result = subprocess.run(
        [sys.executable, str(ROOT / "ml" / "demand_forecasting" / "train.py")],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"demand_forecasting/train.py failed: {result.stderr}"


@pytest.mark.integration
def test_churn_prediction_training_runs_when_db_available():
    """
    Smoke-test: ml/churn_prediction/train.py should complete without error
    when a PostgreSQL instance is available and .env is configured.
    """
    if not _has_db_config():
        pytest.skip("Database environment variables are not configured")

    result = subprocess.run(
        [sys.executable, str(ROOT / "ml" / "churn_prediction" / "train.py")],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"churn_prediction/train.py failed: {result.stderr}"

