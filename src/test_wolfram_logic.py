"""
Test file for wolfram_logic.py
------------------------------
"""
from wolfram_logic import Wolfram
from unittest.mock import MagicMock
from unittest.mock import patch


@patch("requests.get")
def test_call_wolfram(mock_get: MagicMock):
    """Testing to ensure the wolfram API is called"""
    wolfram = Wolfram()
    query = "What is the time"
    wolfram.call_wolfram(query)
    mock_get.assert_called()
