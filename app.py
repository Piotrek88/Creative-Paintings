from openai import OpenAI
import requests
import streamlit as st
from PIL import Image
import os



styl_css = """
<link href="https://fonts.googleapis.com/css2?family=Lobster&display=swap" rel="stylesheet">
<style>
.custom-font {
    font-family: 'Comic Sans MS', cursive;
    font-size: 30px;
    justify-content: center;
    align-items: center;
    text-align: center;
    color:#40E0D0;
    line-height: 2.0;
}
.fullscreen-button {
    display: none;
}
</style>
"""
st.markdown(styl_css, unsafe_allow_html=True)

opis_aplikacji = """
<div class="custom-font">
Aplikacja do generowania kolorowanek.
</div>
"""

def generate_image(prompt):
    response = openai_client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
        response_format="url"
    )
    image_url = response.data[0].url

    return image_url 

def download_image(image_url):
    response = requests.get(image_url)
    if response.status_code == 200:
        return response.content
    else:
        raise Exception("Pobieranie obrazu nie powiodło się.")

main_images= [
    {"name": "Zwierzaki", "image": os.path.join("appart", "zwierzaki.jpg")},
    {"name": "Pojazdy", "image": os.path.join("appart", "pojazdy.jpg")},
    {"name": "Inne", "image": os.path.join("appart", "inne.jpg")}
]

sub_animal= {
    "Pies": os.path.join("appart", "pies.jpg"),
    "Kot": os.path.join("appart", "kot.jpg"), 
    "Mysz": os.path.join("appart", "mysz.jpg"),
    "Koń": os.path.join("appart", "kon.jpg"),
    "Słoń": os.path.join("appart", "slon.jpg"),
    "Żyrafa": os.path.join("appart", "zyrafa.jpg"), 
    "Królik": os.path.join("appart", "krolik.jpg"),
    "Krowa": os.path.join("appart", "krowa.jpg"),
    "Owca": os.path.join("appart", "owca.jpg"),
    "Świnia": os.path.join("appart", "swinka.jpg")
}

sub_vehicles= {
    "Samochód": os.path.join("appart", "samochod.jpg"),
    "Traktor": os.path.join("appart", "traktor.jpg"),
    "Pociąg": os.path.join("appart", "pociag.jpg"),
    "Cieżarówka": os.path.join("appart", "ciezarowka.jpg"),
    "Samolot": os.path.join("appart", "samolot.jpg"),
    "Karetka": os.path.join("appart", "karetka.jpg"),
    "Straż": os.path.join("appart", "straz.jpg"),
    "Policja": os.path.join("appart", "policja.jpg"),
    "Motor": os.path.join("appart", "motor.jpg"),
    "Wyścigówka": os.path.join("appart", "wyscigowka.jpg")
}


max_chars= 30

options = {
    "Pies": "black and white line art, dog, losowa czarno-biała sceneria dla danego zwierzęcia",
    "Kot": "black and white line art, cat, losowa czarno-biała sceneria dla danego zwierzęcia",
    "Mysz": "black and white line art, mouse, losowa czarno-biała sceneria dla danego zwierzęcia",
    "Koń": "black and white line art, horse, losowa czarno-biała sceneria dla danego zwierzęcia",
    "Słoń": "black and white line art, elephant, losowa czarno-biała sceneria dla danego zwierzęcia",
    "Żyrafa": "black and white line art, giraffe, losowa czarno-biała sceneria dla danego zwierzęcia",
    "Królik": "black and white line art, rabbit, losowa czarno-biała sceneria dla danego zwierzęcia",
    "Krowa": "black and white line art, cow, losowa czarno-biała sceneria dla danego zwierzęcia",
    "Owca": "black and white line art, sheep, losowa czarno-biała sceneria dla danego zwierzęcia",
    "Świnia": "black and white line art, pig, losowa czarno-biała sceneria dla danego zwierzęcia",
    "Samochód": "black and white line art, car, losowa czarno-biała sceneria dla danego pojazdu",
    "Traktor": "black and white line art, traktor, losowa czarno-biała sceneria dla danego pojazdu",
    "Pociąg": "black and white line art, train, losowa czarno-biała sceneria dla danego pojazdu",
    "Cieżarówka": "black and white line art, Cieżarówka, losowa czarno-biała sceneria dla danego pojazdu",
    "Samolot": "black and white line art, airplane, losowa czarno-biała sceneria dla danego pojazdu",
    "Karetka": "black and white line art, karetka, losowa czarno-biała sceneria dla danego pojazdu",
    "Straż": "black and white line art, wóz strażacki, losowa czarno-biała sceneria dla danego pojazdu",
    "Policja": "black and white line art, radiowóz, losowa czarno-biała sceneria dla danego pojazdu",
    "Motor": "black and white line art, motorbike, losowa czarno-biała sceneria dla danego pojazdu",
    "Wyścigówka": "black and white line art, wyścigówka, losowa czarno-biała sceneria dla danego pojazdu",
}



