import sounddevice as sd
import scipy.io.wavfile as wav
import tempfile
import numpy as np
from faster_whisper import WhisperModel

recorded_frames = []
stream = None
sample_rate = 16000


def callback(indata, frames, time, status):
    global recorded_frames
    recorded_frames.append(indata.copy())


def start_recording():
    global stream, recorded_frames

    recorded_frames = []

    stream = sd.InputStream(
        samplerate=sample_rate,
        channels=1,
        callback=callback
    )

    stream.start()


def stop_recording():
    global stream, recorded_frames

    stream.stop()
    stream.close()

    audio_data = np.concatenate(recorded_frames, axis=0)

    temp_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".wav"
    )

    wav.write(
        temp_file.name,
        sample_rate,
        audio_data
    )

    return temp_file.name


def speech_to_text(audio_file):
    print("Loading Whisper model...")

    model = WhisperModel(
        "small",
        device="cpu",
        compute_type="int8"
    )

    segments, info = model.transcribe(
        audio_file,
        beam_size=5
    )

    full_text = ""

    for segment in segments:
        full_text += segment.text + " "

    return full_text.strip()