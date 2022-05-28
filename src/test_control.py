"""
Test file for control.py
------------------------
"""
from unittest.mock import MagicMock
from unittest.mock import patch
from control import MyGUI

gui = MyGUI("test window")


@patch("tkinter.ttk")
@patch("threading.Thread")
def test_tkinter(mock_tk: MagicMock, mock_thread):
    """Testing that the tkinter module is called"""
    gui.click()
    gui.__init__("test")
    mock_tk.assert_called()