openai_client = OpenAI(api_key=st.secrets["openai_api_key"])


# Inicjalizacja stanu Streamlit
if 'selected_main' not in st.session_state:
    st.session_state.selected_main = None

# Przygotowanie stanu dla generowanych obrazów
if 'generated_images' not in st.session_state:
    st.session_state['generated_images'] = []

# Zmiana kategorii resetuje obrazy tylko wtedy, gdy użytkownik zmieni wybór
if st.session_state.selected_main != st.session_state.get("previous_main", None):
    st.session_state.generated_images = []
st.session_state["previous_main"] = st.session_state.selected_main



#### MAIN ####


col1,col2,col3 = st.columns([5, 8, 5])
with col2:
    st.image(os.path.join("appart", "BEZ TLA.png"))

st.markdown(opis_aplikacji, unsafe_allow_html=True)
st.markdown("<br><br>", unsafe_allow_html=True)   


# Wyświetlanie głównych kategorii
cols = st.columns(3)
for index, item in enumerate(main_images):
    with cols[index]:
        st.image(item["image"], width=220)
        if st.button(item["name"], use_container_width=True):
            st.session_state.selected_main = item["name"]
            st.session_state.generated_images = []

# Logika dla wyboru kategorii "Inne"
if 'selected_main' in st.session_state and st.session_state.selected_main == "Inne":
    base_prompt = "black and white line art, losowa czarno-biała sceneria dla danego"
    user_input = st.text_area("Napisz jaki obrazek chcesz wygenerować:", height=200, max_chars=30)
    st.session_state['user_input'] = user_input
    is_disabled = not st.session_state['user_input'].strip()

    if st.button("Wygeneruj obraz", disabled=is_disabled) and st.session_state['user_input'].strip():
        image_url = generate_image(f"{base_prompt} + ('') + {st.session_state['user_input']}")
        st.session_state['generated_images'].append(("Własny obraz", image_url))

# Logika dla podkategorii Zwierzaki lub Pojazdy
if 'selected_main' in st.session_state and st.session_state.selected_main in ["Zwierzaki", "Pojazdy"]:
    sub_images = sub_animal if st.session_state.selected_main == "Zwierzaki" else sub_vehicles
    sub_cols = st.columns(5)
    for index, (name, path) in enumerate(sub_images.items()):
        with sub_cols[index % 5]:
            st.image(path)
            if st.button(name, use_container_width=True):
                image_url = generate_image(options[name] + f" Obraz: {name}")
                st.session_state['generated_images'].append((name, image_url))

# Wyświetlanie i pobieranie obrazu
if st.session_state['generated_images']:
    name, image_url = st.session_state['generated_images'][-1]

    st.image(image_url, caption=f"Obraz {name}")

    try:
        image_data = download_image(image_url)
        # Ustawienie przycisku do pobrania obrazu
        col1, col2, col3 = st.columns(3)
        with col2:
            st.download_button(
                label=f"Pobierz {name}",
                data=image_data,
                file_name=f"{name}.png",
                mime="image/png",
                key=f"download_{name}"
            )
    except Exception as e:
        st.error(f"Nie udało się pobrać obrazu: {e}")
