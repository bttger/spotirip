import spotirip.const as const
import pydub as pd
import numpy as np


def _convert(audio_array):
    x = np.int16(audio_array * 2 ** 15)
    return pd.AudioSegment(x.tobytes(), frame_rate=const.FRAMERATE, sample_width=2, channels=2)


def export_mp3(audio_array, directory, filename, tags):
    print("exporting")
    song = _convert(audio_array)
    song.export("%s%s.mp3" % (directory, filename), format="mp3", bitrate="%dk" % const.BITRATE, tags=tags)  # TODO tags
    return


def export_wav(audio_array, directory,  filename):
    song = _convert(audio_array)
    song.export("%s%s.wav" % (directory, filename), format="wav")
    return
