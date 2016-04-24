#! /usr/bin/env python
from __future__ import print_function, division
import sys
import warnings

import numpy as np
from scipy.io import wavfile
from stft import spectrogram, ispectrogram


# Notes on using scipy.io.wavfile:
# 1. The data has shape (n_samples, n_channels). This is compatible with stft.
# 2. The dtype of the data is some integer type. We restore it manually
#    after the inverse STFT.


def wav_to_magnitude_phase(wav, window_size):
    fourier = spectrogram(wav, framelength=window_size)
    magnitude = np.abs(fourier)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        phase = fourier / magnitude
    phase[~np.isfinite(phase)] = 1.0  # when magnitude is zero, set phase to 1
    dtype = wav.dtype
    return magnitude, phase, dtype


def wav_from_magnitude_phase(magnitude, phase, dtype):
    fourier = magnitude * phase
    return ispectrogram(fourier).real.astype(dtype)


def swap_wav_magnitude(a, b, window_size):
    a_magnitude, a_phase, a_dtype = wav_to_magnitude_phase(a, window_size)
    b_magnitude, b_phase, b_dtype = wav_to_magnitude_phase(b, window_size)
    return (
        wav_from_magnitude_phase(b_magnitude, a_phase, a_dtype),
        wav_from_magnitude_phase(a_magnitude, b_phase, a_dtype),
    )


def main(argv):
    if len(argv) == 6:
        window_size = int(argv[1])
        a_fname = argv[2]
        b_fname = argv[3]
        a_phase_b_mag_fname = argv[4]
        b_phase_a_mag_fname = argv[5]
    else:
        print(
            'Usage: %s ' % argv[0] +
            '<WINDOW_WIDTH> <FILE_1> <FILE_2> <OUTFILE_1> <OUTFILE_2>' + (
                '\n\nSwap magnitude and phase of WAV files FILE_1 and FILE_2.'
                '\n\nWINDOW_WIDTH: STFT frame length (integer # of samples)'
                '\nOUTFILE_1: phase of FILE_1, magnitude of FILE_2'
                '\nOUTFILE_2: phase of FILE_2, magnitude of FILE_1'))
        return 1

    a_rate, a = wavfile.read(a_fname)
    b_rate, b = wavfile.read(b_fname)
    assert a_rate == b_rate
    assert a.dtype == b.dtype

    print('Window width: %d samples = %.3f ms' %
          (window_size, 1e3 * window_size / a_rate))

    a_phase_b_mag, b_phase_a_mag = swap_wav_magnitude(a, b, window_size)

    wavfile.write(a_phase_b_mag_fname, a_rate, a_phase_b_mag)
    wavfile.write(b_phase_a_mag_fname, a_rate, b_phase_a_mag)

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
