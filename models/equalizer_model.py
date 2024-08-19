import numpy as np
from scipy import signal

class EqualizerModel:
    def __init__(self, gains=None, q_factors=None, mutes=None, locks=None):
        """
        Inizializza l'equalizzatore con guadagni, Q Factor, mute e lock opzionali.
        :param gains: Una lista di guadagni per le 10 bande di frequenza.
        :param q_factors: Una lista di Q Factor per le 10 bande di frequenza.
        :param mutes: Una lista di stati di mute (True/False) per le 10 bande di frequenza.
        :param locks: Una lista di stati di lock (True/False) per le 10 bande di frequenza.
        """
        self.center_frequencies = [31, 63, 125, 250, 500, 1000, 2000, 4000, 8000, 16000]
        self.gains = gains if gains is not None else [1.0] * len(self.center_frequencies)
        self.q_factors = q_factors if q_factors is not None else [5.0] * len(self.center_frequencies)
        self.mutes = mutes if mutes is not None else [False] * len(self.center_frequencies)
        self.locks = locks if locks is not None else [False] * len(self.center_frequencies)

    def apply_equalization(self, audio_data, fs):
        """
        Applica l'equalizzazione all'audio dato.
        :param audio_data: Dati audio come array NumPy.
        :param fs: Frequenza di campionamento dell'audio.
        :return: Dati audio equalizzati.
        """
        equalized_samples = self._equalize(audio_data, fs)
        return equalized_samples

    def _equalize(self, audio_data, fs):
        output = np.zeros_like(audio_data)
        for i, center_freq in enumerate(self.center_frequencies):
            if not self.mutes[i]:  # Ignora le bande mute
                q_factor = self.q_factors[i]
                band = self._bandpass_filter(audio_data, center_freq, fs, q_factor)
                output += self.gains[i] * band
        return output

    def _bandpass_filter(self, data, center_freq, fs, q_factor, order=2):
        nyquist = 0.5 * fs
        bandwidth = center_freq / q_factor
        low = (center_freq - bandwidth / 2) / nyquist
        high = (center_freq + bandwidth / 2) / nyquist
        
        b, a = signal.iirfilter(order, [low, high], btype='band', ftype='butter')
        return signal.lfilter(b, a, data)

    def set_gain(self, band_index, gain_value):
        if not self.locks[band_index]:  # Modifica il gain solo se la banda non è bloccata
            self.gains[band_index] = gain_value

    def mute_band(self, band_index, state=True):
        """Mute o unmute una banda specifica."""
        self.mutes[band_index] = state

    def lock_band(self, band_index, state=True):
        """Blocca o sblocca una banda specifica."""
        self.locks[band_index] = state

    def set_q_factor(self, band_index, q_value):
        """
        Imposta il Q Factor per una banda specifica.
        :param band_index: L'indice della banda da modificare (0-9).
        :param q_value: Il nuovo valore del Q Factor.
        """
        self.q_factors[band_index] = q_value
