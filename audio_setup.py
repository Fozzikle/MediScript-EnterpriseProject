import FreeSimpleGUI as sg
import numpy as np
import sounddevice as sd
import threading
import time

bar_length = 30


def get_gradient():
    colours = []
    for i in range(bar_length):
        ratio = i / (bar_length - 1)
        if ratio < 0.5:
            r = 1.0 - 2 * ratio
            g = 2 * ratio
        else:
            r = 2 * (ratio - 0.5)
            g = 1.0 - 2 * (ratio - 0.5)
        b = 0.0
        hex_colour = '#%02x%02x%02x' % (int(r * 255), int(g * 255), int(b * 255))
        colours.append(hex_colour)
    return colours


def animate_speaking(window, flag):
    dots = ""
    while flag[0]:
        dots += "."
        if len(dots) > 3:
            dots = ""
        window.write_event_value('-anim-', f"Listening{dots}")
        time.sleep(0.5)


def run_test(test_name, window, duration=5.0):
    gradient = get_gradient()
    volume_list = []

    window['-anim-'].update("Get ready to speak...")
    time.sleep(1)

    running_flag = [True]
    anim_thread = threading.Thread(target=animate_speaking, args=(window, running_flag), daemon=True)
    anim_thread.start()

    def audio_callback(indata, frames, time_info, status):
        volume_norm = np.sqrt(np.mean(np.square(indata)))
        db = 20 * np.log10(volume_norm + 1e-6)
        volume_list.append(db)

        adjusted_db = db + 40
        normalised = max(0, min(1, (adjusted_db + 60) / 60))
        index = int(normalised * (bar_length - 1))
        bar_str = ""
        for i, colour in enumerate(gradient):
            char = "█" if i <= index else " "
            bar_str += char
        window.write_event_value('-update-', (bar_str, gradient[index], db))

    with sd.InputStream(callback=audio_callback, channels=1, samplerate=44100, blocksize=1024):
        start_time = time.time()
        end_time = start_time + duration
        while time.time() - start_time < duration:
            time_left = int(end_time - time.time())
            event, values = window.read(timeout=100)
            window['-countdown-'].update(f"{time_left}s left")
            if event == '-update-':
                bar_str, colour, db = values['-update-']
                window['-bar-'].update(bar_str, text_color=colour)
                window['-db-'].update(f"{db:.1f} db", text_color=colour)
            elif event == '-anim-':
                window['-anim-'].update(values['-anim-'])

    running_flag[0] = False
    time.sleep(0.5)
    window['-anim-'].update("Recording complete")
    window['-countdown-'].update("")
    time.sleep(1)
    window['-anim-'].update("")

    avg_db = np.mean(volume_list)
    return avg_db


def mic_test_popup():
    gradient = get_gradient()

    layout = [
        # title
        [sg.Push(background_color='#F7F9FB'),
         sg.Text('Microphone Configuration', font=('Segoe UI', 35, 'bold'), text_color='#2A7FA2', pad=(0, 0),
                 background_color='#F7F9FB'),
         sg.Push(background_color='#F7F9FB')],

        [sg.Column(
            layout=[
                # text
                [sg.Text("Follow these steps to test the microphone at different distances.",
                         font=('Segoe UI', 12), text_color='#2D2D2D', background_color='#F7F9FB')],

                # steps to completion
                [sg.Frame(
                    title="",
                    layout=[
                        [sg.Text("Step 1. Stand or sit near your microphone and press 'Start Near-Field Test' and talk",
                                 font=('Segoe UI', 12), text_color='#2D2D2D', background_color='#F7F9FB')],
                        [sg.Text("Step 2. Press the 'Start Far-Field Test' and stand as far away from the microphone as"
                                 " possible.",
                                 font=('Segoe UI', 12), text_color='#2D2D2D', background_color='#F7F9FB')],
                        [sg.Text("Step 3. Follow the prompts to adjust the microphone position.",
                                 font=('Segoe UI', 12), text_color='#2D2D2D', background_color='#F7F9FB')],
                        [sg.Text("Step 4. Repeat 1 through 3 until the prompts says that the microphone is good.",
                                 font=('Segoe UI', 12), text_color='#2D2D2D', background_color='#F7F9FB')]
                    ], font=('Segoe UI', 12, 'bold'), title_color='#2A7FA2', border_width=1, relief=sg.RELIEF_FLAT,
                    background_color='#F7F9FB', pad=((0, 0), (0, 0))
                )],

                # input level
                [sg.Text("Input Level:", font=('Segoe UI', 12), text_color='#2D2D2D', background_color='#F7F9FB',
                         justification='left'),
                 sg.Text("", font=('Segoe UI', 12), text_color='#2D2D2D', background_color='#F7F9FB',
                         justification='right', key='-db-')],

                # sound bar
                [sg.Text("", size=(bar_length + 5, 1),background_color='#F7F9FB', justification='centre', key='-bar-')],

                # listening animation
                [sg.Text("", size=(20, 1), text_color='#2D2D2D', background_color='#F7F9FB', justification='left',
                         key='-anim-'),
                 sg.Text("", size=(15, 1),text_color='#2D2D2D', background_color='#F7F9FB', justification='right',
                         key='-countdown-')],

                # field buttons
                [sg.Button("Start Near-Field Test", size=(20, 2), button_color=('#2D2D2D', '#E0E0E0'),
                           font=('Segoe UI', 12, 'bold'), key='-near-'),
                 sg.Button("Start Far-Field Testing", size=(20, 2), button_color=('white', '#2A7FA2'),
                           font=('Segoe UI', 12, 'bold'), key='-far-')],

                # other buttons
                [sg.Button("Repeat", size=(15, 2), button_color=('#2D2D2D', '#E0E0E0'),
                           font=('Segoe UI', 12, 'bold'), visible=False, key='-repeat-'),
                 sg.Button("See Results", size=(15, 2), button_color=('white', '#2A7FA2'),
                           font=('Segoe UI', 12, 'bold'), key='-result-')]

            ], expand_x=True, background_color='#F7F9FB', pad=((60, 0), (20, 0))
        )]
    ]

    window = sg.Window("Mic Position Setup", layout, background_color='#F7F9FB', finalize=True, modal=True)

    near_db, far_db = None, None

    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break

        elif event == '-near-':
            near_db = run_test("Near Field", window)

        elif event == '-far-':
            far_db = run_test("Far Field", window)

        elif event == '-repeat-':
            near_db = far_db = None
            window['-bar-'].update("")
            window['-db-'].update("")
            window['-repeat-'].update(visible=False)

        elif event == '-result-':
            if near_db is None or far_db is None:
                sg.Popup("Ensure both tests are completed before viewing results.")
                continue

            diff = near_db - far_db
            abs_diff = abs(diff)
            direction = "Closer to" if diff > 0 else "further away from"

            if abs_diff < 7:
                result_message = (
                    f"Microphone is in an ideal location. \n\n"
                    f"Difference between Near and Far Field: {abs_diff:.1f} db\n"
                    "Small difference indicates good sensitivity across distances."
                )
            else:
                result_message = (
                    f"Microphone placement needs adjustment. \n\n"
                    f"Near Field: {near_db:.1f} db\n"
                    f"Far Field: {far_db:.1f} db\n"
                    f"Difference: {abs_diff:.1f} db\n\n"
                    f"Consider moving the microphone {direction} the Far Field position to balance levels better."
                )

            sg.popup("Microphone Position Test Results", result_message)
            window['-repeat-'].update(visible=True)

    window.close()
