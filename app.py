from dotenv import dotenv_values
from openai import OpenAI
import requests
import streamlit as st
from PIL import Image

env = dotenv_values(".env")

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
Aplikacja do generowania kolorowanek
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



# Inicjalizacja stanu Streamlit
if 'selected_main' not in st.session_state:
    st.session_state.selected_main = None
if 'generated_images' not in st.session_state:
    st.session_state.generated_images = []

# Zmiana kategorii resetuje obrazy tylko wtedy, gdy użytkownik zmieni wybór
if st.session_state.selected_main != st.session_state.get("previous_main", None):
    st.session_state.generated_images = []

st.session_state["previous_main"] = st.session_state.selected_main



main_images= [
    {"name": "Zwierzaki", "image": r"C:\Users\ppawl\OneDrive\Pulpit\CreativePaintings\appart\zwierzaki.jpg"},
    {"name": "Pojazdy", "image": r"C:\Users\ppawl\OneDrive\Pulpit\CreativePaintings\appart\pojazdy.jpg"},
    {"name": "Inne", "image": r"C:\Users\ppawl\OneDrive\Pulpit\CreativePaintings\appart\inne.jpg"}
]

sub_animal= {
    "Pies": r"C:\Users\ppawl\OneDrive\Pulpit\CreativePaintings\appart\pies.jpg",
    "Kot": r"C:\Users\ppawl\OneDrive\Pulpit\CreativePaintings\appart\kot.jpg", 
    "Mysz": r"C:\Users\ppawl\OneDrive\Pulpit\CreativePaintings\appart\mysz.jpg",
    "Koń": r"C:\Users\ppawl\OneDrive\Pulpit\CreativePaintings\appart\kon.jpg",
    "Słoń": r"C:\Users\ppawl\OneDrive\Pulpit\CreativePaintings\appart\slon.jpg",
    "Żyrafa": r"C:\Users\ppawl\OneDrive\Pulpit\CreativePaintings\appart\zyrafa.jpg", 
    "Królik": r"C:\Users\ppawl\OneDrive\Pulpit\CreativePaintings\appart\krolik.jpg",
    "Krowa": r"C:\Users\ppawl\OneDrive\Pulpit\CreativePaintings\appart\krowa.jpg",
    "Owca": r"C:\Users\ppawl\OneDrive\Pulpit\CreativePaintings\appart\owca.jpg",
    "Świnia": r"C:\Users\ppawl\OneDrive\Pulpit\CreativePaintings\appart\swinka.jpg"
}

sub_vehicles= {
    "Samochód": r"C:\Users\ppawl\OneDrive\Pulpit\CreativePaintings\appart\samochod.jpg",
    "Traktor": r"C:\Users\ppawl\OneDrive\Pulpit\CreativePaintings\appart\traktor.jpg",
    "Pociąg": r"C:\Users\ppawl\OneDrive\Pulpit\CreativePaintings\appart\pociag.jpg",
    "Cieżarówka": r"C:\Users\ppawl\OneDrive\Pulpit\CreativePaintings\appart\ciezarowka.jpg",
    "Samolot": r"C:\Users\ppawl\OneDrive\Pulpit\CreativePaintings\appart\samolot.jpg",
    "Karetka": r"C:\Users\ppawl\OneDrive\Pulpit\CreativePaintings\appart\karetka.jpg",
    "Straż": r"C:\Users\ppawl\OneDrive\Pulpit\CreativePaintings\appart\straz.jpg",
    "Policja": r"C:\Users\ppawl\OneDrive\Pulpit\CreativePaintings\appart\policja.jpg",
    "Motor": r"C:\Users\ppawl\OneDrive\Pulpit\CreativePaintings\appart\motor.jpg",
    "Wyścigówka": r"C:\Users\ppawl\OneDrive\Pulpit\CreativePaintings\appart\wyscigowka.jpg"
}


max_chars= 150

