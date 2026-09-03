from moviepy.editor import VideoFileClip
import os

# Directories
input_folder = "loading_bar_gifs"
output_folder = "loading_bar_gifs_scaled"
scale_factor = 0.5  # 50% size

os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    if filename.lower().endswith(".gif"):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        clip = VideoFileClip(input_path)
        resized_clip = clip.resize(scale_factor)

        # Save with good quality (preserves smoothness and palette)
        resized_clip.write_gif(output_path, program='ffmpeg', fps=clip.fps)

        print(f"Saved resized GIF: {filename}")
