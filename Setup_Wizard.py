# Imports
import FreeSimpleGUI as sg
import os
import new_patient_setup
import tutorial_setup_wizard
from File_Config import save_config, load_config
import audio_setup


# Setup Wizard Stuff
def get_step(step_index):
    # Initial landing page
    if step_index == 0:
        return [
            # Title
            [sg.Push(background_color='#F7F9FB'),
             sg.Text("Welcome to ", font=('Segoe UI', 35), text_color='#2A7FA2', pad=(0, 0),
                     background_color='#F7F9FB'),
             sg.Text("MediScript", font=('Segoe UI', 35, 'bold'), text_color='#6E7780', pad=(0, 0),
                     background_color='#F7F9FB'),
             sg.Push(background_color='#F7F9FB')],

            [sg.Column(
                layout=[
                    # Body intro
                    [sg.Push(background_color='#F7F9FB'),
                     sg.Text("We are excited to guide you through the setup process. This tool is designed\n"
                             "to streamline your transcription and patient workflow.",
                             font=('Segoe UI', 13), text_color='#2D2D2D', background_color='#F7F9FB'),
                     sg.Push(background_color='#F7F9FB')],

                    # body dp
                    [sg.Column(
                        layout=[[sg.Frame(
                            title="What This Setup Will Cover:",
                            layout=[
                                [sg.Text("• Configuration of patient data folder", font=('Segoe UI', 12),
                                         text_color='#2D2D2D', background_color='#F7F9FB')],
                                [sg.Text("• Configuration of transcription tools", font=('Segoe UI', 12),
                                         text_color='#2D2D2D', background_color='#F7F9FB')],
                                [sg.Text("• Configuration of patient registration", font=('Segoe UI', 12),
                                         text_color='#2D2D2D', background_color='#F7F9FB')]
                            ], font=('Segoe UI', 12, 'bold'), title_color='#2A7FA2', border_width=1,
                            relief=sg.RELIEF_FLAT, background_color='#F7F9FB', pad=((0, 0), (0, 0))
                        )]],
                        element_justification='left', expand_x=True, background_color='#F7F9FB', pad=((60, 0), (20, 0))
                    )],

                    # body conc
                    [sg.Column(
                        layout=[[
                            sg.Text(
                                "These steps ensure your system is fully prepared. By the end of setup, you will have\n"
                                "a configured workspace ready to assist with transcription and documentation tasks.",
                                font=('Segoe UI', 12), text_color='#2D2D2D', justification='left', pad=(50, 20),
                                expand_x=True, background_color='#F7F9FB'
                            )]],
                        background_color='#F7F9FB'
                    )]
                ],
                background_color='#F7F9FB'
            )],

            # Buttons
            [sg.Push(background_color='#F7F9FB'),
             sg.Button("Begin Setup", size=(12, 1), button_color=('white', '#2A7FA2'), font=('Segoe UI', 12, 'bold'),
                       key='-next-'),
             sg.Button("Exit", size=(12, 1), button_color=('#2D2D2D', '#E0E0E0'), font=('Segoe UI', 12, 'bold'),
                       key='-Finish-'),
             sg.Push(background_color='#F7F9FB')]
        ]

    # Check if there is a database that this needs to connect to
    elif step_index == 1:
        return [
            # title
            [sg.Push(background_color='#F7F9FB'),
             sg.Text('Database Connection Setup', font=('Segoe UI', 35, 'bold'), text_color='#2A7FA2', pad=(0, 0),
                     background_color='#F7F9FB'),
             sg.Push(background_color='#F7F9FB')],

            # spacer
            [sg.Text("", pad=(0, 0), background_color='#F7F9FB')],

            # body
            [sg.Column(
                layout=[
                    # text
                    [
                        sg.Push(background_color='#F7F9FB'),
                        sg.Text("Do you have a pre-existing patient database that you would like to use?",
                                font=('Segoe UI', 12), text_color='#2D2D2D', background_color='#F7F9FB'),
                        sg.Push(background_color='#F7F9FB')
                    ],

                    # buttons
                    [
                        sg.Push(background_color='#F7F9FB'),
                        sg.Button("yes", size=(15, 2), button_color=('white', '#2A7FA2'), font=('Segoe UI', 12, 'bold'),
                                  key='-Ydata-'),
                        sg.Button("No", size=(15, 2), button_color=('#2D2D2D', '#E0E0E0'),
                                  font=('Segoe UI', 12, 'bold'),
                                  key='-Ndata-'),
                        sg.Push(background_color='#F7F9FB')
                    ]
                ],
                expand_x=True, background_color='#F7F9FB', pad=((0, 0), (10, 10))
            )],
        ]
    # left like this rather than popup incase in future want to add this feature
    elif step_index == 2:
        return [
            # title
            [sg.Push(background_color='#F7F9FB'),
             sg.Text('Under Construction!', font=('Segoe UI', 35, 'bold'), text_color='#2A7FA2', pad=(0, 0),
                     background_color='#F7F9FB'),
             sg.Push(background_color='#F7F9FB')],

            # spacer
            [sg.Text("", pad=(0, 0), background_color='#F7F9FB')],

            # body
            [sg.Column(
                layout=[[
                    sg.Push(background_color='#F7F9FB'),
                    sg.Text("We understand that some users may already have patient data they'd like to bring into\n"
                            "MediScript. While this feature is apart of the future of MediScript, it is not yet "
                            "available\n"
                            "in this version.\n\n"
                            "We are sorry for the inconvenience and appreciate your patience as we update and improve\n"
                            "this application.\n\n"
                            "For now, you can still move forward strongly! MediScript will store all new patient data\n"
                            "locally, in a secure folder of you your choice. This ensure your information remains safe "
                            "and fully accessible\n\n"
                            "When you are ready, click Continue to proceed with setting up MediScript",
                            font=('Segoe UI', 12), text_color='#2D2D2D', background_color='#F7F9FB'),
                    sg.Push(background_color='#F7F9FB')
                ]],
                expand_x=True, background_color='#F7F9FB', pad=((60, 60), (10, 10))
            )],

            # buttons
            [sg.Column(
                layout=[[
                    sg.Push(background_color='#F7F9FB'),
                    sg.Button("Continue", size=(15, 2), button_color=('white', '#2A7FA2'),
                              font=('Segoe UI', 12, 'bold'),
                              key='-continue-'),
                    sg.Push(background_color='#F7F9FB')
                ]],
                expand_x=True, background_color='#F7F9FB', pad=((0, 0), (25, 10))
            )],
        ]

    # Choosing File Locations
    elif step_index == 3:
        return [
            # title
            [sg.Push(background_color='#F7F9FB'),
             sg.Text('Setting File Location', font=('Segoe UI', 35, 'bold'), text_color='#2A7FA2', pad=(0, 0),
                     background_color='#F7F9FB'),
             sg.Push(background_color='#F7F9FB')],

            # body
            [sg.Column(
                layout=[

                    # text
                    [
                        sg.Push(background_color='#F7F9FB'),
                        sg.Text("We are now going to determine where patient information will be store.\n"
                                "To achieve this, you will enter below the file path to where you would like this data "
                                "to be\n"
                                "stored on your machine. MediScript will then create a folder called 'Patient Data'. "
                                "Here\n"
                                "individual folders of each patient will be created. Inside, patient information will "
                                "be stored\n"
                                "along with the transcriptions and audio recordings of their consults",
                                font=('Segoe UI', 12), text_color='#2D2D2D', background_color='#F7F9FB'),
                        sg.Push(background_color='#F7F9FB')
                    ],

                    # input bar
                    [
                        sg.Push(background_color='#F7F9FB'),
                        sg.InputText("Enter file path here", font=('Segoe UI', 12), text_color='#2D2D2D',
                                     background_color='#F7F9FB', key='-path-'),
                        sg.Push(background_color='#F7F9FB')
                    ],

                    # buttons
                    [
                        sg.Push(background_color='#F7F9FB'),
                        sg.Button("Tutorial", size=(15, 2), button_color=('#2D2D2D', '#E0E0E0'),
                                  font=('Segoe UI', 12, 'bold'),
                                  key='-tutorial-'),
                        sg.Push(background_color='#F7F9FB'),
                        sg.Button("Next", size=(15, 2), button_color=('white', '#2A7FA2'),
                                  font=('Segoe UI', 12, 'bold'),
                                  key='-next-'),
                        sg.Push(background_color='#F7F9FB'),
                    ],
                ],
                expand_x=True, background_color='#F7F9FB', pad=((60, 60), (10, 10))
            )],
        ]

    # config to improve audio clarity
    elif step_index == 4:
        return [
            # title
            [sg.Push(background_color='#F7F9FB'),
             sg.Text('Setting File Location', font=('Segoe UI', 35, 'bold'), text_color='#2A7FA2', pad=(0, 0),
                     background_color='#F7F9FB'),
             sg.Push(background_color='#F7F9FB')],

            # body- text + agc
            [sg.Column(
                layout=[
                    [
                        sg.Push(background_color='#F7F9FB'),
                        sg.Text("Now, lets run a microphone test to ensure it is in the most optimal position, "
                                "angle, and\n"
                                "distance for clear and consistent transcriptions, whether you are seated, "
                                "standing, or\n"
                                "moving within the room.",
                                font=('Segoe UI', 12), text_color='#2D2D2D', background_color='#F7F9FB'),
                        sg.Push(background_color='#F7F9FB')
                    ],

                    [
                        sg.Text("Would you like to Automatic Gain Control (AGC)? This will help\n"
                                "improve voice clarity during transcription",
                                font=('Segoe UI', 12), text_color='#2D2D2D', background_color='#F7F9FB'),
                        sg.Push(background_color='#F7F9FB')
                    ],

                    [
                        sg.Checkbox("Enable AGC (recommended)",
                                    font=('Segoe UI', 12), text_color='#2D2D2D', background_color='#F7F9FB'),
                        sg.Push(background_color='#F7F9FB')
                    ],

                    # buttons
                    [
                        sg.Push(background_color='#F7F9FB'),
                        sg.Button("Microphone Calibration", size=(15, 2), button_color=('#2D2D2D', '#E0E0E0'),
                                  font=('Segoe UI', 12, 'bold'),
                                  key='-mic_test-'),
                        sg.Push(background_color='#F7F9FB'),
                        sg.Button("Next", size=(15, 2), button_color=('white', '#2A7FA2'),
                                  font=('Segoe UI', 12, 'bold'),
                                  key='-next-'),
                        sg.Push(background_color='#F7F9FB'),
                    ],
                ], background_color='#F7F9FB', pad=((60, 60), (10, 10))
            )]
        ]
    # Patient Information
    elif step_index == 5:
        return [
            # title
            [sg.Push(background_color='#F7F9FB'),
             sg.Text('Add Patient Details', font=('Segoe UI', 35, 'bold'), text_color='#2A7FA2', pad=(0, 0),
                     background_color='#F7F9FB'),
             sg.Push(background_color='#F7F9FB')],

            # body- text + opt out
            [sg.Column(
                layout=[
                    [
                        sg.Push(background_color='#F7F9FB'),
                        sg.Text("You can begin adding patient records using the 'Add Patient Details' button below. "
                                "If your\n"
                                "organisation plans to use MediScript with multiple patients, simply repeat this "
                                "process for\n"
                                "each one.\n\n"
                                "If your organisation has not yet implemented support for History or Clinical data "
                                "integration,\n"
                                "you can choose to hide those options during data entry by selecting the checkbox "
                                "below.",
                                font=('Segoe UI', 12), text_color='#2D2D2D', background_color='#F7F9FB'),
                        sg.Push(background_color='#F7F9FB')
                    ],

                    [
                        sg.Checkbox("Opt out of History and Clinical Data for now",
                                    font=('Segoe UI', 12), text_color='#2D2D2D', background_color='#F7F9FB'),
                        sg.Push(background_color='#F7F9FB')
                    ],

                    # buttons
                    [
                        sg.Push(background_color='#F7F9FB'),
                        sg.Button("Add Patient Details", size=(15, 2), button_color=('#2D2D2D', '#E0E0E0'),
                                  font=('Segoe UI', 12, 'bold'),
                                  key='-Patient-'),
                        sg.Push(background_color='#F7F9FB'),
                        sg.Button("Next", size=(15, 2), button_color=('white', '#2A7FA2'),
                                  font=('Segoe UI', 12, 'bold'),
                                  key='-next-'),
                        sg.Push(background_color='#F7F9FB'),
                    ],

                ], background_color='#F7F9FB', pad=((60, 60), (10, 10))
            )]
        ]

    # TOS EULA PRIVACY DISCLAIMER
    elif step_index == 6:
        def load_txt(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()

        tos_txt = load_txt("documentation/tos_draft_project.txt")
        eula_txt = load_txt("documentation/eula_draft_project.txt")
        pp_txt = load_txt("documentation/privacy_policy_draft_project.txt")
        disclaimer_txt = load_txt("documentation/disclaimer_draft_project.txt")

        return [
            # title
            [sg.Push(background_color='#F7F9FB'),
             sg.Text('Terms and Conditions', font=('Segoe UI', 35, 'bold'), text_color='#2A7FA2', pad=(0, 0),
                     background_color='#F7F9FB'),
             sg.Push(background_color='#F7F9FB')],

            [sg.Column(
                layout=[
                    # text
                    [sg.Push(background_color='#F7F9FB'),
                     sg.Text("Please review the following legal documents before proceeding",
                             font=('Segoe UI', 12), text_color='#2D2D2D', background_color='#F7F9FB'),
                     sg.Push(background_color='#F7F9FB')],

                    # condition table
                    [sg.TabGroup([[
                        sg.Tab("Disclaimer",
                               [[sg.Multiline(disclaimer_txt, size=(80, 15), disabled=True, key='-disc-')]]),
                        sg.Tab("Privacy Policy", [[sg.Multiline(pp_txt, size=(80, 15), disabled=True, key='-pp-')]]),
                        sg.Tab("End-User License Agreement (EULA)",
                               [[sg.Multiline(eula_txt, size=(80, 15), disabled=True,
                                              key='-eula-')]]),
                        sg.Tab("Terms of Service", [[sg.Multiline(tos_txt, size=(80, 15), disabled=True, key='-tos-')]])
                    ]], background_color='#F7F9FB', key='-tabgroup-', tab_location='top')],

                    # opt
                    [sg.Checkbox("I agree to all of the above terms", font=('Segoe UI', 12), text_color='#2D2D2D',
                                 background_color='#F7F9FB', key='-agree-', enable_events=True)],

                    # button
                    [sg.Push(background_color='#F7F9FB'),
                     sg.Button("Next", size=(10, 2), button_color=('white', '#2A7FA2'), font=('Segoe UI', 12, 'bold'),
                               key='-next-')]
                ], background_color='#F7F9FB', pad=((60, 60), (10, 10))
            )]
        ]

    # End Setup
    elif step_index == 7:
        return [
            # title
            [sg.Push(background_color='#F7F9FB'),
             sg.Text('Congratulations!', font=('Segoe UI', 35, 'bold'), text_color='#2A7FA2', pad=(0, 0),
                     background_color='#F7F9FB'),
             sg.Push(background_color='#F7F9FB')],

            # body
            [sg.Column(
                layout=[
                    # text
                    [sg.Text("You've successfully completed the setup for The Transcriber. \n\n"
                             "Everything is now configured and ready to use. From folder organization to transcription "
                             "tools, your system is fully prepared and optimized for smooth performance. This isn't "
                             "just the end of setup, it's the beginning of a more efficient way to work. \n\n"
                             "Take a moment to appreciate the progress you've made. When you're ready, you can start "
                             "transcribing, manage patient files, or explore the features you've just enabled. \n\n"
                             "Setup is complete. You're good to go",
                             font=('Segoe UI', 12), text_color='#2D2D2D', background_color='#F7F9FB')],

                    # finish button
                    [sg.Push(background_color='#F7F9FB'),
                     sg.Button("Finish", size=(10, 2), button_color=('white', '#2A7FA2'), font=('Segoe UI', 12, 'bold'),
                               key='-Finish-')]
                ], background_color='#F7F9FB', pad=((60, 60), (10, 10))
            )]
        ]
    pass


def run_setup_wizard():
    # Step control
    current_step = 0

    window = sg.Window("Getting Started", get_step(current_step), size=(800, 500), finalize=True,
                       background_color='#F7F9FB')

    # Event Loop
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break

        step_change = False

        # Step 0/ every time next is pressed
        if event == '-next-':
            # check if on 'Choosing file location'
            if current_step == 3:
                patient_folder = values.get('-path-', ' ').strip()
                # error page
                if not os.path.exists(patient_folder):
                    sg.popup_error(
                        "This file location is not valid! Try using the tutorial to help link a valid file location",
                        background_color='#F7F9FB')
                    continue

                # making the folder and naming it
                try:
                    data_folder = os.path.join(patient_folder, "Patient Data")
                    os.makedirs(data_folder, exist_ok=True)
                    sg.popup("Folder successfully made!", background_color='#F7F9FB')
                    save_config({"base_folder": data_folder, "setup_complete": True})
                    step_change = True
                    current_step += 1

                except Exception as e:
                    sg.popup("Failed to create folder:\n" + str(e), background_color='#F7F9FB')

            elif current_step == 4:
                agc_enabled = values.get('-agc_toggle-', True)
                config = load_config()
                config['agc_enabled'] = agc_enabled
                save_config(config)
                step_change = True
                current_step += 1

            elif current_step == 5:
                config["skip_history_clinical"] = values.get('-opt-', False)
                save_config(config)
                step_change = True
                current_step += 1

            elif current_step < 7:
                step_change = True
                current_step += 1

        elif event == '-tutorial-':
            tutorial_setup_wizard.launch_tutorial()

        elif event == '-mic_test-':
            audio_setup.mic_test_popup()

        elif event == '-Patient-':
            new_patient_setup.new_patient_window()  # runs new_patient_setup.py

        if event == '-Ydata-':
            current_step = 2  # step 1_1
            step_change = True

        elif event == '-continue-':
            current_step = 3
            step_change = True

        elif event == '-Ndata-':
            current_step = 3  # step 2
            step_change = True

        elif current_step == 6 and event == '-agree-':
            window['-next-'].update(disabled=not values['-agree-'])

        if event == '-Finish-':
            break

        # Window layout
        if step_change:
            window.close()
            window = sg.Window("Setup", get_step(current_step), size=(800, 500), finalize=True,
                               background_color='#F7F9FB')

    # Closing the window
    window.close()


# Launching main ui
def finish_setup():
    import UI
    UI.UI_window()
