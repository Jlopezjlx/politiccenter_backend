import tempfile

import pytest
import unittest
import sys

sys.path.append('./')

from api import create_app


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # create a temporary file to isolate the database for each test
    # create the app with common test config
    app = create_app()
    app.config['WTF_CSRF_ENABLED'] = False
    yield app


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()

