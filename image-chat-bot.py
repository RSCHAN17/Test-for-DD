from openai import OpenAI
import streamlit as st
import base64
import os
import tempfile

client = OpenAI(api_key=st.secrets["API_KEY"])


st.title("Animal Chatbot")
uploaded_file = st.file_uploader(
    "Upload image", type=["jpg", "png"])
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

    animal_information=[{"animal:dog"},{"animal:cat"},{"animal:fox"},{"animal:bird"}]

    prompt = f"""
    Task:
    Using the animals in {animal_information} determine which one is in the picture and the species and breed

    Rules:
    - If there are more than 1 different types of animals in the picture, focus on the one that takes up more space
    - If there are more than one of the same animal in the picture, return the number of them additionally

    Output form:
    If there is an animal in the picture and it is in {animal_information}:
    'You have spotted' and then the animal, its species, its breed and how many.
    If there is an animal in the picture but it is not in {animal_information}: 
    'The animal you have spotted is not in our database, it could be': and then the animal that it is.
    If there are no animals in the picture: 
    "There is no animal spotted in this picture, try again!"

    """
### Is it in database: Yes
### What is is the main animal in the photo: 
### Is there another animal in this photo:
### How many of the main animal are there:
### What species is the animal:
### What breed is the animal:


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
    st.markdown(f'**Answer:** {answer}')
