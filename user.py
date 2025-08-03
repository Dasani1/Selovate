import easygui

from tkinter import Tk
from tkinter.filedialog import askopenfilename, askdirectory
Tk().withdraw()  # Hide the root window


easygui.msgbox("Find the folder of the Model.", "Selovate - User")
folder_path = askdirectory(title="Selovate - User")

easygui.msgbox("Find the image you want to recognize.", "Selovate - User")
file_path = askopenfilename(title="Selovate - User")

import use

model = use.load_model(folder_path)

answer = model(file_path)


easygui.msgbox(f'Answer: {answer["label"]}', "Selovate - User")