options = {
    "Pies": "białe tło, czarne linie, kolorowanka dla dzieci, pies, losowa sceneria",
    "Kot": "białe tło, czarne linie, kolorowanka dla dzieci, kot, losowa sceneria", 
    "Mysz": "białe tło, czarne linie, kolorowanka dla dzieci, mysz, losowa sceneria",
    "Koń": "białe tło, czarne linie, kolorowanka dla dzieci, koń, losowa sceneria",
    "Słoń": "białe tło, czarne linie, kolorowanka dla dzieci, słoń, losowa sceneria",
    "Żyrafa": "białe tło, czarne linie, kolorowanka dla dzieci, zyrafa, losowa sceneria",
    "Królik": "białe tło, czarne linie, kolorowanka dla dzieci, królik, losowa sceneria",
    "Krowa": "białe tło, czarne linie, kolorowanka dla dzieci, krowa, losowa sceneria",
    "Owca": "białe tło, czarne linie, kolorowanka dla dzieci, owca, losowa sceneria",
    "Świnia": "białe tło, czarne linie, kolorowanka dla dzieci, świnia, losowa sceneria",
    "Samochód": "białe tło, czarne linie, kolorowanka dla dzieci, samochód, losowa sceneria",
    "Traktor": "białe tło, czarne linie, kolorowanka dla dzieci, traktor, losowa sceneria",
    "Pociąg": "białe tło, czarne linie, kolorowanka dla dzieci, pociąg, losowa sceneria",
    "Cieżarówka": "białe tło, czarne linie, kolorowanka dla dzieci, ciężarówka, losowa sceneria",
    "Samolot": "białe tło, czarne linie, kolorowanka dla dzieci, samolot, losowa sceneria",
    "Karetka": "białe tło, czarne linie, kolorowanka dla dzieci, karetka, losowa sceneria",
    "Straż": "białe tło, czarne linie, kolorowanka dla dzieci, wóz strażacki, losowa sceneria",
    "Policja": "białe tło, czarne linie, kolorowanka dla dzieci, radiowóz, losowa sceneria",
    "Motor": "białe tło, czarne linie, kolorowanka dla dzieci, motor, losowa sceneria",
    "Wyścigówka": "białe tło, czarne linie, kolorowanka dla dzieci, wyścigówka, losowa sceneria"
}



mapping= {
    "Jeden": 1,
    "Dwa" : 2,
    "Trzy": 3
}


#
# Main program
#


# Kod zabezpieczający klucz API
if not st.session_state.get("openai_api_key"):
    if "OPENAI_API_KEY" in env:
        st.session_state["openai_api_key"] = env["OPENAI_API_KEY"]
    else:
        col1,col2,col3 = st.columns([5, 8, 5])
        with col2:
            st.image(r"C:\Users\ppawl\OneDrive\Pulpit\CreativePaintings\appart\BEZ TLA.png", use_column_width= True)
        st.info("Podaj klucz API aby korzystać z Creative Paintings")
        st.session_state["openai_api_key"] = st.text_input("Klucz API", type="password")
        if st.session_state["openai_api_key"]:
            st.experimental_rerun()
if not st.session_state.get("openai_api_key"):
    st.stop()

openai_client = OpenAI(api_key=st.session_state["openai_api_key"])




col1,col2,col3 = st.columns([5, 8, 5])
with col2:
    st.image(r"C:\Users\ppawl\OneDrive\Pulpit\CreativePaintings\appart\BEZ TLA.png", use_column_width= True)

st.markdown(opis_aplikacji, unsafe_allow_html=True)
st.markdown("<br><br>", unsafe_allow_html=True)                 
selected_option = st.selectbox("Liczba obrazków do wygenerowania:", ["Jeden", "Dwa", "Trzy"])
num_images = mapping[selected_option]




# Wyświetlanie głównych kategorii
cols = st.columns(3)
for index, item in enumerate(main_images):
    with cols[index]:
        st.image(item["image"], width=220)
        if st.button(item["name"], use_container_width=True):
            st.session_state.selected_main = item["name"]
            st.session_state.generated_images = []

# Logika dla wyboru kategorii "Inne"
if st.session_state.selected_main == "Inne":
    base_prompt = "białe tło, czarne linie, kolorowanka dla dzieci, losowa sceneria"
    user_input = st.text_area("Napisz jaki obrazek chcesz wygenerować:", height=200)

    
    if st.button("Wygeneruj obrazki") and user_input.strip():
            st.session_state.generated_images = [
            generate_image(f"{base_prompt}, {user_input} #{i+1}")
            for i in range(num_images)
            ]
            


# Logika dla podkategorii Zwierzaki lub Pojazdy
if st.session_state.selected_main in ["Zwierzaki", "Pojazdy"]:
    sub_images = sub_animal if st.session_state.selected_main == "Zwierzaki" else sub_vehicles
    sub_cols = st.columns(5)
    for index, (name, path) in enumerate(sub_images.items()):
        with sub_cols[index % 5]:
            st.image(path, use_column_width=True)
            if st.button(name, use_container_width=True):
                st.session_state.generated_images = [
                    generate_image(options[name] + f" #{i+1}")
                    for i in range(num_images)
                ]

# Wyświetlanie i pobieranie wygenerowanych obrazów
for idx, image_url in enumerate(st.session_state.generated_images):
    st.image(image_url, caption=f"Obraz #{idx+1}")
    image_data = download_image(image_url)
    st.download_button(
        label=f"Pobierz Obraz #{idx+1}",
        data=image_data,
        file_name=f"obraz_{idx+1}.png",
        mime="image/png",
        key=f"download_{idx}_{image_url}"
    )