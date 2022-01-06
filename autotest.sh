cd recordings
sudo arecord sample.wav -c1 --vumeter=mono -d 5 --device=hw:1,0 --format S16_LE --rate 44100
cd ..
python upload_recording.py