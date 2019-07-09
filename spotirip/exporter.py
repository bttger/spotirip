import spotirip.const as const
import pydub as pd
import numpy as np


def _convert(audio_array):
    x = np.int16(audio_array * 2 ** 15)
    return pd.AudioSegment(x.tobytes(), frame_rate=const.FRAMERATE, sample_width=2, channels=2)


def _cut(audio_array, start_timestamp, end_timestamp, rec_end_timestamp):
    start_frame = int(((start_timestamp - rec_end_timestamp) + const.DELTA) * const.FRAMERATE)
    end_frame = int(((end_timestamp - rec_end_timestamp) + const.DELTA) * const.FRAMERATE)

    # TODO cut off everything on both sides where no sound
    return audio_array[start_frame:end_frame]


def _export_mp3(audio_segment, directory, filename, tags):
    audio_segment.export("%s%s.mp3" % (directory, filename), format="mp3", bitrate="%dk" % const.BITRATE, tags=tags)
    return


def _export_wav(audio_segment, directory,  filename):
    audio_segment.export("%s%s.wav" % (directory, filename), format="wav")
    return


def export(audio_array, directory, filename, tags, start_timestamp, end_timestamp, rec_end_timestamp, mp3=False):
    audio_segment = _convert(_cut(audio_array, start_timestamp, end_timestamp, rec_end_timestamp))

    if mp3:
        _export_mp3(audio_segment, directory, filename, tags)
    else:
        _export_wav(audio_segment, directory, filename)

    return
