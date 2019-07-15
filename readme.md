# Spotirip
#### The Spotify Ripper - records your streamed music, exports it to wav or mp3 and tags it automatically

## Dependencies
- Python 3.7+
- [Spotipy](https://github.com/plamere/spotipy) (© 2014 Paul Lamere)
- [SoundCard](https://github.com/bastibe/SoundCard) (© 2016 Bastian Bechtold)
- [pydub](https://github.com/jiaaro/pydub) (© 2011 James Robert)

## Getting Started
- Download this repository as [zip](https://github.com/bttger/spotirip/archive/master.zip) or clone it locally
- Download ffmpeg or libav (as described in the [pydub doc](https://github.com/jiaaro/pydub#dependencies), for exporting to mp3)
- Install the dependencies

```
$ pip install spotipy soundcard pydub
$ pip install git+https://github.com/plamere/spotipy.git --upgrade
```

- Get yourself the spotify api access on their developer site
- Add a generic app in your developer dashboard
- Get the client_id and whitelist the redirect url (localhost is recommended)
- Paste your details in the [const.py](spotirip/const.py)

```python
USERNAME = "myUserName"
CLIENT_ID = "aLotOfNumbersAndCharacters"
CLIENT_SECRET = "aLotOfNumbersAndCharacters"
REDIRECT_URL = "http://localhost/"
```

- Run [list_cards.py](list_cards.py) to choose the soundcard id and override it in the constants file
- Start Spotify, play music and then run spotirip

```
$ py main.py -h
usage: main.py [-h] [-i] [-m] [--min MIN] [--secs SECS] [-u USERNAME]
               [-q QUALITY] [-d DIRECTORY]

optional arguments:
  -h, --help            show this help message and exit
  -i, --immediately     Start recording immediately after successful
                        authorization. This leads to returning back to song
                        beginning. If not set, recording will start within the
                        next song.
  -m, --mp3             Export in mp3 format.
  --min MIN             Set the max song length in minutes temporarily for
                        this session as opposed to the constants file.
  --secs SECS           Set the max song length in seconds temporarily for
                        this session as opposed to the constants file.
  -u USERNAME, --username USERNAME
                        Set the user temporarily for this session as opposed
                        to the constants file.
  -q QUALITY, --quality QUALITY
                        Set the export quality in Kbit/s temporarily for this
                        session.
  -d DIRECTORY, --directory DIRECTORY
                        Set the directory where you want to save the recorded
                        songs. If not set it will save the files in the /music
                        subdirectory of spotirip.

$ py main.py -i -m -min 5
```

- To exit Spotirip type ```exit``` in your console and spotirip will just record the current playing song and
terminate after exporting it

## Tips
A good internet connection is mandatory and I recommend either to turn off your Dropbox/G-Drive Sync or to choose a directory where it is not getting synced all the time. In my case my bad internet connection caused problems and python threw some errors while making HTTP requests to the Spotify API.

Furthermore you should really exit Spotirip with the ```exit``` command and let Spotify continue playing to ensure that the recording gets well finished and exported. This can take some time depending on the ```MAX_SONG_LENGTH``` in the constants file. This constant is necessary because the recoding will start with a delay and therefore we have to start it before the next song actually begins. But since the Spotify API does not give the ability to get the duration of the next song, it is not possible to forward the correct record duration to the recorder (which needs the duration before starting the recording).

Also you must be aware of the memory usage since it is recording the soundcard with by default 44100 frames per second in a numpy array. For a maximum song length of more than like eight minutes you should have a pc with at least eight gigabyte of RAM. The problem is that python allocates memory depending on the total pc RAM and because it does not want to exhaust the total memory, it simply limits the memory usage and throws a memory error exception if the limit is reached.

## Disclaimer
This software is for educational purposes only. No responsibility is held or accepted for misuse.
