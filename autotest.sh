python -c'import sim800L_helpers;sim800L_helpers.send_command("ATA")'
cd recordings
sudo arecord sample.wav --format S16_LE --rate 44100 -d 5 --vumeter=stereo
cd ..
python upload_recording.py
