"""
Database
========
*This module handles all the interaction with the Database*

"""
import sqlite3
import logging
from record_play import IO
logging.basicConfig(level=logging.DEBUG)


class Database:
    """Class to handle SQLite operations like playing from a db """
    def __init__(self) -> None:
        """The Database constructor sets the name of the SQLite database"""
        self.name = "sound.db"

    def play_from_db(self, command) -> str:
        """This method runs during play mode.
        It selects the correct sound to run based on the command from user"""
        try:
            self.con = sqlite3.connect(self.name)
            self.cur = self.con.cursor()
        except Exception as e:
            logging.error(f"""An errror occured: {e}
      1. Please make sure you have a database called: sound.db,
      2. It is not currently opened (being used by other programs)
      3. It is in the same directory level as the wav files""")
            quit()

        command = command.lower().split()
        # Play Loud music
        if "music" in command and "loud" in command:
            self.cur.execute('SELECT * FROM clips WHERE kind=? AND volume=?',
                             ("music", "loud"))
            logging.info("Loud music selected")
        # Or if just guitar is in the command
        elif "guitar" in command:
            self.cur.execute('SELECT * FROM clips WHERE name=?',
                             ("guitar_tune.wav",))

        # Play quiet music
        elif "music" in command and "quiet" in command:
            self.cur.execute('SELECT * FROM clips WHERE kind=? AND volume=?',
                             ("music", "quiet"))
            logging.info("Quiet music selected")
        elif "classical" in command:
            self.cur.execute('SELECT * FROM clips WHERE name=?',
                             ("classical_music.wav",))

        # Play Loud Noise
        elif "noise" in command and "loud" in command:
            self.cur.execute('SELECT * FROM clips WHERE kind=? AND volume=?',
                             ("noise", "loud"))
            logging.info("Loud noise selected")
        elif "dog" in command:
            self.cur.execute('SELECT * FROM clips WHERE name=?',
                             ("dog_bark.wav",))

        # Play quiet noise
        elif "noise" in command and "quiet" in command:
            self.cur.execute('SELECT * FROM clips WHERE kind=? AND volume=?',
                             ("noise", "quiet"))
            logging.info("Quiet noise selected")
        elif "door" in command:
            self.cur.execute('SELECT * FROM clips WHERE name=?',
                             ("quiet_door_slam.wav",))

        # If sound can't be found... log the event
        else:
            logging.debug("Sound cannot be found")
            return

        row = self.cur.fetchone()
        self.con.commit()
        self.con.close()
        name, blob = row[0], row[1]
        io_controller = IO()
        io_controller.play(blob)
        logging.info(f"Now Playing: {name}")
        return (row[0], row[1])
