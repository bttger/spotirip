import argparse
import spotirip as sr
from time import sleep
import multiprocessing as mp


def main(immediately, mp3, quality, username, directory):
    player = sr.spotify.Spotify(sr.const.USERNAME if username is None else username)
    rec_queue = mp.Queue()
    tags = player.get_tags()
    filename = player.get_file_name()

    if immediately:
        player.reset_playback()
    else:
        sleep(player.get_remaining_playback_time() / 60 - sr.const.MEAN_RESP_TIME / 1000)

    remain = player.get_remaining_playback_time()

    rec_process = mp.Process(target=sr.recorder.start_recording, args=(rec_queue, 10000,))
    print("start rec_process")
    rec_process.start()
    print("wait rec_process")
    sleep(2)

    exp_process = mp.Process(target=sr.exporter.export_mp3, args=(rec_queue.get(), directory, filename, tags,))
    print("start exp_process")
    exp_process.start()
    print("wait exp_process")



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

    # TODO sicherstellen dass spotify music läuft
    # TODO create music/

    main(args.immediately, args.mp3, args.quality, args.username,
         args.directory if args.directory is not None else "music/")
