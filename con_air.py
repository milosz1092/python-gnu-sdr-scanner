#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Airband
# Generated: Wed Sep 21 08:54:42 2016
##################################################
#my comment
from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from optparse import OptionParser

from grc_gnuradio import wxgui as grc_wxgui
import wx


import os
import osmosdr
from threading import Thread # This is the right package name
from threading import Event
import time


class airband_console(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self)
        _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Variables
        ##################################################
        self.base_freq = base_freq = 121250000
        self.t = 0
        self.volume_min = 0.001
        self.volume = volume = self.volume_min
        self.volume_max = 0.6
        self.squelch = squelch = -26
        self.samp_rate = samp_rate = 2400000
        self.freq_corr = freq_corr = 31
        self.freq = freq = base_freq
        self.frq_choices = [121250000, 121500000, 122200000, 123450000, 124175000, 124925000, 125450000, 130875000, 132700000, 134225000, 134925000, 136050000, 136575000, 169000000]
        # EPSD Port 122700000      EP Przelotowa 124500000      Air-To-Air 2 136975000
        #self.frq_choices = [134225000]
        self.frq_labels = ['EPSC TWR', 'EP EMRG', 'EPSD Kwadrat', 'Air-To-Air', 'Mueritz EDWW Radar', 'B FIR Warszawa', 'EPWW Radar 2', 'EPWW Radar 3', 'EPWW Radar 4', 'D FIR Warszawa', 'EPWW Radar', 'Mark EDWW Radar', 'E FIR Warszawa', 'Lotnicze Pogotowie Ratunkowe']
        #self.frq_labels = ['D FIR Warszawa']
        self.j = 0

        ##################################################
        # Blocks
        ##################################################
        
        self.rtlsdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + "" )
        self.rtlsdr_source_0.set_sample_rate(samp_rate)
        self.rtlsdr_source_0.set_center_freq(freq, 0)
        self.rtlsdr_source_0.set_freq_corr(freq_corr, 0)
        self.rtlsdr_source_0.set_dc_offset_mode(0, 0)
        self.rtlsdr_source_0.set_iq_balance_mode(2, 0)
        self.rtlsdr_source_0.set_gain_mode(False, 0)
        self.rtlsdr_source_0.set_gain(49.6, 0)
        self.rtlsdr_source_0.set_if_gain(1, 0)
        self.rtlsdr_source_0.set_bb_gain(1, 0)
        self.rtlsdr_source_0.set_antenna("RX", 0)
        self.rtlsdr_source_0.set_bandwidth(0, 0)
          
        self.signal_probe = blocks.probe_signal_c()
        #self.signal_probe = analog.probe_avg_mag_sqrd_c(0, 1)
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(50, (firdes.low_pass_2(1,samp_rate,25e3,10e3,40)), 0, samp_rate)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vff((volume, ))
        self.audio_sink_0 = audio.sink(48000, "hw:0,1", True)
        self.analog_pwr_squelch_xx_0 = analog.pwr_squelch_cc(squelch, 0.1, 0, False)
        self.analog_am_demod_cf_0 = analog.am_demod_cf(
        	channel_rate=48000,
        	audio_decim=1,
        	audio_pass=5000,
        	audio_stop=5500,
        )
        self.analog_agc2_xx_0 = analog.agc2_cc(1e-1, 0.1e-4, 1.0, 0)
        self.analog_agc2_xx_0.set_max_gain(5)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.audio_sink_0, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))
        self.connect((self.analog_am_demod_cf_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.analog_agc2_xx_0, 0), (self.analog_am_demod_cf_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.analog_pwr_squelch_xx_0, 0))
        self.connect((self.analog_pwr_squelch_xx_0, 0), (self.signal_probe, 0))
        self.connect((self.analog_pwr_squelch_xx_0, 0), (self.analog_agc2_xx_0, 0))

    def get_base_freq(self):
        return self.base_freq

    def set_base_freq(self, base_freq):
        self.base_freq = base_freq
        self.set_freq(self.base_freq)

    def get_volume(self):
        return self.volume

    def set_volume(self, volume):
        self.volume = volume
        self.blocks_multiply_const_vxx_0.set_k((self.volume, ))

    def get_squelch(self):
        return self.squelch

    def set_squelch(self, squelch):
        self.squelch = squelch
        self.analog_pwr_squelch_xx_0.set_threshold(self.squelch)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.freq_xlating_fir_filter_xxx_0.set_taps((firdes.low_pass_2(1,self.samp_rate,25e3,10e3,40)))
        self.rtlsdr_source_0.set_sample_rate(self.samp_rate)

    def get_freq_corr(self):
        return self.freq_corr

    def set_freq_corr(self, freq_corr):
        self.freq_corr = freq_corr
        self.rtlsdr_source_0.set_freq_corr(self.freq_corr, 0)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.rtlsdr_source_0.set_center_freq(freq, 0)
        self.freq = freq
        

    def print_panel(self): 
        sys.stdout.flush()
        sys.stdout.write("\r Current freq: %i" % tb.get_freq() )
        sys.stdout.flush()

tb = airband_console()


class MyThread(Thread):
    def __init__(self, event):
        Thread.__init__(self)
        self.stopped = event
    def run(self):
        while not self.stopped.wait(0.0):
            
            tb.set_freq(tb.frq_choices[tb.j])
            self.stopped.wait(0.15)
            probe = tb.signal_probe.level()
            
            if probe != complex(0):
                tb.set_volume(tb.volume_max)
                print ""
                print "Signal on: " + tb.frq_labels[tb.j] + " [" + str(tb.get_freq()/1000000.0) + "]"

                while (1):
                    self.stopped.wait(2.0)
                    
                    probe = tb.signal_probe.level()
                    if probe == complex(0):
                        signal = 3
                        while (1):
                            self.stopped.wait(0.2)
                            probe = tb.signal_probe.level()
                            if probe == complex(0):
                                signal = signal - 1

                            if signal == 0:
                                break
                        probe = tb.signal_probe.level()

                        if probe == complex(0):
                            tb.set_volume(tb.volume_min)
                            print "\nSCANING..."
                            break

            if tb.j + 1 >= len(tb.frq_choices):
                tb.j = 0
            else:
                tb.j = tb.j + 1



stopFlag = Event()
thread = MyThread(stopFlag)
thread.start()
print "SCANING..."
# this will stop the timer
#stopFlag.set()


if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads() 
        except:
            print "Warning: failed to XInitThreads()"
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    # new comment  dsfnj  sdfkjdn  
    tb.Start(True) 
    tb.Wait()
