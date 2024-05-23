#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# Author: eleonora
# GNU Radio version: 3.10.1.1

from packaging.version import Version as StrictVersion
from PyQt5 import Qt
import sip
import os
import datetime
from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import filter
from gnuradio import gr
from gnuradio.fft import window
import signal
from gnuradio import soapy



from gnuradio import qtgui
REMOUTE = False
SAVE = False
FILENAME = ''
DIRECTORY_PATH = ''
DRIVER_ID = ['', '']

SAMP_RATE_2 = 48000
SAMP_RATE = 0
BASE_FREQ = 0

class fmfm(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "FM DSP", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("SDR")
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

        self.settings = Qt.QSettings("GNU Radio", "fmfm")

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
        self.samp_rate_2 = samp_rate_2 = SAMP_RATE_2
        self.samp_rate = samp_rate = SAMP_RATE
        self.base_freq = base_freq = BASE_FREQ


        ##################################################
        # Blocks
        ##################################################
        self.soapy_custom_source_0 = None
        if REMOUTE:
            dev = DRIVER_ID[1]
        else:
            dev = 'driver=' + DRIVER_ID[0]
        stream_args = ''
        tune_args = ['']
        settings = ['']
        self.soapy_custom_source_0 = soapy.source(dev, "fc32",
                                  1, '',
                                  stream_args, tune_args, settings)
        self.soapy_custom_source_0.set_sample_rate(0, samp_rate)
        self.soapy_custom_source_0.set_bandwidth(0, 0)
        self.soapy_custom_source_0.set_antenna(0, 'RX')
        self.soapy_custom_source_0.set_frequency(0, base_freq)
        self.soapy_custom_source_0.set_frequency_correction(0, 0)
        self.soapy_custom_source_0.set_gain_mode(0, False)
        self.soapy_custom_source_0.set_gain(0, 10)
        self.soapy_custom_source_0.set_dc_offset_mode(0, True)
        self.soapy_custom_source_0.set_dc_offset(0, 0)
        self.soapy_custom_source_0.set_iq_balance(0, 0)
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=1,
                decimation=25,
                taps=[],
                fractional_bw=0)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
            1024000, #size
            samp_rate_2, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Амплитуда', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)

        label = 'Сигнал 1'
        width = 1
        color = 'red'
        alpha = 1.0
        style = 1
        marker = -1

        self.qtgui_time_sink_x_0.set_line_label(0, label)
        self.qtgui_time_sink_x_0.set_line_width(0, width)
        self.qtgui_time_sink_x_0.set_line_color(0, color)
        self.qtgui_time_sink_x_0.set_line_style(0, style)
        self.qtgui_time_sink_x_0.set_line_marker(0, marker)
        self.qtgui_time_sink_x_0.set_line_alpha(0, alpha)

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.qtgui_sink_x_0 = qtgui.sink_c(
            16384, # fftsize
            window.WIN_BLACKMAN_hARRIS, # wintype
            base_freq, #fc
            1000000, #bw
            "", #name
            True, #plotfreq
            True, #plotwaterfall
            True, #plottime
            True, #plotconst
            None # parent
        )
        self.qtgui_sink_x_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_win = sip.wrapinstance(self.qtgui_sink_x_0.qwidget(), Qt.QWidget)

        self.qtgui_sink_x_0.enable_rf_freq(False)

        self.top_layout.addWidget(self._qtgui_sink_x_0_win)

        if (SAVE):
            # Формируем полный путь к файлу с использованием os.path.join
            file_name_wav = os.path.join(DIRECTORY_PATH,"SDR_%s_%dkHz_RF.wav" % (datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%SZ"), base_freq / 1000))
            # Инициализация блока сохранения потока данных в .wav
            self.blocks_wavfile_sink_0 = blocks.wavfile_sink(
                file_name_wav,
                1,
                samp_rate_2,
                blocks.FORMAT_WAV,
                blocks.FORMAT_PCM_16,
                False
                )


        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_float*1, samp_rate_2,True)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(0.300)

        if (SAVE):
            # Формируем полный путь к файлу с использованием os.path.join
            file_name_iq = os.path.join(DIRECTORY_PATH,"SDR_%s_%dkHz_RF.iq" % (datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%SZ"), base_freq / 1000))
            # Инициализация блока сохранения потока данных в .iq
            self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_float*1, file_name_iq, False)
            self.blocks_file_sink_0.set_unbuffered(False)


        self.audio_sink_0 = audio.sink(48000, '', True)
        self.analog_fm_demod_cf_0 = analog.fm_demod_cf(
        	channel_rate=240000,
        	audio_decim=5,
        	deviation=75000,
        	audio_pass=15000,
        	audio_stop=16000,
        	gain=1.0,
        	tau=75e-6,
        )


        ##################################################
        # Connections
        ##################################################
        if (SAVE):
            self.connect((self.analog_fm_demod_cf_0, 0), (self.blocks_multiply_const_vxx_0, 0))
            self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_file_sink_0, 0))
            self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_throttle_0, 0))
            self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_wavfile_sink_0, 0))
            self.connect((self.blocks_throttle_0, 0), (self.audio_sink_0, 0))
            self.connect((self.blocks_throttle_0, 0), (self.qtgui_time_sink_x_0, 0))
            self.connect((self.rational_resampler_xxx_0, 0), (self.analog_fm_demod_cf_0, 0))
            self.connect((self.rational_resampler_xxx_0, 0), (self.qtgui_sink_x_0, 0))
            self.connect((self.soapy_custom_source_0, 0), (self.rational_resampler_xxx_0, 0))
        else:
            self.connect((self.analog_fm_demod_cf_0, 0), (self.blocks_multiply_const_vxx_0, 0))
            self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_throttle_0, 0))
            self.connect((self.blocks_throttle_0, 0), (self.audio_sink_0, 0))
            self.connect((self.blocks_throttle_0, 0), (self.qtgui_time_sink_x_0, 0))
            self.connect((self.rational_resampler_xxx_0, 0), (self.analog_fm_demod_cf_0, 0))
            self.connect((self.rational_resampler_xxx_0, 0), (self.qtgui_sink_x_0, 0))
            self.connect((self.soapy_custom_source_0, 0), (self.rational_resampler_xxx_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "FM демодуляция")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate_2(self):
        return self.samp_rate_2

    def set_samp_rate_2(self, samp_rate_2):
        self.samp_rate_2 = samp_rate_2
        self.blocks_throttle_0.set_sample_rate(self.samp_rate_2)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate_2)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_base_freq(self):
        return self.base_freq

    def set_base_freq(self, base_freq):
        self.base_freq = base_freq
        self.qtgui_sink_x_0.set_frequency_range(self.base_freq, 1000000)
        self.soapy_custom_source_0.set_frequency(0, self.base_freq)




def fmfm_start_dsp(top_block_cls=fmfm, options=None):
    print("check")
    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    print("top_block_cls")
    tb = top_block_cls()
    print("start")
    tb.start()
    print("show")

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

