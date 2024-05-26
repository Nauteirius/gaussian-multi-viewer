import webbrowser
import gradio as gr
import os

# Define a function to list files in a directory
def list_files(directory):
    try:
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    except FileNotFoundError:
        files = []
    return files

# Define the function to update the HTML file with the chosen filename
def update_html(file):
    if file:
        html_file_path = os.path.join(current_directory, 'example.html')
        try:
            with open(html_file_path, 'w') as html_file:
                html_file.write(f"<html><body><p>Selected file: {file}</p></body></html>")
            result = f"Updated HTML with {file}"
        except Exception as e:
            result = f"Failed to update HTML file: {e}"
    else:
        result = "No file selected"
    return result


# Define the function to update the JS file with the chosen file path
def update_js(file):
    if file:
        viewer_directory = os.path.join(current_directory, 'splat-main')
        js_file_path = os.path.join(viewer_directory, 'main.js')



        
        try:
            with open(js_file_path, 'r') as js_file:
                js_content = js_file.read()

            # Define the old block and new block
            old_block = '''const url = new URL(
        // "nike.splat",
        // location.href,
        params.get("url") || "train.splat",
        "https://huggingface.co/datasets/bati22/splats-gs-neg-games/resolve/main/",
    );'''
            new_block = f'''const url = new URL(
        // "nike.splat",
        // location.href,
        params.get("url") || "{file}",
        "https://huggingface.co/cakewalk/splat-data/resolve/main/",
    );'''
            # Replace the target line with the new line containing the selected file path
            new_line = f'params.get("url") || "{file}",'
            new_js_content = '\n'.join(
                [line if i + 1 != 749 else new_line for i, line in enumerate(js_content.split('\n'))]
            )
            # Replace the old block with the new block
            #new_js_content = js_content.replace(old_block, new_block)

            with open(js_file_path, 'w') as js_file:
                js_file.write(new_js_content)

            # Open the HTML file in the browser
            html_file_path = os.path.join(viewer_directory, 'index.html')
            webbrowser.open(html_file_path)

            result = f"Updated JS with {file} and opened HTML in browser"
        except Exception as e:
            result = f"Failed to update JS file or open HTML file: {e}"
    else:
        result = "No file selected"
    return result


# Define the function to run the command (dummy function for this example)
def run_command(file):
    if file:
        # Replace this with the actual command or function you need to run
        result = f"Running command on {file}"
    else:
        result = "No file selected"
    return result

# Define functions to run scripts using the selected folder path
def run_script1(folder_path):
    # Replace this with the actual script or function you need to run
    result = f"Running script 1 on {folder_path}"
    return result

def run_script2(folder_path):
    # Replace this with the actual script or function you need to run
    result = f"Running script 2 on {folder_path}"
    return result

#def refresh_videos():
#    return gr.Dropdown.update(choices=list_videos(video_directory))

# Define a function to list video files in a directory
def list_videos(directory):
    try:
        videos = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and f.endswith(('.mp4', '.avi', '.mov', '.mkv'))]
    except FileNotFoundError:
        videos = []
    return videos

current_directory = os.getcwd()
video_directory = os.path.join(current_directory, 'videos')
positive_directory = os.path.join(current_directory, 'positive')
negative_directory = os.path.join(current_directory, 'negative')
# Gradio interface
with gr.Blocks() as demo:
    with gr.Tabs():
        with gr.TabItem("Vanilia"):
            gr.Markdown("### Select a file")
            
            # Select directory
            #directory = gr.Textbox(label="Directory Path", placeholder="Enter the directory path", value=".")
            current_directory = os.getcwd()
            vanilla_directory = os.path.join(current_directory, 'vanilla')
            # Dropdown to select file
            file_dropdown = gr.Dropdown(choices=list_files(vanilla_directory), label="Select a File")

            
            # Button to refresh file list
            def refresh_files(directory):
                return gr.update(choices=list_files(directory))
            
            #refresh_button = gr.Button("Refresh File List")
            #refresh_button.click(gr.update(choices=list_files(vanilla_directory)), outputs=file_dropdown)
            #refresh_button.click(refresh_files, inputs=True, outputs=file_dropdown)
            
            # Button to run the command
            #run_button = gr.Button("Run Command")
            #update_button = gr.Button("Update HTML")
            #result_output = gr.Textbox(label="Output")
            #update_button.click(update_html, inputs=file_dropdown, outputs=result_output)
            #run_button.click(run_command, inputs=file_dropdown, outputs=result_output)

            # Button to update the JS file
            update_js_button = gr.Button("Display")
            js_result_output = gr.Textbox(label="Output")
            
            update_js_button.click(update_js, inputs=file_dropdown, outputs=js_result_output)

        with gr.TabItem("Negative gaussian"):
            gr.Markdown("### Select a file")
            
            # Toggle for coloring negative gauss
            coloring_toggle = gr.Checkbox(label="Coloring Negative Gaussians")


            # Function to refresh file list based on toggle state
            def refresh_js_files(coloring):
                directory = negative_directory if coloring else positive_directory
                return gr.update(choices=list_files(directory))
            
            refresh_js_files(False)
            # Dropdown to select file
            js_file_dropdown = gr.Dropdown(label="Select a File")


            
            # Button to refresh file list
            refresh_js_files_button = gr.Button("Refresh File List")
            refresh_js_files_button.click(refresh_js_files, inputs=coloring_toggle, outputs=js_file_dropdown)

            
            # Automatically refresh file list when toggle changes
            coloring_toggle.change(refresh_js_files, inputs=coloring_toggle, outputs=js_file_dropdown)

            # Set default file list based on initial toggle state
            #initial_state = coloring_toggle.value


            # Button to update the JS file
            update_js_button = gr.Button("Display")
            js_result_output = gr.Textbox(label="Output")
            
            update_js_button.click(update_js, inputs=js_file_dropdown, outputs=js_result_output)

        
        with gr.TabItem("GaMeS"):
            gr.Markdown("### Select a file")
            
            # Select video from the specified directory
            current_directory = os.getcwd()
            video_directory = os.path.join(current_directory, 'videos')
            
            # Dropdown to select video
            video_dropdown = gr.Dropdown(choices=list_videos(video_directory), label="Select a Video")
            
            # Button to refresh video list
            def refresh_videos(directory):
                return gr.update(choices=list_videos(directory))
            
            #refresh_video_button = gr.Button("Refresh Video List")
            #refresh_video_button.click(refresh_videos, inputs=None, outputs=video_dropdown)
            
            # Button to display the video
            def display_video(video_file):
                video_path = os.path.join(video_directory, video_file)
                return video_path

            display_video_button = gr.Button("Display Video")
            video_output = gr.Video()
            
            display_video_button.click(display_video, inputs=video_dropdown, outputs=video_output)

# Launch the Gradio app
demo.launch()