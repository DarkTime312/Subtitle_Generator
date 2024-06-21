import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import subprocess
import pathlib
import threading
import sys
import os
import sv_ttk


def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def select_file():
    global video_path
    video_path = filedialog.askopenfilenames(filetypes=(('MP4 Files', '*.mp4'), ('All files', '*.*')))
    # print(video_path)
    file_path_var.set(video_path[0] if len(video_path) == 1 else 'Multiple files!')


def start_task():
    # Start the long-running task in a separate thread
    thread = threading.Thread(target=convert)
    thread.start()


def convert():
    # Define the command and arguments
    command = 'auto_subtitle'
    model = f'--model {model_var.get()}'
    srt_only = '--srt_only True'
    file = pathlib.Path(video_path[0])
    destination_path = f'-o "{str(file.parent)}"'

    # Combine the command and arguments into a single string
    for path in video_path:
        full_command = f'{command} "{path}"  {destination_path} {model} {srt_only}'
        if path:
            try:
                # Run the command
                progress.pack(pady=100)
                progress.start()
                root.update()
                root.attributes('-disabled', True)
                subprocess.run(full_command, shell=True, capture_output=True)

            except subprocess.CalledProcessError as e:
                # Handle errors in the command execution
                print(f"An error occurred: {e}")
    progress.destroy()
    root.attributes('-disabled', False)
    messagebox.showinfo("Done", "Done!")


root = tk.Tk()
root.geometry('500x500')
root.title("Sub generator")

# theme_path = resource_path('Azure/azure.tcl')
# root.tk.call('source', theme_path)
# root.tk.call("set_theme", "dark")

# root.tk.call('source', 'Azure/azure.tcl')
# root.tk.call("set_theme", "dark")

select_path_btn = ttk.Button(root, text='Select Files', command=select_file)
file_path_var = tk.StringVar()
lbl_path = ttk.Label(root, textvariable=file_path_var)

model_var = tk.StringVar(value='tiny.en')

rb_frm = ttk.Frame(root)
rb_lbl = ttk.Label(rb_frm, text='Select Model:')

rb1 = ttk.Radiobutton(rb_frm, text='Tiny', value='tiny.en', variable=model_var)
rb2 = ttk.Radiobutton(rb_frm, text='Small', value='small.en', variable=model_var)
rb3 = ttk.Radiobutton(rb_frm, text='Medium', value='medium.en', variable=model_var)

btn_convert = ttk.Button(root, text='Convert', command=start_task)
progress = ttk.Progressbar(root, length=200, mode='indeterminate')

# layout:
select_path_btn.pack(pady=20)
lbl_path.pack()
rb_lbl.pack(side='left', padx=20)
rb1.pack(anchor='w')
rb2.pack(anchor='w')
rb3.pack(anchor='w')
rb_frm.pack(pady=50)

btn_convert.pack()
sv_ttk.set_theme("dark")

root.mainloop()
