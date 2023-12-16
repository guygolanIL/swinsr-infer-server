import torch
import numpy as np
from PIL import Image
import cv2
from transformers import AutoImageProcessor, Swin2SRForImageSuperResolution

def model_infer(image_binary):
    imageMat = np.frombuffer(image_binary, np.uint8)
    image = cv2.imdecode(imageMat, cv2.IMREAD_COLOR)
    # Check if GPU is available and use CUDA, otherwise use CPU
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    processor = AutoImageProcessor.from_pretrained("caidas/swin2SR-classical-sr-x2-64")
    model = Swin2SRForImageSuperResolution.from_pretrained("caidas/swin2SR-classical-sr-x2-64")

    # Move model to the GPU if available
    model.to(device)

    # Prepare image for the model
    inputs = processor(image, return_tensors="pt")

    # Move inputs to the GPU if available
    inputs = {k: v.to(device) for k, v in inputs.items()}

    # Forward pass
    with torch.no_grad():
        outputs = model(**inputs)

    # Move outputs to CPU for further processing
    output = outputs.reconstruction.data.squeeze().float().cpu().clamp_(0, 1).numpy()
    output = np.moveaxis(output, source=0, destination=-1)
    output = (output * 255.0).round().astype(np.uint8)  # float32 to uint8

    print('saving image')
    cv2.imwrite(f"sr_{'halas'}.png", output)

    _, img_encoded = cv2.imencode(".png", output)
    
    return img_encoded.tobytes()


