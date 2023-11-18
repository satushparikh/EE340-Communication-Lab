#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# Author: osboxes
# GNU Radio version: 3.10.3.0

from packaging.version import Version as StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import analog
from gnuradio import blocks
import pmt
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore



from gnuradio import qtgui

class Lab6_Task1(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "Lab6_Task1")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 4300000
        self.interferer_amplitude = interferer_amplitude = 1e-2
        self.gain_signal = gain_signal = 0.001

        ##################################################
        # Blocks
        ##################################################
        self._interferer_amplitude_range = Range(1e-2, 1, 1e-2, 1e-2, 200)
        self._interferer_amplitude_win = RangeWidget(self._interferer_amplitude_range, self.set_interferer_amplitude, "'interferer_amplitude'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._interferer_amplitude_win)
        self.qtgui_sink_x_1 = qtgui.sink_f(
            1024, #fftsize
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            True, #plotfreq
            True, #plotwaterfall
            True, #plottime
            True, #plotconst
            None # parent
        )
        self.qtgui_sink_x_1.set_update_time(1.0/10)
        self._qtgui_sink_x_1_win = sip.wrapinstance(self.qtgui_sink_x_1.qwidget(), Qt.QWidget)

        self.qtgui_sink_x_1.enable_rf_freq(False)

        self.top_layout.addWidget(self._qtgui_sink_x_1_win)
        self.blocks_transcendental_0 = blocks.transcendental('tanh', "float")
        self.blocks_throttle_0_0 = blocks.throttle(gr.sizeof_float*1, samp_rate,True)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_float*1, samp_rate,True)
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_ff(gain_signal)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(20)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_float*1, '/media/sf_EE_340/Lab6/Input.bin', True, 0, 0)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_add_xx_0 = blocks.add_vff(1)
        self.analog_sig_source_x_0 = analog.sig_source_f(samp_rate, analog.GR_COS_WAVE, 430000, interferer_amplitude, 0, 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_file_source_0, 0), (self.blocks_throttle_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_transcendental_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.qtgui_sink_x_1, 0))
        self.connect((self.blocks_throttle_0_0, 0), (self.blocks_multiply_const_vxx_0_0, 0))
        self.connect((self.blocks_transcendental_0, 0), (self.blocks_throttle_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "Lab6_Task1")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        self.blocks_throttle_0_0.set_sample_rate(self.samp_rate)
        self.qtgui_sink_x_1.set_frequency_range(0, self.samp_rate)

    def get_interferer_amplitude(self):
        return self.interferer_amplitude

    def set_interferer_amplitude(self, interferer_amplitude):
        self.interferer_amplitude = interferer_amplitude
        self.analog_sig_source_x_0.set_amplitude(self.interferer_amplitude)

    def get_gain_signal(self):
        return self.gain_signal

    def set_gain_signal(self, gain_signal):
        self.gain_signal = gain_signal
        self.blocks_multiply_const_vxx_0_0.set_k(self.gain_signal)




def main(top_block_cls=Lab6_Task1, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
