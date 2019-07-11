import spotirip.const as const
import spotipy
import spotipy.util as util

scope = "user-read-playback-state user-modify-playback-state"


class Spotify:
    def __init__(self, username):
        self._username = username
        self.token = util.prompt_for_user_token(self._username, scope,
                                                client_id=const.CLIENT_ID,
                                                client_secret=const.CLIENT_SECRET,
                                                redirect_uri=const.REDIRECT_URL)
        self._client = spotipy.Spotify(auth=self.token)

        self._client.trace = True
        self._client.trace_out = True

        self._current_playback = self._client.current_playback()
        self._client.volume(100)
        # self._client.repeat("off") not working when playlist is off and spotify autoplay is activated

    def update_current_playback(self):
        """Updates all information held in the Spotify client, like remaining time, tags and timestamps."""

        self._current_playback = self._client.current_playback()

    def update_access_token(self):
        """Updates the access token to the Spotify API because it will expire after an hour."""
        self.token = util.prompt_for_user_token(self._username, scope,
                                                client_id=const.CLIENT_ID,
                                                client_secret=const.CLIENT_SECRET,
                                                redirect_uri=const.REDIRECT_URL)
        self._client = spotipy.Spotify(auth=self.token)

    def get_remaining_playback_time(self):
        """Returns the remaining playback time in ms."""

        return self._current_playback["item"]["duration_ms"] - self._current_playback["progress_ms"]

    def reset_playback(self):
        """Sets the playback to the song beginning and pauses.\n
        After this, the resume_playback function has to be called manually."""

        self._client.seek_track(0)
        self._client.pause_playback()

    def resume_playback(self):
        # self._client.start_playback(offset={"position": 0})
        self._client.start_playback()

    def get_tags(self):
        """Returns a dictionary with 3 items corresponding to the tags of the current playing song.
        Those tags are the artist (String of all artists), title and album title."""

        artists = ""
        for artist in self._current_playback["item"]["artists"]:
            artists += artist["name"] + ", "

        return {"artist": artists[:-2], "title": self._current_playback["item"]["name"],
                "album": self._current_playback["item"]["album"]["name"]}

    def get_file_name(self):
        """Returns a string with the artist and title of the current playing song, separated by a dash."""

        return "%s - %s" % (self.get_tags()["artist"], self.get_tags()["title"])

    def get_timestamps(self):
        """Returns two timestamps in a tuple.
        First one is the start timestamp of the current playing song. The second one is accordingly for the end."""

        start_timestamp = (self._current_playback["timestamp"] - self._current_playback["progress_ms"]) / 1000
        end_timestamp = (self._current_playback["timestamp"] + self._current_playback["item"]["duration_ms"]) / 1000

        return start_timestamp, end_timestamp
