from gnuradio import gr
from gnuradio import blocks
from gnuradio import filter

REMOUTE = False
SAVE = False
FILENAME = ''
DIRECTORY_PATH = ''
DRIVER_ID = ['', '']

SAMP_RATE_2 = 0
SAMP_RATE = 0
BASE_FREQ = 0

class am_demod_cf(gr.hier_block2):

    def __init__(self, channel_rate, audio_decim, audio_pass, audio_stop):
        gr.hier_block2.__init__(self, "am_demod_cf",
                                # Input signature
                                gr.io_signature(1, 1, gr.sizeof_gr_complex),
                                gr.io_signature(1, 1, gr.sizeof_float))      # Input signature

        MAG = blocks.complex_to_mag()
        DCR = blocks.add_const_ff(-1.0)

        audio_taps = filter.optfir.low_pass(0.5,          # Filter gain
                                            channel_rate,  # Sample rate
                                            audio_pass,   # Audio passband
                                            audio_stop,   # Audio stopband
                                            0.1,          # Passband ripple
                                            60)           # Stopband attenuation
        LPF = filter.fir_filter_fff(audio_decim, audio_taps)

        self.connect(self, MAG, DCR, LPF, self)


class demod_10k0a3e_cf(am_demod_cf):

    def __init__(self, channel_rate, audio_decim):
        am_demod_cf.__init__(self, channel_rate, audio_decim,
                             5000,  # Audio passband
                             5500)  # Audio stopband