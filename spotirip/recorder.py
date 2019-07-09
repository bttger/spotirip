import spotirip.const as const
import soundcard as sc
import time


def start_recording(recorded_queue, ms):
    audio_array = sc.get_microphone(const.SOUNDCARD_ID, include_loopback=True).record(
        numframes=int(const.FRAMERATE * ms / 1000),
        samplerate=int(const.FRAMERATE))

    recorded_queue.put((audio_array, time.time()))
    recorded_queue.close()
    return
