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
ls = [
    "Sika deer", "Chinese water deer", "Beaver", "Rabbit", "Mountain hare", 
    "Brown hare", "Field vole", "Bank vole", "Water vole", "Brown rat", 
    "Wood mouse", "House mouse", "Harvest mouse", "Hazel dormouse", 
    "Red squirrel", "Grey squirrel", "Fallow deer", "Red deer", 
    "Muntjac deer", "Roe deer", "Polecat", "Pine marten", "Wildcat", 
    "Weasel", "Stoat", "American mink", "European otter", "European badger", 
    "Red fox", "Alcathoe bat", "Whiskered bat", "Serotine", "Natterer's bat", 
    "Leisler's bat", "Grey long-eared bat", "Daubenton's bat", "Brandt's bat", 
    "Lesser horseshoe bat", "Greater horseshoe bat", "Bechstein's bat", 
    "Barbastelle bat", "Brown long-eared bat", "Noctule", "Common pipistrelle", 
    "Mole", "Water shrew", "Pygmy shrew", "Common shrew", "European hedgehog", 
    "Sand lizard", "Smooth snake", "Adder", "Grass snake", "Slow worm", 
    "Common lizard", "Marsh frog", "Common frog", "Natterjack toad", 
    "Common toad", "Palmate newt", "Smooth newt", "Great crested newt", 
    "Red-necked grebe", "Great northern diver", "Little grebe", 
    "Great crested grebe", "Black-necked grebe", "Slavonian grebe", 
    "Black-throated diver", "Red-throated diver", "Mediterranean gull", 
    "Sooty shearwater", "Storm Petrel", "Roseate tern", "Arctic tern", 
    "Common tern", "Sandwich tern", "Little tern", "Kittiwake", 
    "Great black-backed gull", "Lesser black-backed gull", "Herring gull", 
    "Common gull", "Black-headed gull", "Arctic skua", "Great skua", 
    "Razorbill", "Guillemot", "Black guillemot", "Puffin", "Shag", 
    "Cormorant", "Northern gannet", "Manx shearwater", "Fulmar", 
    "Red-crested pochard", "Long-tailed duck", "Egyptian goose", "Smew", 
    "Garganey", "Eider", "Common scoter", "Red-breasted merganser", 
    "Goosander", "Goldeneye", "Tufted duck", "Pochard", "Teal", "Wigeon", 
    "Shoveler", "Pintail", "Gadwall", "Mallard", "Mandarin duck", 
    "Shelduck", "Brent goose", "Barnacle goose", "Canada goose", 
    "Pink-foot goose", "White-fronted goose", "Greylag goose", 
    "Whooper swan", "Bewick's swan", "Mute swan", "Glossy ibis", 
    "Cattle egret", "Common crane", "Great white egret", "European spoonbill", 
    "Little egret", "Grey heron", "Bittern", "Honey buzzard", "Goshawk", 
    "Barn owl", "Little owl", "Long-eared owl", "Short-eared owl", "Tawny owl", 
    "Merlin", "Peregrine falcon", "Hobby", "Kestrel", "Sparrowhawk", 
    "Buzzard", "Hen harrier", "Marsh harrier", "Osprey", "Red kite", 
    "Golden eagle", "White-tailed eagle", "Quail", "Capercaillie", 
    "Ptarmigan", "Pheasant", "Grey partridge", "Red-legged partridge", 
    "Black grouse", "Red grouse", "Little stint", "Stone curlew", 
    "Black-winged stilt", "Jack snipe", "Purple sandpiper", "Corncrake", 
    "Red-neck phalarope", "Snipe", "Woodcock", "Whimbrel", "Curlew", 
    "Bar-tailed godwit", "Black-tailed godwit", "Greenshank", "Redshank", 
    "Ruff", "Common sandpiper", "Green Sandpiper", "Dunlin", "Sanderling", 
    "Knot", "Turnstone", "Grey plover", "Golden plover", "Lapwing", 
    "Ringed plover", "Little ringed plover", "Avocet", "Oystercatcher", 
    "Coot", "Moorhen", "Water rail", "Collared dove", "Turtle dove", 
    "Stock dove", "Woodpigeon", "Rock dove", "Wryneck", "Waxwing", 
    "Kingfisher", "Cuckoo", "Lesser spotted woodpecker", "Green woodpecker", 
    "Great spotted woodpecker", "Nightjar", "Swallow", "House martin", 
    "Sand martin", "Swift", "Ring-necked parakeet", "Tree pipit", 
    "Shore lark", "Tree sparrow", "House sparrow", "Dunnock", "Grey wagtail", 
    "Yellow wagtail", "Pied wagtail", "Meadow pipit", "Rock pipit", 
    "Woodlark", "Skylark", "Black redstart", "Ring ouzel", "Treecreeper", 
    "Nuthatch", "Wren", "Dipper", "Starling", "Spotted flycatcher", 
    "Pied flycatcher", "Wheatear", "Whinchat", "Stonechat", "Redstart", 
    "Nightingale", "Robin", "Blackbird", "Fieldfare", "Redwing", 
    "Mistle thrush", "Song thrush", "Yellow-browed warbler", 
    "Grasshopper warbler", "Firecrest", "Dartford warbler", "Chiffchaff", 
    "Willow warbler", "Wood warbler", "Cetti's warbler", "Reed warbler", 
    "Sedge warbler", "Lesser whitethroat", "Whitethroat", "Garden warbler", 
    "Blackcap", "Goldcrest", "Marsh tit", "Willow tit", "Bearded tit", 
    "Long-tailed tit", "Coal tit", "Blue tit", "Great tit", "Great grey shrike", 
    "Raven", "Hooded crow", "Carrion crow", "Rook", "Jackdaw", "Chough", 
    "Jay", "Magpie", "Common rosefinch", "Twite", "Brambling", "Hawfinch", 
    "Snow bunting", "Corn bunting", "Yellowhammer", "Reed bunting", 
    "Common crossbill", "Bullfinch", "Siskin", "Goldfinch", "Greenfinch", 
    "Lesser redpoll", "Linnet", "Chaffinch"
]
st.markdown("""
    <style>
    /* Target the text inside */
    
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
        <p>You have spotted: <span id='name'>{data["name"]}</span></p>
        <p>Zoo ID: <span id='zoo_id'>{data["zoo_id"]}</span></p>
        <p>Species: <span id='species'>{data['species']}</span></p>           
        <p>Points: <span id='capture_points'>{data['capture_points']}</span></p>
        <p>Number of them: <span id='number'>{data['how_many']}</span></p>
        </div>
        """)
        st.html(f"<span id='img'> <img src='data:image;base64,{base64_image}' style='max-height:300px;'/></span>")
        image_url=f"data:image;base64,{base64_image}"
        
        css = """
        <style>
            div[data-testid="stForm"] {
                background-color: #36656B !important;
            }
            .stTextinput input[aria-label="To confirm you want to submit your spotting, enter your username"] {
                background-color: #A5C89E !important;
                color: #36656B !important;
            }
            .stTextinput input[aria-label="Location - In the form of lat,long - Copy and paste your coordinates from here:"] {
                background-color: #A5C89E !important;
                color: #36656B !important;
            }
        </style>
        """
        with st.form(key="spot_submission", clear_on_submit=True):
            st.write("Submit spotting")
            username=st.text_input(label="To confirm you want to submit your spotting, enter your username")
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


    

