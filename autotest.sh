python -c'from utils.sim800l_helpers import send_command;send_command("ATA")'
cd recordings
sudo arecord sample.wav --format S16_LE --rate 44100 -d 5 --vumeter=stereo
cd ..
python upload_recording.py
