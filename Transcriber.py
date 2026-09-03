# Imports
from vosk import Model, KaldiRecognizer
import pyaudio
import json
import os
from datetime import datetime
import FreeSimpleGUI as sg
import threading
import time
from cleaning import full_clean
import numpy as np
from record_raw_audio import AudioRecording


# backend stuff
def transcriber(end_transcriber, transcription_folder):
    # setup
    model = Model(
        r"C:\Users\mathi\PycharmProjects\Enterprise_Computing_Major_Work_Transcriber\vosk-model-small-en-us-0.15\vosk-model-small-en-us-0.15")
    recognizer = KaldiRecognizer(model, 16000)

    mic = pyaudio.PyAudio()
    stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
    stream.start_stream()

    # Creating place to store the transcription
    transcript = []

    try:
        # Loop for when the transcriber is active
        while True:
            data = stream.read(4096, exception_on_overflow=True)

            audio_data = np.frombuffer(data, dtype=np.int16)
            max_val = np.max(np.abs(audio_data))
            if max_val > 0:
                gain = int(0.75 * 32767 / max_val)
                audio_data = np.clip(audio_data * gain, -32768, 32767).astype(np.int16)
            normalized_data = audio_data.tobytes()

            if recognizer.AcceptWaveform(normalized_data):
                result = json.loads(recognizer.Result())  # reformat output
                text = result.get("text", "")
                if text:
                    transcript.append(text)  # Store transcription

            # ending transcription
            if end_transcriber():
                break

    finally:
        # ensuring tasks close correctly
        stream.stop_stream()
        stream.close()
        mic.terminate()

        # Ensuring that the whole transcription is saved (had bug where last sentence didn't save)
        final_result = json.loads(recognizer.FinalResult())
        final_text = final_result.get("text", "")
        if final_text:
            transcript.append(final_text)

        # Adding ability to clean data
        raw_text = "\n".join(transcript)
        cleaned_transcript = full_clean(raw_text)

        # Saving the transcription to .txt file and setting save location
        os.makedirs(transcription_folder, exist_ok=True)

        filename_raw = os.path.join(transcription_folder,
                                    f"transcription_raw_{datetime.now().strftime('%d%m%y_%H%M%S')}.txt")
        with open(filename_raw, "w") as f:
            f.write("\n".join(transcript))

        filename_cleaned = os.path.join(transcription_folder,
                                        f"transcription_cleaned_{datetime.now().strftime('%d%m%y_%H%M%S')}.txt")
        with open(filename_cleaned, "w") as f:
            f.write("\n".join(f"{speaker}: {sentence}" for speaker, sentence in cleaned_transcript))

        return filename_raw, filename_cleaned


# Frontend Stuff

# making a loading bar (show it is working)
def loading(text_element, stop_flag):
    full_text = "Transcribing..."
    while not stop_flag[0]:
        for i in range(0, len(full_text) + 1):
            if stop_flag[0]:
                break
            text_element.update(full_text[:i])
            time.sleep(0.1)  # speed of loading
        time.sleep(0.35)  # time before re-looping


# Creating transcriber window
def transcription_window(transcription_folder):
    stop_flag = [False]
    file_output = [None]

    def end_transcriber():
        return stop_flag[0]

    def threaded_transcriber():
        filename_raw, filename_cleaned = transcriber(end_transcriber, transcription_folder)
        file_output[0] = (filename_raw, filename_cleaned)

    # Transcriber thread
    thread = threading.Thread(target=threaded_transcriber, daemon=True)
    thread.start()

    # Raw audio thread
    audio_logger = AudioRecording(transcription_folder)
    thread_audio = threading.Thread(target=audio_logger.start_recording, daemon=True)
    thread_audio.start()

    layout = [
        [sg.Text("", key="-Animate-", font=('Segoe UI', 14, 'bold'), text_color='#2A7FA2', size=(20, 1),
                 background_color='#F7F9FB')],
        [sg.Column([[sg.Button("Stop", size=(15, 2), button_color=('white', '#2A7FA2'),
                               font=('Segoe UI', 12, 'bold'))]], background_color='#F7F9FB', justification='right')]
    ]

    window = sg.Window("Transcribing", layout, modal=True, finalize=True, size=(300, 100), background_color='#F7F9FB')

    threading.Thread(target=loading, args=(window["-Animate-"], stop_flag), daemon=True).start()

    while True:
        event, _ = window.read(timeout=100)  # timeout ensures the animation continuously updates
        if event == sg.WIN_CLOSED or event == "Stop":
            stop_flag[0] = True
            break

    window.close()

    # ending threads
    audio_logger.end_recording()
    thread_audio.join()
    thread.join()

    if file_output[0] is not None:
        filename_raw, filename_cleaned = file_output[0]

        for file in [filename_cleaned, audio_logger.output_path]:
            if os.path.exists(file):
                os.startfile(file)
