USERNAME = "myUserName"
CLIENT_ID = "aLotOfNumbersAndCharacters"
CLIENT_SECRET = "aLotOfNumbersAndCharacters"
REDIRECT_URL = "http://localhost/"

SOUNDCARD_ID = "{0.0.0.00000000}.{e4f0594c-5e6f-436d-ab0e-4ecaf7f8djf7d8}"

# only for mp3 exports
BITRATE = 320

# implementation relevant constants, because starting the recording has some latency
FRAMERATE = 44100
FORERUN = 4  # in seconds
DELTA = 2  # in seconds, expanding the recorded frame
GAMMA = 0.05  # in seconds, the threshold for recognizing the gap between two songs
OMEGA = 40  # threshold for maximum volume level in gap between two songs
MAX_SONG_LENGTH = 600  # in seconds, maximum length of recorded songs
