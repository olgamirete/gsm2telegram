python3 -c'from utils.sim800l_helpers import send_command;send_command("ATA")'
aplay test_sounds/harp.wav -D plughw:1,0
# arecord sample.wav --format S16_LE --rate 44100 -d 5 --vumeter=stereo -D plughw:1,0
arecord recordings/sample.wav -r 44100 -f S16_LE -d 5 --vumeter=mono -D plughw:1,0 -c1
python3 upload_recording.py