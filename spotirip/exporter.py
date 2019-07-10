import spotirip.const as const
import pydub as pd
import numpy as np
from math import sqrt


def _convert(audio_array):
    x = np.int16(audio_array * 2 ** 15)
    return pd.AudioSegment(x.tobytes(), frame_rate=const.FRAMERATE, sample_width=2, channels=2)


def _cut(audio_array, start_timestamp, end_timestamp, rec_end_timestamp):
    start_frame = int(((start_timestamp - rec_end_timestamp) - const.DELTA) * const.FRAMERATE)
    end_frame = int(((end_timestamp - rec_end_timestamp) + const.DELTA * 2) * const.FRAMERATE)

    audio_array_cut = audio_array[start_frame:end_frame]

    i = 0
    # search for first occurrence when sound is played (after previous song)
    while True:
        # check if sound is not played for at least const.GAMMA time
        i2 = i
        while abs(audio_array_cut[i2][0] * 2 ** 15) < const.OMEGA and abs(audio_array_cut[i2][1] * 2 ** 15) < const.OMEGA:
            i2 += 1

        if i2 - i > const.GAMMA * const.FRAMERATE or i > const.DELTA * const.FRAMERATE * 2:
            i = i2
            break

        i += 1

    j = len(audio_array_cut) - 1
    # search for first occurrence when sound is played (from the back)
    while True:
        # check if sound is not played for at least const.GAMMA time
        j2 = j
        while abs(audio_array_cut[j2][0] * 2 ** 15) < const.OMEGA and abs(audio_array_cut[j2][1] * 2 ** 15) < const.OMEGA:
            j2 -= 1

        if j - j2 > const.GAMMA * const.FRAMERATE or len(audio_array_cut) - j > const.DELTA * const.FRAMERATE * 2:
            j = j2
            break

        j -= 1

    return audio_array_cut[i:j]


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
