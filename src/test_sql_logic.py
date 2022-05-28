"""
Test file for sql_logic.py
--------------------------
"""
from sql_logic import Database
from unittest.mock import MagicMock
from unittest.mock import patch


@patch("sqlite3.connect")
def test_play_from_db(mock_db: MagicMock):
    """Testing to make sure the sqlite module is called"""
    db = Database()
    db.play_from_db("loud noise")
    mock_db.assert_called()
