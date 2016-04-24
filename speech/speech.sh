#! /usr/bin/env bash

# Usage: ./speech.sh [SECONDS]

SECONDS=${1:-5}
sox AddresstotheWomenofAmerica_64kb.mp3 speech1.wav trim 0 $SECONDS
sox AddresstoCongress-1974_64kb.mp3 speech2.wav trim 0 $SECONDS

for WINDOW_SIZE in 0064 1024 4096 ; do
    # ../swap_wav_mag_phase.py $WINDOW_SIZE \
    #     speech1.wav speech2.wav \
    #     speech1_phase_$WINDOW_SIZE.wav speech2_phase_$WINDOW_SIZE.wav
    ../swap_wav_mag_phase_stft.py $WINDOW_SIZE \
        speech1.wav speech2.wav \
        speech1_phase_${WINDOW_SIZE}_stft.wav \
        speech2_phase_${WINDOW_SIZE}_stft.wav
done

for file in *.wav ; do
    sox "$file" "${file%.wav}.ogg"
done
