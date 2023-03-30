from PIL import Image
from feature_extractor import FeatureExtractor
from pathlib import Path
import numpy as np
import os

root_dir = "./static/img"

if __name__ == '__main__':
    fe = FeatureExtractor()

for subdir, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith(".jpg"):
            img_path = os.path.join(subdir, file)
            subdirectory_name = os.path.basename(subdir)
            file_name = os.path.splitext(file)[0] # e.g., ./static/img/xxx.jpg
            feature = fe.extract(img=Image.open(img_path))
            feature_path = Path("./static/feature") / (subdirectory_name + "_" + file_name + ".npy")  # e.g., ./static/feature/xxx.npy
            np.save(feature_path, feature)


