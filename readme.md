## Dependencies
- Python 3.7+
- [Spotipy](https://github.com/plamere/spotipy) (© 2014 Paul Lamere)
- [SoundCard](https://github.com/bastibe/SoundCard) (© 2016 Bastian Bechtold)
- [pydub](https://github.com/jiaaro/pydub) (© 2011 James Robert)

## Getting Started
- Download this repository as [zip](https://github.com/bttger/spotirip/archive/master.zip) or clone it locally
- Download ffmpeg or libav (as described in the [pydub doc](https://github.com/jiaaro/pydub#dependencies))
- Install the dependencies

```
$ pip install spotipy SoundCard pydub
```

- Get yourself the spotify api access on their developer site
- Add a generic app in your developer dashboard
- Get the client_id and whitelist the redirect url (localhost is recommended)
- Paste your details in the [const.py](spotirip/const.py)

```python
spotirip/const.py

USERNAME = "myUserName"
CLIENT_ID = "aLotOfNumbersAndCharacters"
CLIENT_SECRET = "aLotOfNumbersAndCharacters"
REDIRECT_URL = "http://localhost/"
```

- Run [list_cards.py](list_cards.py) to choose the soundcard id and override it in the constants file
- Start Spotify, play music and then run spotirip

```
$ py main.py -h

usage: main.py [-h] [-i] [-m] [-u USERNAME] [-q QUALITY] [-d DIRECTORY]

optional arguments:
  -h, --help            show this help message and exit
  -i, --immediately     Start recording immediately after successful
                        authorization. This leads to returning back to song
                        beginning. If not set, recording will start within the
                        next song.
  -m, --mp3             Export in mp3 format.
  -u USERNAME, --username USERNAME
                        Change the user temporarily for this session as
                        opposed to the constants file.
  -q QUALITY, --quality QUALITY
                        Set the export quality in Kbit/s temporarily for this
                        session.
  -d DIRECTORY, --directory DIRECTORY
                        Set the directory where you want to save the recorded
                        songs. If not set it will save the files in the /music
                        subdirectory of spotirip.
```

- To exit spotirip type ```exit``` in your console and spotirip will just record the current playing song and
terminate after exporting it

## Disclaimer
This software is for educational purposes only. No responsibility is held or accepted for misuse.