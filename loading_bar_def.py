import threading
import FreeSimpleGUI as sg
import time
import os


def run_loading(task_func=None, next_func=None, *args, **kwargs):
    done_event = threading.Event()

    def task_run():
        try:
            time.sleep(0.3)
            # connects the end window to the loading thread
            if task_func:
                task_func(*args, **kwargs)
        except Exception as e:
            print(f"Error task_function crashed: {e}")
        # Ends animation
        finally:
            done_event.set()

    # running the loading screen
    thread = threading.Thread(target=task_run, daemon=True)
    thread.start()

    # file locations of animations
    anim_folder = os.path.join(os.getcwd(), "loading_bar_gifs")
    loop_anim = os.path.join(anim_folder, "Loading_Loop.gif")

    transparent_colour = 'black'

# centering the window
    # loading size
    window_width, window_height = 400, 225

    # screen size
    screen_width, screen_height = sg.Window.get_screen_size()

    # centering base on screen
    x = int((screen_width - window_width)/2)
    y = int((screen_height - window_height)/2)

    # Creating loading window template
    layout = [[sg.Image(size=(window_width, window_height), background_color=transparent_colour, key='-anim-')]]
    window = sg.Window("", layout, location=(x, y), no_titlebar=True, transparent_color=transparent_colour,
                       keep_on_top=True, finalize=True, background_color=transparent_colour,
                       element_justification='center')

    # ensures window is ontop
    window.bring_to_front()

    # playing looping part
    if os.path.exists(loop_anim):
        window['-anim-'].update_animation(loop_anim)
        while not done_event.is_set():
            event, _ = window.read(timeout=50)
            window['-anim-'].update_animation(loop_anim)

    else:
        print("Missing Animation!", loop_anim)

    window.close()

    if next_func:
        next_func()
