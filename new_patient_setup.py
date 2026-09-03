import FreeSimpleGUI as sg
import Personal_Patient
from Data_Store import patient_folder_structure
import json
from File_Config import load_config

config = load_config()
skip_medical = config.get('skip_history_clinical', False)


def new_patient_window(existing_data=None):
    # button format
    button_style = dict(
        size=(25, 2),
        button_color=('#2D2D2D', '#E0E0E0'),
        font=('Segoe UI', 12, 'bold'),
        pad=(0, 10)
    )

    # title
    title_text = "Edit Patient" if existing_data else "New Patient"

    header = [
        [sg.Push(background_color='#F7F9FB'),
         sg.Text(title_text, font=('Segoe UI', 35, 'bold'), text_color='#2A7FA2',
                 background_color='#F7F9FB'),
         sg.Push(background_color='#F7F9FB')]
    ]

    # buttons
    patient_personal = [[sg.Button("Personal", **button_style, key='-personal-')]]

    patient_history = []
    patient_clinical_directives = []

    if not skip_medical:
        patient_history = [[sg.Button("Medical History", **button_style, key='-history-')]]
        patient_clinical_directives = [[sg.Button("Clinical Data", **button_style, key='-clinical-')]]

    # footer buttons
    sub_can = [[
        sg.Push(background_color='#F7F9FB'),
        sg.Button("Cancel", size=(12, 1), button_color=('#2D2D2D', '#E0E0E0'), font=('Segoe', 12, 'bold'), key='-can-'),
        sg.Button("Submit", size=(12, 1), button_color=('white', '#2A7FA2'), font=('Segoe', 12, 'bold'), key='-sub-'),
        sg.Push(background_color='#F7F9FB')
    ]]

    # layout
    button_layout = [
        [sg.Column(patient_personal, background_color='#F7F9FB')],
    ]

    if not skip_medical:
        button_layout.append([sg.Column(patient_history, background_color='#F7F9FB')])
        button_layout.append([sg.Column(patient_clinical_directives, background_color='#F7F9FB')])

    layout = [
        [sg.Column(header, background_color='#F7F9FB', justification='centre')],
        [sg.Column(button_layout, background_color='#F7F9FB', justification='centre')],
        [sg.VPush(background_color='#F7F9FB')],
        [sg.Column(sub_can, background_color='#F7F9FB', justification='centre')]
    ]

    # window
    window = sg.Window(title_text, layout, background_color='#F7F9FB', use_default_focus=False, size=(420, 500),
                       finalize=True)

    # background stuff
    patient_data = None

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        elif event == '-personal-':
            patient_data = Personal_Patient.Personal_Patient_window(patient_data or existing_data)
        elif event == '-history-':
            sg.popup('This window has not been implemented by your organisation! Skip for now')
        elif event == '-clinical-':
            sg.popup('This window has not been implemented by your organisation! Skip for now')
        elif event == '-sub-':
            if patient_data and 'name' in patient_data:
                config = load_config()
                base_folder = config.get('base_folder')
                if not base_folder:
                    sg.popup("Base folder has not been set. Please delete your current config file and reopen the "
                             "program")
                    break
                files = patient_folder_structure(patient_data['name'], base_folder)
                with open(f'{files["info"]}/patient_data.json', 'w') as f:
                    json.dump(patient_data, f, indent=4)
            break
        elif event == '-can-':
            break

    window.close()
    return patient_data
