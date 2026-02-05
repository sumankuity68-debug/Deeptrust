import torch
import torch.nn as nn
from torchvision import models

class DeepTrustModel(nn.Module):
    def __init__(self, model_name='efficientnet'):
        super(DeepTrustModel, self).__init__()
        
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        if model_name == 'efficientnet':
             try:
                 weights = models.EfficientNet_B0_Weights.DEFAULT
                 self.model = models.efficientnet_b0(weights=weights)
             except:
                 # Fallback for older torchvision versions
                 self.model = models.efficientnet_b0(pretrained=True)
                 
             num_ftrs = self.model.classifier[1].in_features
             self.model.classifier[1] = nn.Linear(num_ftrs, 1)
        else:
            self.model = models.resnet50(pretrained=True)
            num_ftrs = self.model.fc.in_features
            self.model.fc = nn.Linear(num_ftrs, 1)
            
        self.sigmoid = nn.Sigmoid()
        self.to(self.device)

    def forward(self, x):
        return self.sigmoid(self.model(x))

    def predict(self, image_tensor):
        """
        Returns authenticity score (0.0 to 1.0).
        Closer to 1.0 means Fake (if trained with 1=Fake), or vice versa.
        Usually 1=Fake, 0=Real is standard for 'detection'.
        """
        self.eval()
        with torch.no_grad():
            image_tensor = image_tensor.to(self.device)
            output = self.forward(image_tensor)
            return output.item()

def get_model():
    model = DeepTrustModel(model_name='efficientnet')
    return model
