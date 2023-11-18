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
from gnuradio import filter
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation



from gnuradio import qtgui

class dsb_fc_SP(gr.top_block, Qt.QWidget):

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

        self.settings = Qt.QSettings("GNU Radio", "dsb_fc_SP")

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
        self.quadrature_rate = quadrature_rate = 960000
        self.audio_rate = audio_rate = 48000

        ##################################################
        # Blocks
        ##################################################
        self.tab = Qt.QTabWidget()
        self.tab_widget_0 = Qt.QWidget()
        self.tab_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tab_widget_0)
        self.tab_grid_layout_0 = Qt.QGridLayout()
        self.tab_layout_0.addLayout(self.tab_grid_layout_0)
        self.tab.addTab(self.tab_widget_0, 'Modulated')
        self.tab_widget_1 = Qt.QWidget()
        self.tab_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tab_widget_1)
        self.tab_grid_layout_1 = Qt.QGridLayout()
        self.tab_layout_1.addLayout(self.tab_grid_layout_1)
        self.tab.addTab(self.tab_widget_1, 'Demodulated')
        self.top_layout.addWidget(self.tab)
        self.rational_resampler_xxx_0 = filter.rational_resampler_fff(
                interpolation=20,
                decimation=1,
                taps=[],
                fractional_bw=0)
        self.qtgui_sink_x_0_0 = qtgui.sink_f(
            1024, #fftsize
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            audio_rate, #bw
            "", #name
            True, #plotfreq
            True, #plotwaterfall
            True, #plottime
            True, #plotconst
            None # parent
        )
        self.qtgui_sink_x_0_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_0_win = sip.wrapinstance(self.qtgui_sink_x_0_0.qwidget(), Qt.QWidget)

        self.qtgui_sink_x_0_0.enable_rf_freq(False)

        self.tab_layout_1.addWidget(self._qtgui_sink_x_0_0_win)
        self.qtgui_sink_x_0 = qtgui.sink_f(
            1024, #fftsize
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            quadrature_rate, #bw
            "", #name
            False, #plotfreq
            True, #plotwaterfall
            True, #plottime
            True, #plotconst
            None # parent
        )
        self.qtgui_sink_x_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_win = sip.wrapinstance(self.qtgui_sink_x_0.qwidget(), Qt.QWidget)

        self.qtgui_sink_x_0.enable_rf_freq(False)

        self.tab_layout_0.addWidget(self._qtgui_sink_x_0_win)
        self.low_pass_filter_0 = filter.fir_filter_fff(
            20,
            firdes.low_pass(
                1,
                quadrature_rate,
                11000,
                500,
                window.WIN_HAMMING,
                6.76))
        self.dc_blocker_xx_0 = filter.dc_blocker_ff(32, True)
        self.blocks_multiply_xx_1 = blocks.multiply_vff(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vff(1)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(0.5)
        self.blocks_add_const_vxx_0 = blocks.add_const_ff(1)
        self.analog_sig_source_x_1 = analog.sig_source_f(quadrature_rate, analog.GR_COS_WAVE, 100000, 1, 0, 0)
        self.analog_sig_source_x_0 = analog.sig_source_f(audio_rate, analog.GR_COS_WAVE, 10000, 1, 0, 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.analog_sig_source_x_1, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.analog_sig_source_x_1, 0), (self.blocks_multiply_xx_1, 1))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_multiply_xx_1, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.qtgui_sink_x_0, 0))
        self.connect((self.blocks_multiply_xx_1, 0), (self.dc_blocker_xx_0, 0))
        self.connect((self.dc_blocker_xx_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.qtgui_sink_x_0_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.blocks_multiply_xx_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "dsb_fc_SP")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_quadrature_rate(self):
        return self.quadrature_rate

    def set_quadrature_rate(self, quadrature_rate):
        self.quadrature_rate = quadrature_rate
        self.analog_sig_source_x_1.set_sampling_freq(self.quadrature_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.quadrature_rate, 11000, 500, window.WIN_HAMMING, 6.76))
        self.qtgui_sink_x_0.set_frequency_range(0, self.quadrature_rate)

    def get_audio_rate(self):
        return self.audio_rate

    def set_audio_rate(self, audio_rate):
        self.audio_rate = audio_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.audio_rate)
        self.qtgui_sink_x_0_0.set_frequency_range(0, self.audio_rate)




def main(top_block_cls=dsb_fc_SP, options=None):

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
