import wave
import pyaudio
import soundfile as sf
from datetime import datetime
import os


class AudioRecording:
    # records audio to .wac file real time
    def __init__(self, transcription_folder):
        timestamp = datetime.now().strftime('%d%m%y_%H%M%S')
        self.output_folder = os.path.join(transcription_folder, 'raw_audio')
        os.makedirs(self.output_folder, exist_ok=True)
        self.output_path = os.path.join(self.output_folder, f"raw_audio_{timestamp}.wav")

        self.running = False
        self.frames = []
        self.rate = 16000
        self.channels = 1
        self.chunk = 1024
        self.format = pyaudio.paInt16

    def start_recording(self):
        self.running = True
        audio = pyaudio.PyAudio()
        stream = audio.open(format=self.format, channels=self.channels, rate=self.rate, input=True,
                            frames_per_buffer=self.chunk)
        while self.running:
            data = stream.read(self.chunk, exception_on_overflow=False)
            self.frames.append(data)

        stream.stop_stream()
        stream.close()
        audio.terminate()

        self.save_audio()

    def end_recording(self):
        self.running = False

    def save_audio(self):
        with wave.open(self.output_path, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(pyaudio.PyAudio().get_sample_size(self.format))
            wf.setframerate(self.rate)
            wf.writeframes(b''.join(self.frames))
