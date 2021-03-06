#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
@author: Felipe Espic

DESCRIPTION:
This script extracts high resolution acoustic parameters from a wave file.
Then, it resynthesises the signal from these features.
Features:
- m_mag:  Magnitude Spectrum  (dim=fft_len/2+1, usually 2049)
- m_real: Normalised real "R" (dim=fft_len/2+1, usually 2049)
- m_imag: Normalised imag "I" (dim=fft_len/2+1, usually 2049)
- v_f0:   F0 (dim=1)

INSTRUCTIONS:
This demo should work out of the box. Just run it by typing: python <script name>
If wanted, you can modify the input options and/or perform some modification to the
extracted features before re-synthesis. See the main function below for details.
"""

import sys, os
curr_dir = os.getcwd()
sys.path.append(os.path.realpath(curr_dir + '/../src'))

import libutils as lu
import libaudio as la
from libplot import lp
import magphase as mp

def analysis(wav_file, fft_len):
    est_file = lu.ins_pid('temp.est')
    la.reaper(wav_file_orig, est_file)
    m_mag, m_real, m_imag, v_shift, v_voi, m_frm, fs = mp.analysis_with_del_comp__ph_enc__f0_norm__from_files_raw(wav_file, est_file, fft_len)
    v_f0 = mp.shift_to_f0(v_shift, v_voi, fs, out='f0', b_smooth=True)
    os.remove(est_file)
    return m_mag, m_real, m_imag, v_f0

def synthesis(m_mag, m_real, m_imag, v_f0, fs):
    v_syn_sig = mp.synthesis_wit_del_comp_from_raw_params(m_mag, m_real, m_imag, v_f0, fs)
    return v_syn_sig

def plots(m_mag, m_real, m_imag, v_f0):
    lp.plotm(la.db(m_mag)) # in decibels for better visualisation
    lp.title('Magnitude Spectrum (dB)')
    lp.xlabel('Time (frames)')
    lp.ylabel('Frequency bins')

    lp.plotm(m_real)
    lp.title('"R" Feature Phase Spectrum')
    lp.xlabel('Time (frames)')
    lp.ylabel('Frequency bins')

    lp.plotm(m_imag)
    lp.title('"I" Feature Phase Spectrum')
    lp.xlabel('Time (frames)')
    lp.ylabel('Frequency bins')

    lp.figure()
    lp.plot(v_f0)
    lp.title('F0')
    lp.xlabel('Time (frames)')
    lp.ylabel('F0')
    lp.grid()
    return


if __name__ == '__main__':  
    # CONSTANTS: So far, the vocoder has been tested only with the following constants:
    fft_len = 4096
    fs      = 48000

    # INPUT:==============================================================================
    wav_file_orig = 'data/wavs_nat/hvd_577.wav' # Original natural waveform. You can choose any of the provided ones in the /wavs_nat directory.
    out_dir       = 'data/wavs_syn' # Where the synthesised waveform will be stored

    b_plots       = True # True if you want to plot the extracted parameters.

    # PROCESS:============================================================================
    lu.mkdir(out_dir)

    # ANALYSIS:
    print("Analysing.....................................................")
    m_mag, m_real, m_imag, v_f0 = analysis(wav_file_orig, fft_len)

    # MODIFICATIONS:
    # If wanted, you can do modifications to the parameters here.

    # SYNTHESIS:
    print("Synthesising.................................................")
    v_syn_sig = synthesis(m_mag, m_real, m_imag, v_f0, fs)

    # SAVE WAV FILE:
    print("Saving wav file..............................................")
    wav_file_syn = out_dir + '/' + lu.get_filename(wav_file_orig) + '_copy_syn_high_res.wav'
    la.write_audio_file(wav_file_syn, v_syn_sig, fs)

    # PLOTS:===============================================================================
    if b_plots:
        plots(m_mag, m_real, m_imag, v_f0)
        raw_input("Press Enter to close de figs and finish...")
        lp.close('all')

    print('Done!')







