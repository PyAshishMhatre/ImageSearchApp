import streamlit as st
import numpy as np
from PIL import Image
from feature_extractor import FeatureExtractor
from datetime import datetime
from pathlib import Path
import os
import openai
from urllib.request import urlopen
from io import BytesIO


openai.api_key = "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"



def GenSimilar(img, features, img_paths):  #Run search
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

def genimage(ask):
    try:
        response = openai.Image.create(
        prompt= ask,
        n=1,
        size="256x256"
        )
        image_url = response['data'][0]['url']
        st.image(image= image_url)
        
        image_file = urlopen(image_url)
        image_data = image_file.read()

        pil_image = Image.open(BytesIO(image_data))
        GenSimilar(pil_image, features, img_paths)
        
        
    except openai.error.OpenAIError as e:
        print(e.http_status)
        print(e.error)

# Read image features
fe = FeatureExtractor()
features = []
img_paths = []
for feature_path in Path("./static/feature").glob("*.npy"):
    features.append(np.load(feature_path))
    img_paths.append(Path("./static/img") / (feature_path.stem + ".jpg"))
features = np.array(features)


#Load the image from the path
image_path = "./banner.png"
banner = Image.open(image_path)
st.image(banner, use_column_width = True)

#Page Config
st.title('**:blue[Fashion Image Search]**')

#Take User Input
option = st.selectbox('How would you like to search?',('Upload an Image', 'Generate AI Image'))

if option == 'Upload an Image':
    file = st.file_uploader(label='Upload image to search', type=['jpg','png','jpeg'], key='FileInput')
    if file:
        st.image(file, caption='Uploaded image')
        img = Image.open(file)  # PIL image
        uploaded_img_path = "static/uploaded/" + datetime.now().isoformat().replace(":", ".") + "_" + file.name
        img.save(uploaded_img_path)
        GenSimilar(img, features, img_paths)
        
elif option == 'Generate AI Image':
    ask = st.text_input(label='Enter the description of clothing you want to see')
    run = st.button(label='Build', key='button1')  
    if run and ask != "":
        genimage(ask)  

else:
    st.markdown('Select search method !')







    

    
