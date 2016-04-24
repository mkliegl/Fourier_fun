#! /usr/bin/env python
from __future__ import print_function, division
import sys
import warnings

import numpy as np
from scipy.io import wavfile
from scipy.fftpack import fft, ifft


# Notes:
# 1. `wav` data as obtained from scipy.io.wavfile
#     has shape (n_samples, n_channels); hence we do (inverse) Fourier
#     transforms over the 0th axis
# 2. The dtype of the data is some integer type that will have
#    to be restored by the inverse Fourier transform.


def wav_to_magnitude_phase(wav):
    fourier = fft(wav, axis=0)
    magnitude = np.abs(fourier)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        phase = fourier / magnitude
    phase[~np.isfinite(phase)] = 1.0  # when magnitude is zero, set phase to 1
    dtype = wav.dtype
    return magnitude, phase, dtype


def wav_from_magnitude_phase(magnitude, phase, dtype):
    fourier = magnitude * phase
    return ifft(fourier, axis=0).real.astype(dtype)


def swap_wav_magnitude(a, b, window_size):
    N = min(a.shape[0], b.shape[0])
    N -= (N % window_size)  # make N a multiple of window_size
    b_mag_a_phase = a[:N].copy()
    a_mag_b_phase = b[:N].copy()
    for i in range(0, N, window_size):
        a_magnitude, a_phase, a_dtype = wav_to_magnitude_phase(
            a[i:i + window_size])
        b_magnitude, b_phase, b_dtype = wav_to_magnitude_phase(
            b[i:i + window_size])
        b_mag_a_phase[i:i + window_size] = wav_from_magnitude_phase(
            b_magnitude, a_phase, a_dtype)
        a_mag_b_phase[i:i + window_size] = wav_from_magnitude_phase(
            a_magnitude, b_phase, a_dtype)
    return b_mag_a_phase, a_mag_b_phase


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
                '\n\nWINDOW_WIDTH: number of samples to take the Fourier '
                'transform over'
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
