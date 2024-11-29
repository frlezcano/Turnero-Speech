import flet as ft
from gtts import gTTS
import subprocess
import os
from io import BytesIO

def text_to_voice(text, output, lang, volume, speed):
    output_mp3 = f"{output}.mp3"
    output_wav = f"{output}.wav"
    gTTS.GOOGLE_TTS_MAX_CHARS = 200

    # Crear archivo MP3
    tts = gTTS(text=text, lang=lang, tld="com")
    tts.save(output_mp3)

    # Ajustar volumen y velocidad con FFMPEG
    ffmpeg_command = (
        f'ffmpeg -y -i "{output_mp3}" -filter:a "atempo={speed},volume={volume}" -vn "{output_wav}"'
    )
    subprocess.run(ffmpeg_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    return output_wav


def main(page: ft.Page):
    # Función para gestionar el botón de generación
    def generate_audio(e):
        if len(text_field.value) > 200:
            page.dialog = ft.AlertDialog(
                title=ft.Text("Error"),
                content=ft.Text("El texto no puede exceder los 200 caracteres."),
            )
            page.dialog.open = True
            page.update()
            return

        # Generar el archivo de audio
        output_file = text_to_voice(
            text=text_field.value,
            output="output_audio",
            lang=lang_dropdown.value,
            volume=volume_slider.value,
            speed=speed_slider.value,
        )

        result_label.value = f"Audio generado: {output_file}"
        result_label.visible = True
        play_button.visible = True
        save_button.visible = True
        page.update()

    # Función para reproducir el audio generado
    def play_audio(e):
        subprocess.run(["ffplay", "-nodisp", "-autoexit", "output_audio.wav"])

    # Función para guardar el archivo de audio
    def save_audio(e):
        file_picker.save_file("output_audio.wav")

    # Controles de entrada
    text_field = ft.TextField(label="Texto (máximo 200 caracteres)", max_length=200)
    lang_dropdown = ft.Dropdown(
        label="Selecciona el idioma",
        options=[
            ft.dropdown.Option("es", "Español"),
            ft.dropdown.Option("en", "Inglés"),
            ft.dropdown.Option("fr", "Francés"),
        ],
        value="es",
    )
    volume_slider = ft.Slider(label="Volumen", min=0.5, max=2.0, value=1.0, step=0.1)
    speed_slider = ft.Slider(label="Velocidad", min=0.5, max=2.0, value=1.0, step=0.1)

    # Botones y resultados
    generate_button = ft.ElevatedButton("Generar", on_click=generate_audio)
    play_button = ft.ElevatedButton("Reproducir", on_click=play_audio, visible=False)
    save_button = ft.ElevatedButton("Guardar", on_click=save_audio, visible=False)
    result_label = ft.Text(visible=False)

    # Layout
    page.add(
        ft.Column(
            [
                text_field,
                lang_dropdown,
                volume_slider,
                speed_slider,
                generate_button,
                result_label,
                play_button,
                save_button,
            ]
        )
    )


ft.app(target=main)
