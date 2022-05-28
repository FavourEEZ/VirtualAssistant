"""
Azure
=====
A class that handles all the interactions with the
Azure API
"""
from conf import AZURE_API_SUBSCRIPTION_KEY
from conf import AZURE_REGION
import requests
import logging
logging.basicConfig(level=logging.DEBUG)


class Azure:
    """Azure contains a method that converts a sound/command) to text.
     The class has another method that turns text to sound"""
    def __init__(self) -> None:
        """Azure contructor sets the environment variables needed
        for the program to run"""
        self.__subscription_key = AZURE_API_SUBSCRIPTION_KEY
        self.__region = AZURE_REGION

    # This method takes an audio file as a parameter and sends it to azure
    def speech_to_text(self, sound_as_binary):
        """Sends the API request to convert speech to text.
        It expects sound as a wav file and returns the response object,
        which contains the text in: response["content"]["DisplayText"]."""
        url = f'https://{self.__region}.stt.speech.microsoft.com/'\
            'speech/recognition/conversation/cognitiveservices/v1'
        params = {"language": "en-GB"}
        headers = {
            "Content-Type": "audio/wav",
            "Accept": "application/json;text/xml",
            "Ocp-Apim-Subscription-Key": self.__subscription_key,
        }
        try:
            response = requests.post(url=url, params=params,
                                     data=sound_as_binary, headers=headers)
        # Raises this excepting if there is an error with the API call to Azure
        except Exception as e:
            msg = f"""An error occured during an API call to stt:
            Please check your env variables/network connection---> {str(e)}"""
            logging.error(msg)
            quit()

        if response:  # pragma: no cover
            response = response.json()
            recognition = response["RecognitionStatus"]
            if recognition == "Success":
                text = response["DisplayText"]
                logging.info(text)
                return text
            elif recognition == "InitialSilenceTimeout":
                print("\n"*3)
                logging.info("Please speak")
                return "empty"
            else:
                print("\n"*3)
                logging.warning(f"""An unexptected issue occured|
                RecognitionStatus: {recognition}""")
                return "empty"

        print("\n"*3)
        logging.warning(
            "An unexptected issue occured! --------------Please try again")
        return "empty"

    def text_to_speech(self, message):
        """This method handles the api call to azure for text to speech"""

        # url to the endpoint that will perform our text to speech request
        url = f'https://{self.__region}.tts.speech.microsoft.com'\
            '/cognitiveservices/v1'
        headers = {
            'Ocp-Apim-Subscription-Key': self.__subscription_key,
            'Content-Type': 'application/ssml+xml',
            'X-Microsoft-OutputFormat': 'riff-16khz-16bit-mono-pcm'
        }
        v = "en-US-ChristopherNeural"

        # Data to be sent as part of the request.
        data = f"""
        <speak version='1.0' xml:lang='en-US'>
        <voice xml:lang='en-US' xml:gender='Male' name='{v}'>{message}</voice>
        </speak>"""

        # Send our request to the voice api and save the result in response
        response = requests.post(url, data=data, headers=headers)
        print(response)

        # Requests returns binary content in response.content
        # saving the converted audio to a file
        with open("output.wav", "wb") as out:
            out.write(response.content)
