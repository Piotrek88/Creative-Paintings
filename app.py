import psycopg2 # type: ignore
from openai import OpenAI
import requests
import streamlit as st
from PIL import Image
import os
from st_paywall import add_auth   # type: ignore
from datetime import datetime, timezone
import pandas as pd # type: ignore


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


FREE_USER_MAX_PIC = 3
PREMIUM_USER_MAX_PIC = 30

#
# database & openai
#

def get_connection():
    return psycopg2.connect(
        dbname=st.secrets["database"],
        user=st.secrets["username"],
        password=st.secrets["password"],
        host=st.secrets["host"],
        port=st.secrets["port"],
        sslmode=st.secrets["sslmode"]
    )

def get_current_month_usage_df(email):
    with get_connection() as conn:
        now = datetime.now(timezone.utc)
        start_date = datetime(now.year, now.month, 1)
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM usages WHERE google_user_email = %s AND created_at >= %s", (email, start_date))
            rows = cur.fetchall()
            columns = [desc[0] for desc in cur.description]
            df_usages = pd.DataFrame(rows, columns=columns)

    return df_usages

def insert_usage(email, created_at, output_tokens, input_tokens, user_input):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT generations FROM usages
                WHERE google_user_email = %s AND user_input = %s
            """, (email, user_input))

            result = cur.fetchone()

            if result:
                current_generations = result[0]
                cur.execute("""
                    UPDATE usages
                    SET generations = %s, created_at = %s, output_tokens = %s, input_tokens = %s
                    WHERE google_user_email = %s AND user_input = %s
                """, (current_generations + 1, created_at, output_tokens, input_tokens, email, user_input))
            else:
                cur.execute("""
                    INSERT INTO usages (google_user_email, created_at, output_tokens, input_tokens, user_input, generations)
                    VALUES (%s, %s, %s, %s, %s, 1)
                """, (email, created_at, output_tokens, input_tokens, user_input))

            conn.commit()


def generate_image(prompt):
    if not st.session_state.get('email'):
        raise Exception("Zaloguj się")
    
    response = openai_client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
        response_format="url"
    )
    image_url = response.data[0].url
    usage = {'completion_tokens': 0, 'prompt_tokens': 0}  # Default values
    if hasattr(response, 'usage'):
        usage = {
            'completion_tokens': response.usage.completion_tokens,
            'prompt_tokens': response.usage.prompt_tokens
        }

    insert_usage(
        email=st.session_state['email'],
        created_at=datetime.now(timezone.utc),
        output_tokens=usage['completion_tokens'],
        input_tokens=usage['prompt_tokens'],
        user_input=prompt
    )

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
base_prompt = "black and white line art, losowa czarno-biała sceneria dla danego"

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


def allow_usage():
    is_free_user = not st.session_state.get("user_subscribed")
    email = st.session_state.get("email")

    if not email:
        raise Exception("User is not logged in")

    usage_df = get_current_month_usage_df(email)
    used_pic = usage_df['generations'].sum()

    if is_free_user:
        if used_pic >= FREE_USER_MAX_PIC:
            return False, "Przekroczono limit, subskrybuj naszą usługę, aby móc generować więcej obrazów."

    else:
        if used_pic >= PREMIUM_USER_MAX_PIC:
            return False, "Przekroczono limit obrazów, poczekaj do końca miesiąca."

    return True, ""

def is_content_appropriate(user_input):
    response = openai_client.moderations.create(
    model="omni-moderation-latest",
    input= base_prompt + user_input,
)
    category_scores = response.results[0].category_scores.model_dump()

    for category, score in category_scores.items():
        if score > 0.02:
            st.write(f"Alert: Treść jest nieodpowiednia, dokonaj zmian")
            return False
        else

#### MAIN ####

def main():
    col1, col2, col3 = st.columns([5, 8, 5])
    with col2:
        st.image(os.path.join("appart", "BEZ TLA.png"))
    st.markdown(opis_aplikacji, unsafe_allow_html=True)
    st.markdown("<br><br>", unsafe_allow_html=True)   

    try:
        add_auth(
            required=False,
            login_sidebar=False,
            login_button_text="Zaloguj się",
        )
    except KeyError:
        pass

    if st.session_state.get('email'):
        allow, msg = allow_usage()
        if not allow:
            st.error(msg)
        else:
            cols = st.columns(3)
            for index, item in enumerate(main_images):
                with cols[index]:
                    st.image(item["image"], width=220)
                    if st.button(item["name"], use_container_width=True):
                        st.session_state.selected_main = item["name"]
                        st.session_state.generated_images = []

            if 'selected_main' in st.session_state and st.session_state.selected_main == "Inne":
                user_input = st.text_area("Napisz jaki obrazek chcesz wygenerować:", height=200, max_chars=30)
                st.session_state['user_input'] = user_input
                is_disabled = not st.session_state['user_input'].strip()

                if st.button("Wygeneruj obraz", disabled=is_disabled) and st.session_state['user_input'].strip():
                    try:
                        if is_content_appropriate(user_input):
                            image_url = generate_image(f"{base_prompt} {st.session_state['user_input']}")
                            st.session_state['generated_images'].append(("Własny obraz", image_url))
                            st.write("Tresc jest odpowiednia")
                        else:
                            st.warning("Podany tekst nie jest odpowiedni. Proszę spróbować ponownie.")
                    except Exception as e:
                        st.error(f"Wystąpił błąd: {e}")

            if 'selected_main' in st.session_state and st.session_state.selected_main in ["Zwierzaki", "Pojazdy"]:
                sub_images = sub_animal if st.session_state.selected_main == "Zwierzaki" else sub_vehicles
                sub_cols = st.columns(5)
                for index, (name, path) in enumerate(sub_images.items()):
                    with sub_cols[index % 5]:
                        st.image(path)
                        if st.button(name, use_container_width=True):
                            image_url = generate_image(options[name] + f" Obraz: {name}")
                            st.session_state['generated_images'].append((name, image_url))

            if st.session_state['generated_images']:
                name, image_url = st.session_state['generated_images'][-1]
                st.image(image_url, caption=f"Obraz {name}")

                try:
                    image_data = download_image(image_url)
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

    with st.sidebar:
        st.image(os.path.join("appart", "BEZ TLA.png"), width=180)
        st.link_button("Polityka prywatności", "https://garr.fra1.cdn.digitaloceanspaces.com/CreativePaintings/privacy_policy.pdf")
        st.link_button("Regulamin", "https://garr.fra1.cdn.digitaloceanspaces.com/CreativePaintings/regulations.pdf")

        if st.session_state.get('email'):
            account, stats = st.tabs(["Konto", "Statystyki"])
            with account:
                st.write(f"Jesteś zalogowano jako: {st.session_state['email']}")
                st.write(f"Aktywna subskrypcja: {'**Premium**' if st.session_state.get('user_subscribed') else '**Darmowa**'}")

            with stats:
                usage_df = get_current_month_usage_df(st.session_state['email'])
                st.write(f"Wykorzystane obrazki")
                max_pic = FREE_USER_MAX_PIC if not st.session_state.get("user_subscribed") else PREMIUM_USER_MAX_PIC
                st.metric(" ", f"{usage_df['generations'].sum()} / {max_pic}")

if __name__ == "__main__":
    main()