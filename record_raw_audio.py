import wave
import sounddevice as sd
from datetime import datetime
import os


class AudioRecording:
    # records audio to .wav file in real time
    def __init__(self, transcription_folder):
        timestamp = datetime.now().strftime('%d%m%y_%H%M%S')
        self.output_folder = os.path.join(transcription_folder, 'raw_audio')
        os.makedirs(self.output_folder, exist_ok=True)
        self.output_path = os.path.join(
            self.output_folder,
            f"raw_audio_{timestamp}.wav"
        )

        self.running = False
        self.frames = []
        self.rate = 16000
        self.channels = 1
        self.chunk = 1024
        self.dtype = 'int16'

    def start_recording(self):
        self.running = True

        try:
            with sd.RawInputStream(
                samplerate=self.rate,
                blocksize=self.chunk,
                channels=self.channels,
                dtype=self.dtype
            ) as stream:

                while self.running:
                    data, overflowed = stream.read(self.chunk)
                    self.frames.append(data)

        finally:
            self.save_audio()

    def end_recording(self):
        self.running = False

    def save_audio(self):
        with wave.open(self.output_path, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(2)
            wf.setframerate(self.rate)
            wf.writeframes(b''.join(self.frames))
