import argparse
import os
import spotirip as sr
from time import sleep
import multiprocessing as mp
import queue
import spotirip.const as const
import threading

_FINISH = False

recorded_queue = mp.Queue()  # tuple<audio_array, epoch timestamp end of recording>
song_meta_queue = queue.Queue()  # tuple<filename, tags, tuple<epoch timestamp begin, end>>
rec_process_queue = queue.Queue()  # all started recording processes because they are not terminating automatically

remaining_records_to_export = 0


def make_dir(directory):
    try:
        os.mkdir(directory)
    except OSError:
        print("Creation of the directory %s failed" % directory)


def check_exit():
    global _FINISH
    while True:
        if input() == "exit":
            print("\nWait for remaining record...")
            _FINISH = True
            break


def check_new_recordings(directory, mp3):
    global recorded_queue
    global song_meta_queue
    global rec_process_queue

    global remaining_records_to_export

    while not _FINISH:
        while remaining_records_to_export > 0:
            # get both the recording and song metadata
            rec = recorded_queue.get()
            song_meta = song_meta_queue.get()

            # terminate the corresponding recording process because it will not terminate by itself
            rec_process_queue.get().terminate()

            # start exporting
            exp_process = mp.Process(target=sr.exporter.export,
                                     args=(rec[0], directory, song_meta[0], song_meta[1], song_meta[2][0],
                                           song_meta[2][1], rec[1], mp3,))
            exp_process.start()
            remaining_records_to_export -= 1

            print("\nExported: %s" % song_meta[0])
        sleep(1)


def main(immediately, mp3, quality, username, directory):
    make_dir(directory)

    _check_exit = threading.Thread(target=check_exit)
    _check_exit.start()

    _check_new_recordings = threading.Thread(target=check_new_recordings, args=(directory, mp3,))
    _check_new_recordings.start()

    player = sr.spotify.Spotify(sr.const.USERNAME if username is None else username)

    global recorded_queue
    global song_meta_queue
    global rec_process_queue

    global remaining_records_to_export

    if immediately:
        player.reset_playback()
        # TODO stop playback, start recording and after x seconds start playback

    while True:
        remain = player.get_remaining_playback_time()

        # sleep until just before the next song
        sleep(remain / 1000 - const.FORERUN)

        # start recording before next song begins because of latency
        if not _FINISH:
            rec_process = mp.Process(target=sr.recorder.start_recording,
                                     args=(recorded_queue, int(const.MAX_SONG_LENGTH * 1000),))
            rec_process.start()
            rec_process_queue.put(rec_process)
            remaining_records_to_export += 1

        if _FINISH:
            print("\nWait for remaining export...")
            _check_exit.join()
            _check_new_recordings.join()
            break

        # sleep until next song began
        sleep(const.FORERUN * 2)

        # Put currently playing song in song metadata queue
        player.update_current_playback()
        timestamps = player.get_timestamps()
        song_meta_queue.put((player.get_file_name(), player.get_tags(), (timestamps[0], timestamps[1])))
        print("\n\nCurrently Recording: %s\n\n" % player.get_file_name())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--immediately", action="store_true",
                        help="Start recording immediately after successful authorization. This leads to returning "
                             "back to song beginning. If not set, recording will start within the next song.")
    parser.add_argument("-m", "--mp3", action="store_true",
                        help="Export in mp3 format.")
    parser.add_argument("-u", "--username",
                        help="Change the user temporarily for this session as opposed to the constants file.")
    parser.add_argument("-q", "--quality", type=int,
                        help="Set the export quality in Kbit/s temporarily for this session.")
    parser.add_argument("-d", "--directory",
                        help="Set the directory where you want to save the recorded songs. If not "
                             "set it will save the files in the /music subdirectory of spotirip.")
    args = parser.parse_args()

    print("Please ensure that the following conditions are met:"
          "\n\t- Spotify is already playing"
          "\n\t- Normalize volume is activated"
          "\n\t- Crossfading is deactivated"
          "\n\nIf you are sure press enter...")
    input()

    main(args.immediately, args.mp3, args.quality, args.username,
         args.directory if args.directory is not None else "music/")
