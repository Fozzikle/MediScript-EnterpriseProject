import FreeSimpleGUI as sg
import Transcriber
import os
from File_Config import base_folder
from Data_Store import patient_folder_structure


def file_format(filename):
    # Converting from filename to a more ux title
    try:
        parts = filename.replace('.txt', '').split('_')
        if len(parts) >= 4:
            date = parts[2]
            time = parts[3]
            formatted = f"Consult on date: {date[:2]}/{date[2:4]}/20{date[4:]} at {time[:2]}:{time[2:4]}:{time[4:]}"
            return formatted
    except Exception as e:
        print(f"Error formatting filename: {e}")
    return filename


def Patient_view_window(patient_data):
    # defining file locations
    patient_name = patient_data['name']
    folder = patient_folder_structure(patient_name, base_folder())
    transcriptions_path = folder['transcriptions']
    processed_path = folder['processed']

    # logic for list box
    consult_files = []
    display_mapping = {}

    if os.path.exists(processed_path):
        for file in os.listdir(processed_path):
            if file.startswith('transcription_cleaned_') and file.endswith('.txt'):
                display_name = file_format(file)
                consult_files.append(display_name)
                display_mapping[display_name] = file  # connects new name to file name

    # title
    title = [sg.Text("Patient View", font=('Segoe UI', 35, 'bold'), text_color='#2A7FA2',
                     background_color='#F7F9FB')]

    # pp data
    pp_data = [sg.Column(
        layout=[
            [sg.Text("Patient Name: ", font=('Segoe UI', 12, 'bold'), text_color='#2D2D2D',
                     background_color='#F7F9FB'),
             sg.Text(patient_data['name'], font=('Segoe UI', 12), text_color='#2D2D2D',
                     background_color='#F7F9FB')],
            [sg.Text("DOB: ", font=('Segoe UI', 12, 'bold'), text_color='#2D2D2D',
                     background_color='#F7F9FB'),
             sg.Text(patient_data['DOB'], font=('Segoe UI', 12), text_color='#2D2D2D',
                     background_color='#F7F9FB')],
            [sg.Text("Gender: ", font=('Segoe UI', 12, 'bold'), text_color='#2D2D2D',
                     background_color='#F7F9FB'),
             sg.Text(patient_data['gender'], font=('Segoe UI', 12), text_color='#2D2D2D',
                     background_color='#F7F9FB')],
            [sg.Text("Insurance: ", font=('Segoe UI', 12, 'bold'), text_color='#2D2D2D',
                     background_color='#F7F9FB'),
             sg.Text(patient_data['insurance'], font=('Segoe UI', 12), text_color='#2D2D2D',
                     background_color='#F7F9FB')]
        ],
        background_color='#F7F9FB'
    )]

    # Layout + personal data collection
    layout = [
        [sg.Column([title], justification='centre', background_color='#F7F9FB')],
        [sg.Column([pp_data], justification='left', background_color='#F7F9FB')],

        [sg.Text("Past Consultations", font=('Segoe UI', 13, 'bold'), text_color='#2D2D2D',
                 background_color='#F7F9FB', pad=(5, (20, 5)))],
        [sg.Column([
            [sg.Listbox(values=consult_files, size=(70, 6), key="-consult_list-",
                        select_mode=sg.LISTBOX_SELECT_MODE_SINGLE, font=('Segoe UI', 11), expand_x=True,
                        highlight_background_color='#2A7FA2', background_color='white')]
        ], justification='left', background_color='#F7F9FB')],
        [sg.Button("Start new consultation", size=(17, 1), button_color=('white', '#2A7FA2'),
                   font=('Segoe UI', 12, 'bold'), key='-Transcribe-')]
    ]

    # creating the window
    window = sg.Window('Patient View', layout, use_default_focus=False, resizable=True, background_color='#F7F9FB',
                       size=(500, 600))

    # event loop
    while True:
        # exit
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break

        # Start transcriber
        elif event == '-Transcribe-':
            Transcriber.transcription_window(transcriptions_path)

        # Show/view past consultations
        elif event == '-consult_list-':
            selected_consult = values['-consult_list-'][0]
            real_filename = display_mapping[selected_consult]
            real_path = os.path.join(processed_path, real_filename)
            os.startfile(real_path)

    window.close()
