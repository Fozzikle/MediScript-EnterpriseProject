# imports
import shutil
import FreeSimpleGUI as sg
import Patient_view
import new_patient_setup
import Patient_Recovery
import os
from File_Config import load_config
import json


def load_patients(base_folder):
    patients = []
    base_path = base_folder

    if not os.path.exists(base_path):
        return patients

    for patient_name in os.listdir(base_path):
        patient_path = os.path.join(base_path, patient_name, "Patient Information", "patient_data.json")
        if os.path.exists(patient_path):
            with open(patient_path, "r") as f:
                data = json.load(f)
                patients.append(data)
    return patients


def UI_window():
    # Help load patient files
    config = load_config()
    base_folder = config.get("base_folder")

    patient = load_patients(base_folder)

    # name only for patient searchbar
    patient_names = [p['name'] for p in patient]

    # Patient Searchbar
    patient_lookup = [
        [sg.Text("Patient Search", font=('Segoe UI', 12), text_color='#2D2D2D', background_color='#F7F9FB')],
        [sg.Input(enable_events=True, size=(0, 1), expand_x=True, do_not_clear=True, background_color='#F7F9FB',
                  key='-search-')],
        [sg.Listbox(patient_names, size=(1, 5), expand_x=True, key="-Patient_List-",
                    select_mode=sg.LISTBOX_SELECT_MODE_SINGLE, font=('Segoe UI', 11),
                    highlight_background_color='#2A7FA2')]
    ]

    # Buttons new, delete, & select (need to add an edit button)
    patient_buttons = [
        [
            sg.Button("Select", size=(12, 1), button_color=('white', '#2A7FA2'), font=('Segoe UI', 12, 'bold'),
                      key='-select-'),
            sg.Button("New Patient", size=(12, 1), button_color=('#2D2D2D', '#E0E0E0'), font=('Segoe UI', 12, 'bold'),
                      key='-add-'),
            sg.Button(" Edit Patient", size=(12, 1), button_color=('#2D2D2D', '#E0E0E0'), font=('Segoe UI', 12, 'bold'),
                      key='-edit-'),
            sg.Button("Delete Patient", size=(12, 1), button_color=('#2D2D2D', '#E0E0E0'), font=('Segoe UI', 12, 'bold'),
                      key='-delete-'),
            sg.Button("Recover Patient", size=(12, 1), button_color=('#2D2D2D', '#E0E0E0'), font=('Segoe UI', 12, 'bold'),
                      key='-recover-')
        ]
    ]

    # Layout
    layout = [
        [sg.Column(patient_lookup, justification='centre', expand_x=True, background_color='#F7F9FB')],
        [sg.Column(patient_buttons, justification='centre', background_color='#F7F9FB')]
    ]

    # Creating the Window
    window = sg.Window('Transcriber', layout, use_default_focus=False, resizable=True, size=(800, 500),
                       background_color='#F7F9FB')

    # Event Loop
    while True:
        event, values = window.read()
        # exit
        if event == "Exit" or event == sg.WIN_CLOSED:
            break

        # searchbar function
        elif event == '-search-':
            search = values["-search-"]
            if search:
                filtered_names = [p['name'] for p in patient if search.lower() in p['name'].lower()]
            else:
                filtered_names = patient_names
            window['-Patient_List-'].update(filtered_names)

        # Select button function
        elif event == "-select-":
            selected_list = values['-Patient_List-']
            if selected_list:
                selected_name = selected_list[0]
                selected_patient = next((p for p in patient if p['name'] == selected_name), None)
                if selected_patient:
                    Patient_view.Patient_view_window(selected_patient)
            else:
                sg.popup("No patient selected!", title="Error")  # error screen

        # New patient button function
        elif event == '-add-':
            new_patient = new_patient_setup.new_patient_window()  # runs new_patient_setup.py
            if new_patient:
                patient.append(new_patient)  # Add name to the patient list
                patient_names = [p['name'] for p in patient]
                window["-Patient_List-"].update(patient_names)

        elif event == '-edit-':
            selected_list = values['-Patient_List-']
            if selected_list:
                selected_name = selected_list[0]
                selected_patient = next((p for p in patient if p['name'] == selected_name), None)
                if selected_patient:
                    update_patient = new_patient_setup.new_patient_window(existing_data = selected_patient)
                    if update_patient:
                        index = patient.index(selected_patient)
                        patient[index] = update_patient
                        patient_names = [p['name'] for p in patient]
                        window['-Patient_List-'].update(patient_names)
                    else:
                        sg.popup("No patient selected", title='Error')
            else:
                sg.popup("No patient selected", title='Error')

        # delete button function
        elif event == '-delete-':
            delete_patient = values["-Patient_List-"]
            if delete_patient:
                selected_name = delete_patient[0]
                patient_to_delete = next((p for p in patient if p['name'] == selected_name), None)
                if patient_to_delete:
                    patient_folder = os.path.join(base_folder, selected_name)
                    delete_folder = os.path.join(os.path.dirname(base_folder), "Deleted Patients")

                os.makedirs(delete_folder, exist_ok=True)

                try:
                    shutil.move(patient_folder, os.path.join(delete_folder, selected_name))
                    sg.popup(
                        f"{selected_name} has been deleted! It can still be recovered by accessing the delete folder",
                        title="Deleted")

                    patient.remove(patient_to_delete)
                    patient_names = [p['name'] for p in patient]
                    window["-Patient_List-"].update(patient_names)

                except Exception as e:
                    sg.popup_error(f"Error moving patient folder: {e}")
            else:
                sg.popup("No patient selected!", title="Error")

        elif event == '-recover-':
            Patient_Recovery.patient_recovery()
            patient = load_patients(base_folder)
            patient_names = [p['name'] for p in patient]
            window["-Patient_List-"].update(patient_names)

    # Closing the Window
    window.close()
