"""
Wolfram
=======
A class that handles all the interactions with the
wolfram API
"""
from conf import APP_NAME
from conf import APPID
import requests
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class Wolfram:
    """*Wolfram class contains a constructor and a method
    to call the wolfram API*"""
    def __init__(self) -> None:
        """Wolfram constructor sets the environment variables needed
        for the program to run"""
        self.APP_NAME = APP_NAME
        self.APPID = APPID
        self.output = ""

    def call_wolfram(self, query):
        """This method makes the api call and performs error handling."""
        print(query)
        q_url = f"http://api.wolframalpha.com/v2/query?" \
                f"appid={self.APPID}" \
                f"&input={query}" \
                f"&format=plaintext" \
                f"&output=json"
        try:
            response = requests.get(q_url).json()
        except Exception as e:
            logger.error(f"An error occured during the API call: {e}")
            self.output = "Unfortunately, an error occured "
            return self.output

        if not response["queryresult"]["success"]:  # pragma: no cover
            # if response["queryresult"]["success"] == False:
            logger.info("Please try again")
            logger.debug("Querying wolfram was unsuccessful")

            try:
                if response["queryresult"]["didyoumeans"]["level"] == "low":
                    self.output = "Sorry, I didn't quite get your question"
                    return self.output
            except Exception as e:
                logger.debug(e)
            self.output = """Sorry, I didn't quite get that.
            Please try asking another question"""
            return self.output

        data = response["queryresult"]["pods"][1]["subpods"][0]
        plaintext = data["plaintext"]

        if plaintext == "":
            logger.info("Return string was empty")
            self.output = "I don't know that but I'm always learning"
            return self.output
        print("*"*30, plaintext)
        return plaintext
