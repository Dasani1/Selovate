
import loadData
import math
import copy

import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import transforms, models
from torch.utils.data import DataLoader, random_split



def train(data_path, imageSize = (224, 224), data_size = -1, batch_size = -1, test = 0.2, learning_rate = 0.0001, epoch_num = 8):
    # image normalizer designed for resnet18
    transform = transforms.Compose([
        transforms.Resize(imageSize),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
    ])

    # load data, if data_size is below zero it uses all we got
    full_dataset = loadData.SingleFolderJsonAnswer(*data_path, data_size, transform=transform)
    data_size = full_dataset.data_num
    if batch_size < 0:
        batch_size = math.ceil(data_size / 32)
    # if user wanna do testing then have test data, or else don't prepare it at all
    if test > 0:
        train_size = round(data_size * (1 - test))
        val_size = data_size - train_size

        train_data, val_data = random_split(full_dataset, [train_size, val_size])
        train_loader = DataLoader(train_data, batch_size = batch_size, shuffle=True)
        val_loader = DataLoader(val_data, batch_size = batch_size)
    else:
        train_size = data_size
        train_data = full_dataset
        train_loader = DataLoader(train_data, batch_size = batch_size, shuffle=True)

    # preparing model
    model = models.resnet18(pretrained=True)
    model.fc = nn.Linear(model.fc.in_features, len(full_dataset.classes))
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)

    # lost (bro this learning rate is killing me)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)

    # training loop by gpt
    losses = [[1]]
    best_model = copy.deepcopy(model)
    for epoch in range(epoch_num):
        losses_epoch = []

        model.train()
        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)

            outputs = model(images)                # model makes predictions
            loss = criterion(outputs, labels)      # calculate how wrong it is
            if min([j for i in losses for j in i]) < loss.item():
                best_model = copy.deepcopy(model)
            losses_epoch.append(loss.item())

            optimizer.zero_grad()                  # clear old gradients
            loss.backward()                        # compute gradients
            optimizer.step()                       # update weights

        losses.append(losses_epoch)
        print(f'Epoch {epoch+1} done')
    model = best_model
    # testing section
    correct=0
    incorrect=0

    if test > 0:
        model.eval()
        with torch.no_grad():
            for images, labels in val_loader:
                images, labels = images.to(device), labels.to(device)
                outputs = model(images)   
                for out, label in zip(outputs,labels):
                    maxindex = torch.argmax(out)
                    if (maxindex==label):
                        correct+=1
                    else:
                        incorrect+=1


    return model, losses, (incorrect,correct), {"labels": full_dataset.classes, "image_size": imageSize, "pretrained": "resnet18"}