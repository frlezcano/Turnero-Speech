import flet as ft
from gtts import gTTS
import subprocess

def text_to_voice(text, output, lang, volume, speed, output_format):
    output_mp3 = f"{output}.mp3"
    output_wav = f"{output}.wav"
    gTTS.GOOGLE_TTS_MAX_CHARS = 200

    # Crear archivo MP3
    tts = gTTS(text=text, lang=lang, tld="com")
    tts.save(output_mp3)

    # Ajustar volumen y velocidad con FFMPEG
    if output_format == "wav":
        ffmpeg_command = (
            f'ffmpeg -y -i "{output_mp3}" -filter:a "atempo={speed},volume={volume}" -vn "{output_wav}"'
        )
        subprocess.run(ffmpeg_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return output_wav
    elif output_format == "mp3":
        adjusted_mp3 = f"{output}_adjusted.mp3"
        ffmpeg_command = (
            f'ffmpeg -y -i "{output_mp3}" -filter:a "atempo={speed},volume={volume}" -vn "{adjusted_mp3}"'
        )
        subprocess.run(ffmpeg_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return adjusted_mp3

def main(page: ft.Page):
    page.title = "Generador de Audio para Turnero"
    page.window.width = 850
    page.window.height = 510
    ## page.window.resizable = False

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
            output_format=format_dropdown.value,  # Formato de salida
        )

        result_label.value = f"Audio generado: {generated_file}"
        result_label.visible = True
        play_button.visible = True
        separador_label.visible = True
        save_button.visible = True
        new_button.visible = True
        page.update()

    # Función para reproducir el audio generado
    def play_audio(e):
        if generated_file:
            subprocess.run(["ffplay", "-nodisp", "-autoexit", generated_file])

    # Función para manejar cambios en los sliders
    def update_volume_label(e):
        volume_label.value = f"Volumen: {round(volume_slider.value, 1)}"
        page.update()

    def update_speed_label(e):
        speed_label.value = f"Velocidad: {round(speed_slider.value, 1)}"
        page.update()

    def new_audio(e):
        result_label.visible = False
        play_button.visible = False
        separador_label.visible = False
        save_button.visible = False
        new_button.visible = False
        page.update()



    # Configuración del FilePicker
    file_picker = ft.FilePicker(on_result=save_file_dialog_result)
    page.overlay.append(file_picker)

    # Controles de entrada
    text_field = ft.TextField(label="Texto (máximo 200 caracteres)", max_length=200, color="#3c73ce")
    lang_dropdown = ft.Dropdown(
        label="Selecciona el idioma",
        color="#3c73ce",
        options=[
            ft.dropdown.Option("es", "Español"),
            ft.dropdown.Option("en", "Inglés"),
            ft.dropdown.Option("fr", "Francés"),
        ],
        value="es",
    )
    format_dropdown = ft.Dropdown(
        label="Formato de salida",
        color="#3c73ce",
        options=[
            ft.dropdown.Option("wav", "WAV"),
            ft.dropdown.Option("mp3", "MP3"),
        ],
        value="wav",  # Por defecto WAV
    )
    volume_slider = ft.Slider(
        label="Volumen",
        min=0.5,
        max=2.0,
        value=1.0,
        on_change=update_volume_label,
    )
    speed_slider = ft.Slider(
        label="Velocidad",
        min=0.5,
        max=2.0,
        value=1.0,
        on_change=update_speed_label,
    )

    text_title = ft.Text("Turnero-Speech", size=28)
    volume_label = ft.Text(value="Volumen: 1.0",color="#3c73ce")
    speed_label = ft.Text(value="Velocidad: 1.0",color="#3c73ce")
    separador_label = ft.Text(value="  -->  ",color="#3c73ce", visible=False)

    # Botones y resultados
    generate_button = ft.ElevatedButton("Generar", on_click=generate_audio)
    play_button = ft.ElevatedButton("Reproducir", on_click=play_audio, visible=False)
    save_button = ft.ElevatedButton(
        "Guardar",
        on_click=lambda e: file_picker.save_file(),
        visible=False,
    )
    new_button = ft.ElevatedButton("Nuevo", on_click=new_audio, visible=False)
    result_label = ft.Text(visible=False,color="#3c73ce")

    # Layout
    page.add(
        ft.Container(
            content=ft.Row(
                [
                    ft.Container(     # Espacio vacío a la izquierda
                        expand=True,
                        padding=ft.padding.all(0),
                        content =ft.Column(
                            controls=[
                                ft.Container(
                                    content=text_title,
                                    alignment=ft.alignment.center,  # Alinea al centro
                                ),
                            ]
                        )                
                    ),
                    ft.Container(     # Espacio vacío a la derecha
                        expand=True,
                        padding=ft.padding.all(30),
                        content =ft.Column(
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                ## ft.Row(),
                                text_field,
                                lang_dropdown,
                                format_dropdown,
                                ft.Row([volume_slider, volume_label]),
                                ft.Row([speed_slider, speed_label]),
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    controls=[                                                                    
                                        generate_button,
                                        ## separador_label,
                                        play_button, 
                                    ]
                                ),
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    controls=[  
                                        result_label,
                                    ]
                                ),
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    controls=[
                                        save_button,
                                        ## separador_label,
                                        new_button,
                                    ]
                                )
                            ]
                        )                
                    )
                ],
                alignment=ft.MainAxisAlignment.END,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            expand=True,
            padding=ft.padding.all(0),
            image_src="images/Turnero-Speech-Background.jpg",  # Ruta a la imagen de fondo
            image_fit=ft.ImageFit.COVER,  # Ajustar la imagen para cubrir toda la página
        )
    )

ft.app(target=main, assets_dir="assets")
