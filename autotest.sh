python3 -c'from utils.sim800l_helpers import send_command;send_command("ATA")'
# aplay test_sounds/harp.wav -D plughw:1,0
# arecord sample.wav --format S16_LE --rate 44100 -d 5 --vumeter=stereo -D plughw:1,0
echo 'will begin recording...'
arecord sample.wav -f cd -d 5 -D plughw:1,0
echo 'will begin playing...'
aplay sample.wav -D plughw:1,0
# python3 upload_recording.py