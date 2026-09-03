# Imports
import FreeSimpleGUI as sg


def Personal_Patient_window(exisitng_data = None):

    name_default = exisitng_data.get('name', '') if exisitng_data else ''
    gender_defualt = exisitng_data.get('gender', '') if exisitng_data else ''
    dob_day = dob_month = dob_year = ''

    if exisitng_data and 'DOB' in exisitng_data:
        try:
            dob_parts = exisitng_data['DOB'].split('/')
            dob_day = int(dob_parts[0])
            dob_month = (dob_parts[1])
            dob_year = int(dob_parts[2])
        except Exception:
            pass

    # title
    title = [
        sg.Text("Personal Patient\nInformation", font=('Segoe UI', 35), text_color='#2A7FA2', pad=(0, 0),
                background_color='#F7F9FB')
    ]

    # Patient Name
    patient_name = [
        [sg.Text("Patient's Name", font=('Segoe UI', 12, 'bold'), text_color='#2D2D2D', background_color='#F7F9FB')],
        [sg.InputText(name_default,  background_color='#F7F9FB', key='-Name-')]
    ]

    # Patient Gender
    patient_gender = [
        [sg.Text("Patient's Gender", font=('Segoe UI', 12, 'bold'), text_color='#2D2D2D', background_color='#F7F9FB')],
        [sg.Combo(["Male", "Female", "Other"], default_value=gender_defualt, size=(7, 1), readonly=True,
                  background_color='#F7F9FB', key="-Gender-")]
    ]

    # Patient DOB
    patient_DOB = [
        [sg.Text("Patient's Date of Birth", font=('Segoe UI', 12, 'bold'), text_color='#2D2D2D',
                 background_color='#F7F9FB')],
        [
            sg.Combo(list(range(1, 32)), default_value=dob_day, size=(5, 1), readonly=True,
                     font=('Segoe UI', 12), text_color='#2D2D2D', background_color='#F7F9FB', key='-Day-'),
            sg.Combo(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
                     default_value=dob_month, size=(7, 1), readonly=True, font=('Segoe UI', 12),
                     text_color='#2D2D2D', background_color='#F7F9FB', key="-Month-"),
            sg.Combo(list(range(1900, 2025)), default_value=dob_year, size=(7, 1), readonly=True,
                     font=('Segoe UI', 12), text_color='#2D2D2D', background_color='#F7F9FB', key="-Year-")
        ]
    ]

    # Patient Insurance
    patient_insurance = [
        [sg.Button("Patient's Insurance Details", size=(100, 2), button_color=('#2D2D2D', '#E0E0E0'),
                   font=('Segoe UI', 12, 'bold'), key='-Insurance-')]

    ]

    # Layout
    button = [
        [sg.Push(background_color='#F7F9FB'),
            sg.Button("Save", size=(15, 2), button_color=('white', '#2A7FA2'), font=('Segoe UI', 12, 'bold'),
                   key='-Save-'),
         sg.Button("Back", size=(15, 2), button_color=('#2D2D2D', '#E0E0E0'), font=('Segoe UI', 12, 'bold'),
                    key='-Back-'),
         sg.Push(background_color='#F7F9FB')
         ]
    ]

    layout = [
        [sg.Column([title], background_color='#F7F9FB')],
        [sg.Column(patient_name, background_color='#F7F9FB')],
        [sg.Column(patient_DOB, background_color='#F7F9FB')],
        [sg.Column(patient_gender, background_color='#F7F9FB')],
        [sg.Column(patient_insurance, background_color='#F7F9FB')],
        [button]
    ]

    # creating window
    window = sg.Window('Patient Personal Information', layout, use_default_focus=False, resizable=True,
                       background_color='#F7F9FB',size=(400, 600))

    patient_personal_data = exisitng_data.copy() if exisitng_data else {}

    # Event Loop
    while True:
        # Exit
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break

        # Insurance window
        if event == '-Insurance-':
            sg.popup('Patient Insurance Details')  # placeholder due to limitation

        # creating a dictionary of personal data
        if event == '-Save-':

            # Checking that all areas are filled
            if values['-Name-'] == '' or values['-Day-'] == '' or values['-Month-'] == '' or values['-Year-'] == '' or \
                    values['-Gender-'] == '':
                sg.popup_error('Make sure all areas are filled in first!')
                continue

            # Saving data
            patient_personal_data = ({
                'name': values['-Name-'],
                'DOB': f"{values['-Day-']}{"/"}{values['-Month-']}{"/"}{values['-Year-']}",
                'gender': values['-Gender-'],
                'insurance': patient_personal_data.get('insurance', 'to be filled')  # limitation/placeholder
            })
            break

        # Back
        if event == '-Back-':
            break

    # closing window
    window.close()
    return patient_personal_data # uses data as if it's in a dictionary rather than a function
