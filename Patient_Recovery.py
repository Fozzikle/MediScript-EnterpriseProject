# imports
import shutil
import FreeSimpleGUI as sg
import os
import json
from File_Config import load_config


# gathering deleted patients
def load_del_patients(deleted_folder):
    patients = []

    if not os.path.exists(deleted_folder):
        return patients

    for patient_name in os.listdir(deleted_folder):
        patient_path = os.path.join(deleted_folder, patient_name, "Patient Information", "patient_data.json")

        if os.path.exists(patient_path):
            try:
                with open(patient_path, "r") as f:
                    data = json.load(f)
                    patients.append(data)
            except Exception as e:
                print(f"Error reading {patient_path}: {e}")

    return patients


def patient_recovery():
    config = load_config()
    base_folder = config.get("base_folder")
    deleted_folder = os.path.join(os.path.dirname(base_folder), "Deleted Patients")

    deleted_patients = load_del_patients(deleted_folder)
    patient_names = [p['name'] for p in deleted_patients]

    # title
    title = [sg.Text("Patient Recovery", font=('Segoe UI', 18, 'bold'), text_color='#2A7FA2',
                     background_color='#F7F9FB')]

    # patient list
    patient_lookup = [
        [sg.Text("Patient Search", font=('Segoe UI', 12), text_color='#2D2D2D', background_color='#F7F9FB')],
        [sg.Input(enable_events=True, size=(0, 1), expand_x=True, do_not_clear=True, background_color='#F7F9FB',
                  key='-search-')],
        [sg.Listbox(patient_names, size=(1, 5), expand_x=True, key="-Patient_List-",
                    select_mode=sg.LISTBOX_SELECT_MODE_SINGLE, font=('Segoe UI', 11),
                    highlight_background_color='#2A7FA2')]
    ]

    # Recover and delete buttons
    button = [
        sg.Button("True delete", size=(12, 1), button_color=('#2D2D2D', '#E0E0E0'), font=('Segoe UI', 12, 'bold'),
                  key='-Delete-'),
        sg.Button("Recover", size=(12, 1), button_color=('white', '#2A7FA2'), font=('Segoe UI', 12, 'bold'),
                  key='-Recover-')
    ]

    # Layout
    layout = [
        [sg.Column([title], justification='centre', background_color='#F7F9FB')],
        [sg.Column(patient_lookup, justification='centre', expand_x=True, background_color='#F7F9FB')],
        [sg.Column([button], justification='centre', background_color='#F7F9FB')]
    ]

    # Window
    window = sg.Window("Patient Recovery", layout, size=(420, 300), finalize=True, resizable=True,
                       background_color='#F7F9FB')

    # event loop
    while True:
        event, values = window.read()
        # exit
        if event == "Exit" or event == sg.WIN_CLOSED:
            break

        elif event == '-Delete-':
            deleted_patients_list = values["-Patient_List-"]
            if deleted_patients_list:
                selected_name = deleted_patients_list[0]
                confirm = sg.popup_yes_no(f"Are you sure you want to permanently delete {selected_name}?",
                                          title="Confirm")

                if confirm == "Yes":
                    try:
                        source_path = os.path.join(os.path.dirname(base_folder), "Deleted Patients", selected_name)
                        shutil.rmtree(source_path)

                        deleted_patients = [p for p in deleted_patients if p['name'] != selected_name]
                        patient_names = [p['name'] for p in deleted_patients]
                        window["-Patient_List-"].update(patient_names)

                        sg.popup(f"{selected_name} has been permanently deleted!", title="Bye Bye")
                    except Exception as e:
                        sg.popup_error(f"Error permanently deleting folder: {e}")
            else:
                sg.popup("No patient selected!", title="Error")

        elif event == '-Recover-':
            recover_patient = values["-Patient_List-"]
            if recover_patient:
                selected_name = recover_patient[0]
                patient_to_recover = next((p for p in deleted_patients if p['name'] == selected_name), None)
                if patient_to_recover:
                    delete_folder = os.path.join(os.path.dirname(base_folder), "Deleted Patients", selected_name)
                    patient_folder = os.path.join(os.path.dirname(base_folder), "Patient Data", selected_name)

                    try:
                        shutil.move(delete_folder, patient_folder)
                        sg.popup(f"{selected_name} has been recovered!", title="Success!")

                        deleted_patients.remove(patient_to_recover)
                        patient_names = [p['name'] for p in deleted_patients]
                        window["-Patient_List-"].update(patient_names)

                    except Exception as e:
                        sg.popup_error(f"Error recovering patient folder: {e}")
                else:
                    sg.popup("No patient Selected!", title="Error")

    window.close()
