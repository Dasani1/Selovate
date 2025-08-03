import os
import json
from PIL import Image
from torch.utils.data import Dataset
import random

class SingleFolderJsonAnswer(Dataset):
    def __init__(self, img_folder, labels_json, data_num, transform=None):
        with open(labels_json, 'r') as f:
            self.labels_dict = json.load(f)

        self.image_names = list(self.labels_dict.keys())
        random.shuffle(self.image_names)

        if data_num > 0:
            self.image_names = self.image_names[0:data_num]
        else:
            data_num = len(self.image_names)
        self.data_num = data_num
        
        self.img_folder = img_folder
        self.transform = transform

        # Create a class-to-index mapping
        self.classes = sorted(set(self.labels_dict.values()))
        self.class_to_idx = {cls: idx for idx, cls in enumerate(self.classes)}

    def __len__(self):
        return len(self.image_names)

    def __getitem__(self, idx):
        img_name = self.image_names[idx]
        img_path = os.path.join(self.img_folder, img_name)

        image = Image.open(img_path+".png").convert('RGB')
        label = self.class_to_idx[self.labels_dict[img_name]]

        if self.transform:
            image = self.transform(image)

        return image, label
