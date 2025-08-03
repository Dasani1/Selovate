import easygui

import json
import os

from tkinter import Tk
from tkinter.filedialog import askopenfilename, askdirectory
Tk().withdraw()  # Hide the root window


easygui.msgbox("Find the folder of the images.", "Selovate - Trainer")
folder_path = askdirectory(title="Selovate - Trainer")

easygui.msgbox("Find the answer.json you generated.", "Selovate - Trainer")
file_path = askopenfilename(title="Selovate - Trainer")

import train
model, losses, correct_rate, model_info = train.train((folder_path, file_path))


seeProgress = easygui.choicebox("Training finished!\nSee Progress?", "Selovate - Trainer", choices=["Continue", "Skip"])
if seeProgress == "Continue":
    import matplotlib.pyplot as plt
    plt.plot([j for i in losses for j in i], label='Loss')
    plt.legend()
    plt.title('Training Progress')
    plt.show()

easygui.msgbox("Select a folder to save your models.", "Selovate - Trainer")
folder_path = askdirectory(title="Selovate - Trainer")

json.dump(model_info, open(os.path.join(folder_path, "info.json"), "w"), indent=4)
train.torch.save(model.state_dict(), os.path.join(folder_path, "model.pth"))

easygui.msgbox("Finished :)!", "Selovate - Trainer")
