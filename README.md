# Turnero-Speech
Generador de audio para el llamador de turnos.

<img width="900" alt="Captura de pantalla 2024-12-03 a la(s) 21 24 17" src="https://github.com/user-attachments/assets/383b4400-6edc-47b7-a5c0-e0b4a36f113b">

# Puede transformar texto a audio 
  Hasta 200 caractéres

# Parametros de Generación de Audio:
* Idioma

  Español,

  Ingles,

  Frances
* Formato de Salida

  mp3
  
  wav
* Volumen

  0.5 - 2
* Velocidad
  
  0.5 -2

Observación: los parámetros aplicados a la generación de audios para producción son los siguientes.
  
 Volumen 1.6
  
 Velocidad 1.2

# Para instalar en Linux/macOS (Windows nunca)

Crea un entorno virtual, luego con poetry instala las dependencias:

   $ cd Turnero-Speech-main

   $ python3 -m venv venv

   $ source venv/bin/activate

   $ poetry install

   $ cd turnero_speech

   $ python3 main.py

En sistemas operativos mas nuevos a la fecha Mayo/2026 la versión de la librería libmpv.so.1 ya no tiene candidatos para instalación, por lo que se recurre a la creación de un link simbólico con el siguiente comando:
  
   $ sudo ln -s /usr/lib/x86_64-linux-gnu/libmpv.so /usr/lib/x86_64-linux-gnu/libmpv.so.1
