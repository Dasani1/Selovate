import torch
from torchvision import transforms, models

import json
from PIL import Image
import os

def load_model(model_path):
    model_info = json.load(open(os.path.join(model_path, "info.json")))

    transform = transforms.Compose([
        transforms.Resize(model_info["image_size"]),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
    ])

    model = models.resnet18()
    model.fc = torch.nn.Linear(model.fc.in_features, len(model_info["labels"]))
    model.load_state_dict(torch.load(os.path.join(model_path, "model.pth")))
    model.eval()

    def returns(image_path):
        image = Image.open(image_path).convert('RGB')
        image = transform(image).unsqueeze(0)
        with torch.no_grad():
            output = model(image)
            confidence, predicted = torch.max(output, 1)

        label = model_info["labels"][predicted.item()]
        return {"index": predicted.item(), "label": label, "confidence": confidence}
    
    return returns