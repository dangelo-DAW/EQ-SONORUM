import librosa
import pydub
import soundfile as sf
import numpy as np
from scipy.signal import butter, sosfilt
import pyaudio
from PyQt5.QtWidgets import QApplication, QWidget
import matplotlib.pyplot as plt
import sounddevice as sd
import plotly.graph_objs as go

print("Tutte le librerie sono state importate correttamente!")
