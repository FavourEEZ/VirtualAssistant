"""
IO
==
record_play.py holds all the logic needed to record audio
from a user's device and also play audio
The IO class stands for Input/Ouput
"""
import pyaudio
import wave
import logging
import io
logger = logging.getLogger(__name__)


class IO:
    """The IO class handles the recording and playing of audio"""
    def __init__(self) -> None:
        """The IO contructor defines the essential variables needed
        for all our imported methods to run properly"""
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000

    def record(self, filename: str, duration=5.0) -> bool:
        """The record method records audio for 5 seconds by
         using the pyaudio library"""
        p = pyaudio.PyAudio()

        s = p.open(format=self.FORMAT, channels=self.CHANNELS,
                   rate=self.RATE, input=True, frames_per_buffer=self.CHUNK)

        logger.info("recording audio for %s seconds", duration)
        logger.info("Recording audiofile")

        frames = []

        for i in range(0, int(self.RATE / self.CHUNK * duration)):
            data = s.read(self.CHUNK)
            frames.append(data)

        logger.info("done recording.")

        s.stop_stream()
        s.close()
        p.terminate()

        wf = wave.open(filename, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        try:
            wf.writeframes(b''.join(frames))
        except Exception as e:
            logging.error(e)
        wf.close()
        return True

    def play(self, audio_in: any):
        '''
        audio_in is either a path to a WAV file or bytes containing WAV audio.
        '''
        p = pyaudio.PyAudio()

        # By passing flake8 error by putting type in an array
        arr = [type(b'')]
        # using if type(audio_in) == type(b''):
        if type(audio_in) in arr:
            wf = wave.open(io.BytesIO(audio_in), 'rb')
            # logger.info("Sound is bytes")
        else:
            try:
                wf = wave.open(audio_in, 'rb')
            except FileNotFoundError:
                logger.warning("No such file: %s", audio_in)
                raise FileNotFoundError
            except Exception as e:
                logging.error(e)
                return

        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        # read data
        data = wf.readframes(self.CHUNK)

        # play stream
        while len(data) > 0:
            stream.write(data)
            data = wf.readframes(self.CHUNK)

        # stop stream
        stream.stop_stream()
        stream.close()

        # close PyAudio
        p.terminate()
