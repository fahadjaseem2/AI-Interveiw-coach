import sounddevice as sd
import scipy.io.wavfile as wav
import tempfile
import numpy as np
from faster_whisper import WhisperModel
import os

# ---------------------------
# Global configs
# ---------------------------
SAMPLE_RATE = 16000
CHANNELS = 1

recorded_frames = []
stream = None

# ---------------------------
# Load Whisper model ONCE
# ---------------------------
print("Loading Whisper model... Please wait.")

model = WhisperModel(
    "small",
    device="cpu",          # change to "cuda" if using GPU
    compute_type="int8"
)

print("Whisper model loaded successfully.")


# ---------------------------
# Audio callback
# ---------------------------
def callback(indata, frames, time, status):
    global recorded_frames

    if status:
        print(f"Audio status warning: {status}")

    recorded_frames.append(indata.copy())


# ---------------------------
# Start recording
# ---------------------------
def start_recording():
    global stream, recorded_frames

    if stream is not None:
        print("Recording already in progress.")
        return

    recorded_frames = []

    try:
        stream = sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            callback=callback
        )

        stream.start()
        print("Recording started...")

    except Exception as e:
        print(f"Error starting recording: {e}")


# ---------------------------
# Stop recording
# ---------------------------
def stop_recording():
    global stream, recorded_frames

    if stream is None:
        raise Exception("No active recording found.")

    try:
        stream.stop()
        stream.close()
        stream = None

        if len(recorded_frames) == 0:
            raise Exception("No audio data recorded.")

        audio_data = np.concatenate(recorded_frames, axis=0)

        # Convert float32 audio to int16 format
        audio_data = (audio_data * 32767).astype(np.int16)

        temp_file = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".wav"
        )

        wav.write(
            temp_file.name,
            SAMPLE_RATE,
            audio_data
        )

        print("Recording stopped.")
        return temp_file.name

    except Exception as e:
        print(f"Error stopping recording: {e}")
        raise e


# ---------------------------
# Speech to text
# ---------------------------
def speech_to_text(audio_file):
    if not os.path.exists(audio_file):
        raise FileNotFoundError("Audio file not found.")

    try:
        print("Transcribing audio...")

        segments, info = model.transcribe(
            audio_file,
            beam_size=5
        )

        full_text = " ".join(
            segment.text.strip()
            for segment in segments
        )

        if not full_text:
            return "No speech detected."

        return full_text

    except Exception as e:
        print(f"Transcription error: {e}")
        return "Error during transcription."