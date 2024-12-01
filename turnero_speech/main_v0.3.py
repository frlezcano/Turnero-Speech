import flet as ft
from gtts import gTTS
import subprocess

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
    generated_file = None  # Variable para guardar la ruta del archivo generado

    # Función para manejar el evento del FilePicker
    def save_file_dialog_result(e: ft.FilePickerResultEvent):
        if e.path:  # Si se seleccionó una ruta válida
            subprocess.run(["cp", generated_file, e.path])
            page.snack_bar = ft.SnackBar(ft.Text("Archivo guardado con éxito!"))
            page.snack_bar.open()
            page.update()

    # Función para generar el archivo de audio
    def generate_audio(e):
        nonlocal generated_file
        if len(text_field.value) > 200:
            page.dialog = ft.AlertDialog(
                title=ft.Text("Error"),
                content=ft.Text("El texto no puede exceder los 200 caracteres."),
            )
            page.dialog.open = True
            page.update()
            return

        # Generar el archivo de audio
        generated_file = text_to_voice(
            text=text_field.value,
            output="output_audio",
            lang=lang_dropdown.value,
            volume=round(volume_slider.value, 1),  # Redondear para más control
            speed=round(speed_slider.value, 1),   # Redondear para más control
        )

        result_label.value = f"Audio generado: {generated_file}"
        result_label.visible = True
        play_button.visible = True
        save_button.visible = True
        page.update()

    # Función para reproducir el audio generado
    def play_audio(e):
        if generated_file:
            subprocess.run(["ffplay", "-nodisp", "-autoexit", generated_file])

    # Configuración del FilePicker
    file_picker = ft.FilePicker(on_result=save_file_dialog_result)
    page.overlay.append(file_picker)

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
    volume_slider = ft.Slider(
        label="Volumen",
        min=0.5,
        max=2.0,
        value=1.0,
        on_change=lambda e: volume_label.update(value=f"Volumen: {round(volume_slider.value, 1)}"),
    )
    speed_slider = ft.Slider(
        label="Velocidad",
        min=0.5,
        max=2.0,
        value=1.0,
        on_change=lambda e: speed_label.update(value=f"Velocidad: {round(speed_slider.value, 1)}"),
    )

    volume_label = ft.Text(value="Volumen: 1.0")
    speed_label = ft.Text(value="Velocidad: 1.0")

    # Botones y resultados
    generate_button = ft.ElevatedButton("Generar", on_click=generate_audio)
    play_button = ft.ElevatedButton("Reproducir", on_click=play_audio, visible=False)
    save_button = ft.ElevatedButton(
        "Guardar",
        on_click=lambda e: file_picker.save_file(),
        visible=False,
    )
    result_label = ft.Text(visible=False)

    # Layout
    page.add(
        ft.Column(
            [
                text_field,
                lang_dropdown,
                ft.Row([volume_slider, volume_label]),
                ft.Row([speed_slider, speed_label]),
                generate_button,
                result_label,
                play_button,
                save_button,
            ]
        )
    )


ft.app(target=main)
