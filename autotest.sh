python -c'from utils.sim800l_helpers import send_command;send_command("ATA")'
cd test_sounds
aplay harp.wav
cd ..
cd recordings
arecord sample.wav --format S16_LE --rate 44100 -d 5 --vumeter=stereo -D plughw:1,0
cd ..
python upload_recording.py