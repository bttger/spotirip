## Dependencies
- Python 3.7+
- [Spotipy]() (© 2014 Paul Lamere)
- [SoundCard]() (© 2016 Bastian Bechtold)
- [pydub](https://github.com/jiaaro/pydub) (© 2011 James Robert)

## Getting Started
- Download this repository as [zip](linkhere) or clone it locally
- Install the dependencies

```bash
pip install spotipy ....
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

