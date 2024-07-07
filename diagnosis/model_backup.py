# import numpy as np
# from PIL import Image
# import pickle

# with open("pickle_model_new.pkl", 'rb') as file:
#     model = pickle.load(file)

# read = lambda imname: np.asarray(Image.open(imname).convert("RGB").resize((224, 224)))


# def predict(image_path):
#     ims_benign = [read(image_path)]
#     picture = np.array(ims_benign, dtype='uint8')
#     picture = picture / 255
#     return 'malignant' if model.predict(picture.reshape(1,-1))[0] == 1 else 'benign'

# if __name__ == '__main__':
#     print(predict('./data/test/benign/1800.jpg'))


from PIL import Image

import torch
from torchvision import models, transforms
import torch.nn as nn
from torch.nn import functional as F
import torch.optim as optim


normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225])

data_transforms = transforms.Compose([
        transforms.Resize((224,224)),
        transforms.ToTensor(),
        normalize
    ])

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

model = models.resnet50(pretrained=False).to(device)
model.fc = nn.Sequential(
               nn.Linear(2048, 128),
               nn.ReLU(inplace=True),
               nn.Linear(128, 7)).to(device)
model.load_state_dict(torch.load('weights.h5', map_location='cpu'))

optimizer = optim.Adam(model.fc.parameters())


classes = ['Actinic Keratoses',
 'Basal Cell Carcinoma',
 'Benign Keratosis Like Lesions',
 'Dermatofibroma',
 'Melanocytic Nevi',
 'Melanoma',
 'Vascular Lesions']


def predict(image_path):
    img = Image.open(image_path)
    validation_batch = torch.stack([data_transforms(img).to(device)])
    pred_logits_tensor = model(validation_batch)
    pred_probs = F.softmax(pred_logits_tensor, dim=1).cpu().data.numpy()
    return dict(zip(classes, pred_probs.flatten()))
