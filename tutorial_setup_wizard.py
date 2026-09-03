import shutil
import FreeSimpleGUI as sg
import os
from PIL import Image, ImageOps

screen_width, screen_height = sg.Window.get_screen_size()
target_image_size = (int(screen_width * 0.55), int(screen_height * 0.45))


# getting image from folder
def load_tutorial_images():
    base_dir = 'tutorial_images'
    image_paths = {}

    if os.path.exists('temp_resized'):
        shutil.rmtree('temp_resized')
    os.makedirs('temp_resized', exist_ok=True)

    for step in range(3):
        step_folder = os.path.join(base_dir, f'step_{step}')

        if os.path.exists(step_folder):
            images = [f for f in os.listdir(step_folder) if f.lower().endswith('.png')]
            images.sort()
            renamed_images = []

            for index, image_file in enumerate(images):
                original_path = os.path.join(step_folder, image_file)
                new_filename = f"{step}_{index + 1}.png"
                resized_path = image_format(original_path, new_filename)
                renamed_images.append(resized_path)

            image_paths[step] = renamed_images

        else:
            image_paths[step] = []

    return image_paths


# standardise images
def image_format(image_path, new_filename, target_size=target_image_size):
    image = Image.open(image_path)
    image = ImageOps.contain(image, target_size, method=Image.BICUBIC)
    padded = Image.new("RGB", target_size, (255, 255, 255))
    offset = ((target_size[0] - image.width) // 2, (target_size[1] - image.height) // 2)
    padded.paste(image, offset)

    output_dir = 'temp_resized'
    os.makedirs(output_dir, exist_ok=True)

    temp_path = os.path.join(output_dir, new_filename)
    padded.save(temp_path)
    return temp_path


# layout and stuff
def launch_tutorial():
    tutorial_images = load_tutorial_images()
    step_index = 0
    image_index = 0

    def step_text(index):
        step_texts = [
            # 1
            """The fist step to setting your patient information file location is to open file explorer. This is done by going to search bar and typing 'File Explorer'. Then pressing enter or clicking the yellow folder named 'File Explorer', alternatively you can also press the open button marked in the image tutorial.""",

            # 2
            """The second step is to now head over too where you want to store your patient's data. If you already have a folder that you want the data to go into then use the search bar in the top right and search for that folder. Otherwise, using the icons and the side bar found on the left, navigate your way to where you want it to save to. The below image tutorial will provide an example to navigating to an 'Example' folder located in the d: drive.""",

            # 3
            """Finally, the third and last step is to copy the file path (the link like thing in the top centre) and paste this in the text box of this transcriber"""
        ]
        return step_texts[index] if index < len(step_texts) else "No step text available"

    def get_layout():
        image_list = tutorial_images[step_index]
        current_image = image_list[image_index] if image_list else None
        multi_image = len(image_list) > 1
        image_count = ''.join(['●' if i == image_index else '○' for i in range(len(image_list))]) if multi_image else ""

        image_elem = sg.Image(filename=current_image, size=target_image_size, pad=(0, 0), key='-image-')

        nav_buttons = [
            sg.Button("Back", size=(15, 2), button_color=('#2D2D2D', '#E0E0E0'), font=('Segoe UI', 12, 'bold'),
                      key='-back-'),
            sg.Push(background_color='#F7F9FB'),
            sg.Button("Next", visible=step_index < len(tutorial_images) - 1, size=(15, 2),
                      button_color=('white', '#2A7FA2'), font=('Segoe UI', 12, 'bold'),
                      key='-next-'),
            sg.Button("Finish", visible=step_index == len(tutorial_images) - 1, size=(15, 2),
                      button_color=('white', '#2A7FA2'), font=('Segoe UI', 12, 'bold'), key='-finish-')

        ]
        return [
            [sg.Text(step_text(step_index), size=(80, 5), expand_x=True, font=('Segoe UI', 12), text_color='#2D2D2D',
                     justification='centre', key='-step_text-', background_color='#F7F9FB')],
            [sg.Text("Ignore the grey bars, they are added for privacy reasons", justification='centre',
                     expand_x=True, font=('Segoe UI', 10), text_color='#666666', background_color='#F7F9FB')],
            [
                sg.Button("<", visible=multi_image, button_color=('black', '#D3D3D3'), size=(3, 2), key='-prev_img-'),
                image_elem,
                sg.Button(">", visible=multi_image, button_color=('black', '#D3D3D3'), size=(3, 2), key='-next_img-')
            ],
            [sg.Text(image_count, justification='centre', expand_x=True, font=('Segoe UI', 12), text_color='#888888',
                     key='-img_count-', background_color='#F7F9FB')],
            [sg.HorizontalSeparator()],
            [*nav_buttons]
        ]

    container_layout = [[sg.Column(get_layout(), expand_x=True, expand_y=True, background_color='#F7F9FB',
                                   key='-container')]]
    window = sg.Window('Tutorial', container_layout, finalize=True, resizable=True, element_justification='centre',
                       background_color='#F7F9FB', size=(target_image_size[0] + 120, target_image_size[1] + 300))

    while True:
        # exit
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == '-finish-':
            break

        if event == '-next-':
            if step_index < len(tutorial_images) - 1:
                step_index += 1
                image_index = 0

        elif event == '-back-':
            if step_index == 0:
                break
            else:
                step_index -= 1
                image_index = 0

        elif event == '-next_img-':
            if image_index < len(tutorial_images[step_index]) - 1:
                image_index += 1

        elif event == '-prev_img-':
            if image_index > 0:
                image_index -= 1

        img_list = tutorial_images[step_index]
        current_image = img_list[image_index] if img_list else None
        multi_img = len(img_list) > 1
        img_count = ''.join(['●' if i == image_index else '○' for i in range(len(img_list))]) if multi_img else ""

        window['-step_text-'].update(step_text(step_index))
        window['-image-'].update(filename=current_image)
        window['-prev_img-'].update(visible=multi_img)
        window['-next_img-'].update(visible=multi_img)
        window['-next-'].update(visible=step_index < len(tutorial_images) - 1)
        window['-finish-'].update(visible=step_index == len(tutorial_images) - 1)
        window['-img_count-'].update(img_count)

    window.close()
