import streamlit as st
import os
import time
import glob
import os
from gtts import gTTS
from PIL import Image
import base64

# Cambia el fondo a negro y el texto a blanco puro, incluyendo los labels
st.markdown(
    """
    <style>
    body, .stApp {
        background-color: #000000 !important;
        color: #FFFFFF !important;
    }
    label, .css-1cpxqw2, .css-1y0tads, .css-1n76uvr, .css-1y4p8pa, .css-1c7y2kd, .stTextInput label, .stTextArea label {
        color: #FFFFFF !important;
    }
    .stTextInput > div > div > input,
    .stTextArea > div > textarea {
        background-color: #222222 !important;
        color: #FFFFFF !important;
    }
    .stButton>button {
        color: #FFFFFF !important;
        background-color: #222222 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<h1 style="color: red;">Conversión de Texto a Audio</h1>', unsafe_allow_html=True)
image = Image.open('imagen_raton_gato.png')
st.image(image, width=350)
with st.sidebar:
    st.subheader("Esrcibe y/o selecciona texto para ser escuchado.")

try:
    os.mkdir("temp")
except:
    pass

st.subheader("Fragmento de Caperucita Roja")
st.write('<span style="color: #FFFFFF;">Había una vez una dulce niña que era querida por todos, especialmente por su abuela, quien le regaló una capa roja. Un día, su madre le pidió que llevara una cesta con comida a su abuela enferma, advirtiéndole que no hablara con extraños en el bosque. En el camino, Caperucita Roja se encontró con un lobo que, astutamente, la distrajo y llegó antes que ella a la casa de la abuela...</span>', unsafe_allow_html=True)
st.markdown('<span style="color: #FFFFFF;">¿Quieres escucharlo? Copia el texto o escribe el tuyo propio.</span>', unsafe_allow_html=True)
text = st.text_area("Ingrese el texto a escuchar.")

tld='com'
option_lang = st.selectbox(
    "Selecciona el lenguaje",
    ("Español", "English"))
if option_lang=="Español" :
    lg='es'
if option_lang=="English" :
    lg='en'

def text_to_speech(text, tld,lg):
    tts = gTTS(text,lang=lg) # tts = gTTS(text,'en', tld, slow=False)
    try:
        my_file_name = text[0:20]
    except:
        my_file_name = "audio"
    tts.save(f"temp/{my_file_name}.mp3")
    return my_file_name, text

#display_output_text = st.checkbox("Verifica el texto")

if st.button("convertir a Audio"):
     result, output_text = text_to_speech(text, 'com',lg)#'tld
     audio_file = open(f"temp/{result}.mp3", "rb")
     audio_bytes = audio_file.read()
     st.markdown(f"<span style='color: #FFFFFF;'>## Tu audio:</span>", unsafe_allow_html=True)
     st.audio(audio_bytes, format="audio/mp3", start_time=0)

     #if display_output_text:
     #st.write(f" {output_text}")

#if st.button("ElevenLAabs",key=2):
#     from elevenlabs import play
#     from elevenlabs.client import ElevenLabs
#     client = ElevenLabs(api_key="a71bb432d643bbf80986c0cf0970d91a", # Defaults to ELEVEN_API_KEY)
#     audio = client.generate(text=f" {output_text}",voice="Rachel",model="eleven_multilingual_v1")
#     audio_file = open(f"temp/{audio}.mp3", "rb")

     with open(f"temp/{result}.mp3", "rb") as f:
         data = f.read()

     def get_binary_file_downloader_html(bin_file, file_label='File'):
        bin_str = base64.b64encode(data).decode()
        href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download {file_label}</a>'
        return href
     st.markdown(get_binary_file_downloader_html(f"temp/{result}.mp3", file_label="Audio File"), unsafe_allow_html=True)
     st.markdown("<b style='color: #FFFFFF;'>Gracias por usar nuestra aplicación</b>", unsafe_allow_html=True)

def remove_files(n):
    mp3_files = glob.glob("temp/*mp3")
    if len(mp3_files) != 0:
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)
                print("Deleted ", f)

remove_files(7)

