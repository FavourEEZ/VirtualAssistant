"""
MyGUI
=====
Control.py - The main file.
---------------------------
This file holds the UI, and acts as the control unit of
the program. It handles the program's main operations
by calling other classes and methods and it figures out
what is needed to be done with the data that is returned

*Use it like this*::

    from main import MyGUI
    ui = MyGUI("Virtual Assistant Simulation")
    ui.run()

"""
import logging
import tkinter
from tkinter import ttk
import threading

# Importing our custom classes to handle their individual operation
from record_play import IO
from azure_logic import Azure
from wolfram_logic import Wolfram
from sql_logic import Database
logger = logging.getLogger(__name__)


class MyGUI:
    """This class holds the gui and the code for the main program"""

    def __init__(self, name: str) -> None:
        """
        MyGUI constructor
        :param name: The name of this thing
        :type name: str
        """
        self._colors = ["blue", "green", "cyan"]
        self.modes = ["On/Off", "Listening"]
        self._root = tkinter.Tk()
        self._root.title(name)
        self._root.geometry("700x500")
        self.__style = ttk.Style(self._root)
        self._root.columnconfigure(1, weight=2)
        self._root.rowconfigure(0, weight=2)

        self.btn = ttk.Button(self._root, text="On/Off", command=self.click)
        self.btn.grid(row=0, column=1, padx=120)
        # Set button colour
        self.__style.configure('TButton', background='white')

        ttk.Label(self._root, text="").grid(row=0, column=1, sticky="NWNE")
        ttk.Label(self._root, text="").grid(row=0, column=2, sticky="NWNE")

        ttk.Label(self._root, text="      ").grid(
            row=0, column=0, sticky="NES", rowspan=2)
        ttk.Label(self._root, text="      ").grid(
            row=0, column=3, sticky="NWS", rowspan=2)
        ttk.Label(self._root).grid(row=1, column=1, ipadx=340, columnspan=2)

        self.__style.configure('TLabel', background="white")
        self.mode = "On/Off"

        # Creating an instance of IO from record_play.py
        self.io_controller = IO()
        # Create an instance of Azure
        self.azure = Azure()
        self.db_controller = Database()

    def run(self):
        """This method starts the tkinter mainloop"""
        self._root.mainloop()

    def on_off_mode(self):
        """This method handles the On/Off mode for the Similation"""
        self.mode = "On/Off"
        logger.info("On/Off mode")
        self.__style.configure('TLabel', background="white")
        self._root.update_idletasks()
        self.io_controller.play(".\\goodbye_tune.wav")

    def listening_mode(self):  # pragma: no cover
        """This method handles the listening mode for the Similation"""
        self.mode = "Listening"
        logger.info("Listening mode")
        self.btn["state"] = "normal"
        self.__style.configure('TLabel', background=self._colors[2])
        self._root.update_idletasks()

        command = "empty"
        # while command == "empty" and self.allow_run == True:
        while command == "empty" and self.allow_run:
            self.io_controller.record('voice_command.wav')
            audioFile = open('.\\voice_command.wav', 'rb')
            # Calling speech to text by passing the audio we have just created
            command = self.azure.speech_to_text(audioFile)
            audioFile.close()
            # If command == "empty" don't run the code below
            if command != "empty":
                # make text lower case, then make each char an array element
                # If the first element in the array is play, call sqllite
                if command.lower().split()[0] == "play":
                    self.play_mode(command)
                else:
                    self.answer_mode(command)

    def play_mode(self, command):
        """This method handles the play mode for the simulation
        by calling sql_logic.py"""
        logging.info("Play mode")
        self.btn["state"] = "disabled"
        self.__style.configure('TLabel', background=self._colors[1])
        self._root.update_idletasks()

        if "." in command or "?" in command:
            command = command.replace('.', '')
        self.db_controller.play_from_db(command)
        self.listening_mode()

    def answer_mode(self, command):  # pragma: no cover
        """This method handles the answer mode for the simulation
        by calling wolfram api via wolfram.py"""
        logging.info("Answer mode")
        self.btn["state"] = "disabled"
        self.__style.configure('TLabel', background=self._colors[0])
        self._root.update_idletasks()
        wolfram = Wolfram()
        wolfram_answer = wolfram.call_wolfram(command)
        self.azure.text_to_speech(wolfram_answer)
        self.io_controller.play("output.wav")

        self.listening_mode()

    def click(self):
        """Called when button clicked
        """
        logging.info("Button has been clicked")
        # When in On/Off mode, call listening mode (in a thread)
        if self.mode == "On/Off":
            self.allow_run = True
            self.io_controller.play(".\\hello_tune.wav")
            self.new_thread = threading.Thread(
                target=self.listening_mode, daemon=False).start()
        # Else (in listening mode), go to On/Off mode
        else:
            self.allow_run = False
            logging.debug("""*****************************Stopping the process
            ...........please ignore the following logging messages""")
            self.on_off_mode()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    ui = MyGUI("Virtual Assistant Simulation")
    ui.run()
