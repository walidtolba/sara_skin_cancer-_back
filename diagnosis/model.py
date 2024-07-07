import numpy as np
import torch
import torchvision.transforms as transforms
from torchvision import models
from PIL import Image
import joblib

IMG_SIZE = 244
BATCH_SIZE = 32
joblib_file = "svm_skin_cancer_model.pkl"

data_transforms = transforms.Compose([
        transforms.Resize((IMG_SIZE, IMG_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])

model = models.vgg16(pretrained=True)
model = model.features 
model.eval()  

# Function to extract features
def extract_features(dataloader, model, dataset_size):
    features = np.zeros((dataset_size, 512 * 7 * 7))
    labels = np.zeros(dataset_size)
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model.to(device)
    with torch.no_grad():
        for i, (inputs, label) in enumerate(dataloader):
            inputs = inputs.to(device)
            output = model(inputs)
            output = output.view(output.size(0), -1)
            features[i * BATCH_SIZE:(i + 1) * BATCH_SIZE] = output.cpu().numpy()
            labels[i * BATCH_SIZE:(i + 1) * BATCH_SIZE] = label.numpy()
    return features, labels

loaded_svm = joblib.load(joblib_file)

def predict_single_image(image_path, model, svm, transform):
    # Load and preprocess the image
    image = Image.open(image_path)
    image = transform(image).unsqueeze(0)  # Add batch dimension
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    image = image.to(device)
    
    # Extract features
    with torch.no_grad():
        features = model(image)
        features = features.view(features.size(0), -1).cpu().numpy()

    # Predict the class using the SVM
    prediction = svm.predict(features)
    
    return prediction

classes = ['Actinic Keratoses',
 'Basal Cell Carcinoma',
 'Benign Keratosis Like Lesions',
 'Dermatofibroma',
 'Melanocytic Nevi',
 'Melanoma',
 'Vascular Lesions']

def predict(image_path):
    d_temp = dict(zip(classes, [0] * len(classes)))
    prediction = predict_single_image(image_path, model, loaded_svm, data_transforms)
    d_temp[classes[int(prediction[0])]] = 1
    return d_temp