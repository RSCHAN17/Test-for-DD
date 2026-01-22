from openai import OpenAI
import streamlit as st
import base64
import os
import tempfile
import json
import pandas as pd

client = OpenAI(api_key=st.secrets["API_KEY"]) # type: ignore
df=pd.read_csv('spotted-animals.csv')

st.title("Spotted verifier")
uploaded_file = st.file_uploader(
    "Upload image", type=["jpg", "png","HEIC"])
if uploaded_file:
    temp_dir = tempfile.mkdtemp()
    path = os.path.join(temp_dir, uploaded_file.name)
    with open(path, "wb") as f:
        f.write(uploaded_file.getvalue())

    # Function to encode the image
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")


    # Path to your image
    image_path = path

    # Getting the Base64 string
    base64_image = encode_image(image_path)

    prompt = f"""
    Task:
    Determine if the picture is one of the animals in {df} and if so then which one.

    Rules:
    - If there are more than 1 different types of animals in the picture, ONLY focus on the one that has the highest 'capture_points'
    - If there are more than one of the same animal in the picture, return the number of them additionally

    Output form:
    - If the animal is not in {df}, ONLY respond with the:
    'This animal is not in the database, it could be a: ' and then the specific animal and speciies
    - If the animal is in the {df}, 
        Return with the row information and the number of animals in the picture as how_many
        Return a Dictionary object only in the format {'{}'}
        With valid dictionary keys:
    - name (as type str)
    - species (as type str)
    - capture_points (as type float)
    - pack_bonus_mult (as type float)
    - how_many (as type int)
    """


    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "user",
                "content": [
                    { "type": "input_text", "text": prompt },
                    {
                        "type": "input_image",
                        "image_url": f"data:image/jpeg;base64,{base64_image}",
                    },
                ],
            }
        ],
    )

    answer=response.output_text
    
    
    st.markdown(f'**Spotted:**')
    st.markdown(f'{answer}')
    if answer[0] == '{':
        temp=str(f"{answer}")
        data=json.loads(temp)
        st.html(f"<p><span>{data}</span></p>")
        st.html(f"""<p><span>
            You have spotted: {data["name"]} <br>
            Species: {data['species']} <br>
            Points: {data['capture_points']} <br>
            Pack multiplier: {data['pack_bonus_mult']} <br>
            Number spotted: {data['how_many']}
            </span></p>""")
    else:
        st.html(f"<p><span>{answer}</span></p>")

