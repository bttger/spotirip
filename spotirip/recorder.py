import spotirip.const as const
import soundcard as sc


def start_recording(rec_queue, ms):
    audio_array = sc.get_microphone(const.SOUNDCARD_ID, include_loopback=True).record(
        numframes=int(const.FRAMERATE * ms / 1000),
        samplerate=int(const.FRAMERATE), blocksize=500)
    print("recorded")
    rec_queue.put(_cut(audio_array))
    print("put in queue")
    rec_queue.close()
    print("closed queue")
    return


def _cut(audio_array):
    return audio_array
