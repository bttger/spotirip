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
        self._current_playback = self._client.current_playback()

    def get_remaining_playback_time(self):
        return self._current_playback["item"]["duration_ms"] - self._current_playback["progress_ms"]

    def reset_playback(self):
        self._client.seek_track(0)
        #self._client.pause_playback()

    def get_tags(self):
        artists = ""
        for artist in self._current_playback["item"]["artists"]:
            artists += artist["name"] + ", "

        return {"artist": artists[:-2], "title": self._current_playback["item"]["name"],
                "album": self._current_playback["item"]["album"]["name"]}

    def get_file_name(self):
        return "%s - %s" % (self.get_tags()["artist"], self.get_tags()["title"])

    def get_timestamps(self):
        start_timestamp = (self._current_playback["timestamp"] - self._current_playback["progress_ms"]) / 1000
        end_timestamp = (self._current_playback["timestamp"] + self._current_playback["item"]["duration_ms"]) / 1000

        return start_timestamp, end_timestamp
