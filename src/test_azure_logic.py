"""
Test file for azure_logic.py
----------------------------
"""
from unittest.mock import MagicMock
from unittest.mock import patch
from azure_logic import Azure

azure = Azure()


@patch("requests.get")
def test_stt(mock_req: MagicMock):
    """Testing to ensure that the Speech to Text API is called"""
    azure.speech_to_text("mock")
    mock_req.assert_not_called()


@patch("requests.get")
def test_tts(mock_req: MagicMock):
    """Testing to ensure that the Text to Speecjh API is called"""
    azure.text_to_speech("mock")
    mock_req.assert_not_called()
