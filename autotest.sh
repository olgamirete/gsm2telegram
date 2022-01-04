cd recordings
sudo arecord --device=hw:1,0 --format S16_LE --rate 44100 -c1 sample.wav --vumeter=mono -d 5
cd ..
python upload_recording.py