from openai import OpenAI
import streamlit as st
import base64
import os
import tempfile
import json
import pandas as pd
import requests
import datetime


df=pd.read_csv('spotted-animals.csv')
ls=['Sika deer', 'Chinese water deer', 'Beaver', 'Rabbit', 'Mountain hare', 'Brown hare', 'Field vole', 'Bank vole', 'Water vole', 'Brown rat', 'Wood mouse', 'House mouse', 'Harvest mouse', 'Hazel dormouse', 'Red squirrel', 'Grey squirrel', 'Fallow deer', 'Red deer', 'Muntjac deer', 'Roe deer', 'Polecat', 'Pine marten', 'Wildcat', 'Weasel', 'Stoat', 'American mink', 'European otter', 'European badger', 'Red fox', 'Alcathoe bat', 'Whiskered bat', 'Serotine', 'Natterer\'s bat', 'Leisler\'s bat', 'Grey long-eared bat', 'Daubenton\'s bat', 'Brandt\'s bat', 'Lesser horseshoe bat', 'Greater horseshoe bat', 'Bechstein\'s bat', 'Barbastelle bat', 'Brown long-eared bat', 'Noctule', 'Common pipistrelle', 'Soprano pipistrelle', 'Nathusius\' pipistrelle', 'Hedgehog', 'Mole', 'Common shrew', 'Pygmy shrew', 'Water shrew', 'Barn owl', 'Short-eared owl', 'Long-eared owl', 'Tawny owl', 'Little owl', 'Swift', 'Kingfisher', 'Green woodpecker', 'Great spotted woodpecker', 'Lesser spotted woodpecker', 'Honey buzzard', 'Goshawk', 'Sparrowhawk', 'Marsh harrier', 'Hen harrier', 'Red kite', 'White-tailed eagle', 'Buzzard', 'Kestrel', 'Merlin', 'Hobby', 'Peregrine', 'Pheasant', 'Grey partridge', 'Red-legged partridge', 'Quail', 'Woodpigeon', 'Stock dove', 'Rock dove', 'Turtle dove', 'Collared dove', 'Cuckoo', 'Great bustard', 'Crane', 'Water rail', 'Corncrake', 'Moorhen', 'Coot', 'Greylag goose', 'Pink-footed goose', 'White-fronted goose', 'Brent goose', 'Canada goose', 'Barnacle goose', 'Mute swan', 'Whooper swan', 'Bewick\'s swan', 'Shelduck', 'Shoveler', 'Gadwall', 'Wigeon', 'Mallard', 'Pintail', 'Teal', 'Eider', 'Common scoter', 'Velvet scoter', 'Goldeneye', 'Goosander', 'Red-breasted merganser', 'Grey heron', 'Bittern', 'Little egret', 'Great white egret', 'Cormorant', 'Shag', 'Gannet', 'Oystercatcher', 'Avocet', 'Lapwing', 'Golden plover', 'Grey plover', 'Ringed plover', 'Little ringed plover', 'Whimbrel', 'Curlew', 'Bar-tailed godwit', 'Black-tailed godwit', 'Turnstone', 'Knot', 'Ruff', 'Sanderling', 'Dunlin', 'Purple sandpiper', 'Woodcock', 'Snipe', 'Redshank', 'Greenshank', 'Green sandpiper', 'Common sandpiper', 'Arctic skua', 'Great skua', 'Guillemot', 'Razorbill', 'Puffin', 'Black-headed gull', 'Common gull', 'Great black-backed gull', 'Herring gull', 'Lesser black-backed gull', 'Kittiwake', 'Little tern', 'Sandwich tern', 'Common tern', 'Arctic tern', 'Raven', 'Carrion crow', 'Hooded crow', 'Rook', 'Jackdaw', 'Magpie', 'Jay', 'Chough', 'Goldfinch', 'Greenfinch', 'Linnet', 'Twite', 'Redpoll', 'Crossbill', 'Bullfinch', 'Hawfinch', 'Chaffinch', 'Brambling', 'Corn bunting', 'Yellowhammer', 'Cirl bunting', 'Reed bunting', 'House sparrow', 'Tree sparrow', 'Grey wagtail', 'Pied wagtail', 'Yellow wagtail', 'Tree pipit', 'Meadow pipit', 'Rock pipit', 'Woodlark', 'Skylark', 'Black redstart', 'Ring ouzel', 'Treecreeper', 'Nuthatch', 'Wren', 'Dipper', 'Starling', 'Spotted flycatcher', 'Pied flycatcher', 'Wheatear', 'Whinchat', 'Stonechat', 'Redstart', 'Nightingale', 'Robin', 'Blackbird', 'Fieldfare', 'Redwing', 'Mistle thrush', 'Song thrush', 'Yellow-browed warbler', 'Grasshopper warbler', 'Firecrest', 'Dartford warbler', 'Chiffchaff', 'Willow warbler', 'Wood warbler', 'Cetti\'s warbler', 'Reed warbler', 'Sedge warbler', 'Lesser whitethroat', 'Whitethroat', 'Garden warbler', 'Blackcap', 'Goldcrest', 'Marsh tit', 'Willow tit', 'Bearded tit', 'Long-tailed tit', 'Coal tit', 'Great tit', 'Blue tit', 'Sand martin', 'Swallow', 'House martin']

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
    client = OpenAI(api_key=st.secrets["API_KEY"]) # type: ignore
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
    Determine if the picture is one of the animals in {ls} and if so then which one.

    Rules:
    - If there are more than 1 different types of animals in the picture, ONLY focus on the one that takes up the most space on the page
    - If there are more than one of the SAME ANIMAL in the picture, return the number of them additionally

    Output form:

    - If there is an animal in the picture 
        1. Determine which of those animals from {ls} is the most likely to be the animal in the picture
        2. Return the name from {ls}, how many of that animal, and the word yes in the 
        3. format the answer ONLY AS: yes,name,number

    - If, WITH 100% CERTAINTY the animal is not in {ls} or there is no animal in the picture, return the phrase:
    Sorry we could match the animal in the picture to to an animal in our databse.
    """
   # - If the animal is DEFINITELY NOT in {ls}, ONLY respond with:
   # 'This animal is not in the database, it could be a: ' and then the specific animal.
   # - If there is no animal in the picture, ONLY respond with:
   # 'No animal has been identified in the picture, please try again!'


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
            st.write("Location - In the form of lat,long - Copy and paste your coordinates from here:")
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


    

