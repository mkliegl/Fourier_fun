#! /usr/bin/env bash

# Usage: ./music.sh [SECONDS]

SECONDS=${1:-5}
sox Carefree.mp3 song1.wav trim 0 $SECONDS
sox Gymnopedie\ No\ 2.mp3 song2.wav trim 0 $SECONDS

for WINDOW_SIZE in 0064 1024 4096 ; do
    # ../swap_wav_mag_phase.py $WINDOW_SIZE \
    #     song1.wav song2.wav \
    #     song1_phase_${WINDOW_SIZE}.wav \
    #     song2_phase_${WINDOW_SIZE}.wav
    ../swap_wav_mag_phase_stft.py $WINDOW_SIZE \
        song1.wav song2.wav \
        song1_phase_${WINDOW_SIZE}_stft.wav \
        song2_phase_${WINDOW_SIZE}_stft.wav
done

for file in *.wav ; do
    sox "$file" "${file%.wav}.ogg"
done
