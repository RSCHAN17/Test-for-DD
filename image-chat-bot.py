from openai import OpenAI
import streamlit as st
import base64
import os
import tempfile
import json
import pandas as pd
import requests
import datetime

client = OpenAI(api_key=st.secrets["API_KEY"]) # type: ignore
df=pd.read_csv('spotted-animals.csv')

st.markdown("""
    <style>
    /* Target the text inside */
    [data-testid="stFileUploadDropzone"] p {
        color: black;
    }
    </style>
    """, unsafe_allow_html=True)

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
    - If there is no animal in the picture, ONLY respond with:
    'No animal has been identified in the picture, please try again!'
    - If the animal is not in {df}, ONLY respond with:
    'This animal is not in the database, it could be a: ' and then the specific animal and speciies
    - If the animal is in the {df}, 
        ONLY return the name of the animal
        IT MUST exactly match its name in {df}
        And the number of that animal in the picture
        in the format: yes,name,number
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
    output=[x.strip() for x in answer.split(",")]
    if output[0]=='yes':

        name = df.loc[df['name'] == output[1]]['name'].values[0]
        zoo_id = df.loc[df['name'] == output[1]]['zoo_id'].values[0]
        species = df.loc[df['name'] == output[1]]['species'].values[0]
        capture_points = df.loc[df['name'] == output[1]]['capture_points'].values[0]
        pack_bonus_mult = df.loc[df['name'] == output[1]]['pack_bonus_mult'].values[0]
        num=output[2]
        data={"name":name,"zoo_id":zoo_id,"species":species,"capture_points":capture_points,"how_many":num}
    
        st.markdown(f'**Spotted:**')
        st.html(f"""<div id='info'>
        <p>You have spotted: <span id='name'>{data["name"]}
        </span></p>
        <p>Zoo ID: <span id='zoo_id'>{data["zoo_id"]}
        </span></p>
        <p>Species: <span id='species'>{data['species']}
        </span></p>           
        <p>Points: <span id='capture_points'>{data['capture_points']}
        </span></p>
        <p>Number of them: <span id='number'>{data['how_many']}
        </span></p>
        </div>
        """)
        st.html(f"<span id='img'> <img src='data:image;base64,{base64_image}' style='max-height:300px;'/></span>")
        image_url=f"data:image;base64,{base64_image}"
        
        css = """
        <style>
            div[data-testid="stForm"] {
                background-color: #36656B !important;
            }
        </style>
        """
        with st.form(key="spot_submission", clear_on_submit=True):
            st.write("Submit spotting")
            username=st.text_input(label='To confirm you want to submit your spotting, enter your username')
            st.write("Location - Copy and paste your coordinates from here:")
            location=st.text_input(label="https://plus.codes/map")
            submitted = st.form_submit_button("Submit")
            if submitted:
                if 1.0 * len(username) * len(location) > 0:
                    now = pd.to_datetime(datetime.datetime.now())
                    now = now.replace(microsecond=0)
                    now = now.isoformat()
                    url_post = "https://spotting-api.onrender.com/spottings/new"
                    post_data = {"date_time":now, "username":username, "animal_name":name, "animal_count":num, "location":location, "image_url":image_url}
                    post_response = requests.post(url_post,json=post_data)
                    post_response_json = post_response.json()
                    st.write("Submitted spot!")
                    
        st.write(css,unsafe_allow_html=True)
    else:
        st.html(f"<p><span>{answer}</span></p>")
        st.html(f"<span id='img'> <img src='data:image;base64,{base64_image}' style='max-height:300px;'/></span>")


    

