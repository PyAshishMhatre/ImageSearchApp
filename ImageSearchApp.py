import streamlit as st
import numpy as np
from PIL import Image
from feature_extractor import FeatureExtractor
from datetime import datetime
from pathlib import Path

image_path = "./banner.png"
# Load the image from the path
banner = Image.open(image_path)
st.image(banner, use_column_width = True)
st.title(':blue[Fashion Image Search]')
# Read image features
fe = FeatureExtractor()
features = []
img_paths = []
for feature_path in Path("./static/feature").glob("*.npy"):
    features.append(np.load(feature_path))
    img_paths.append(Path("./static/img") / (feature_path.stem + ".jpg"))
features = np.array(features)


file = st.file_uploader(label='Upload image to search', type='jpg', key='FileInput')

if file:
    st.image(file, caption='Uploaded image')
    img = Image.open(file)  # PIL image
    uploaded_img_path = "static/uploaded/" + datetime.now().isoformat().replace(":", ".") + "_" + file.name
    img.save(uploaded_img_path)
    
    #Run search
    query = fe.extract(img)
    dists = np.linalg.norm(features-query, axis=1)  # L2 distances to features
    ids = np.argsort(dists)[:30]  # Top 30 results
    scores = [(dists[id], img_paths[id]) for id in ids]
    
    col1, col2, col3 = st.columns(3)
    i = 0
    for score, image in scores:
        i = i + 1
        
        if i == 1:
            with col1:
                image = Image.open(image)
                st.image(image, caption='Score is {d_score}'.format(d_score = score))
        elif i == 2:
             with col2:
                image = Image.open(image)
                st.image(image, caption='Score is {d_score}'.format(d_score = score))
        else:
            with col3:
                image = Image.open(image)
                st.image(image, caption='Score is {d_score}'.format(d_score = score))
                i = 0     
    