"""
Test file for record_play.py
----------------------------
"""
from record_play import IO
from unittest.mock import MagicMock
from unittest.mock import patch


@patch("pyaudio.PyAudio")
@patch("wave.open")
def test_record(mock_audio: MagicMock, mock_wave: MagicMock):
    """Testing to ensure the record audio method is called"""
    io = IO()
    io.record("mock")
    mock_wave.assert_called()


@patch("pyaudio.PyAudio")
@patch("wave.open")
def test_play(mock_audio: MagicMock, mock_wave: MagicMock):
    """Testing the play audio method"""
    io = IO()
    io.play("mock")
    mock_audio.assert_called_once()
