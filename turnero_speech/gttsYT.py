# modulos de terceros
import subprocess

from gtts import gTTS
from io import BytesIO


def textToVoice(texto, salida):
    sal = 'mp3/' + salida + '.mp3'
    sal2 = 'wav/' + salida + '.wav'
    gTTS.GOOGLE_TTS_MAX_CHARS = 200

    tts = gTTS(text=texto, lang='es', tld="com")
    tts.save(sal)

    print('Acelerando audio con FFMPEG')
    # comando = f'ffmpeg -y -i "{sal}" -filter:a "volume=2.0" -vn "{sal2}"'
    comando = f'ffmpeg -y -i "{sal}" -filter:a "atempo=1.2, volume=2.0" -vn "{sal2}"'
    # comando = f'ffmpeg -y -i "{sal}" -filter:a "atempo=1.30" -vn "{sal2}"'
    subprocess.run(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    mp3_fp = BytesIO()
    tts = gTTS('Hola mundo2', 'es')
    tts.write_to_fp(mp3_fp)

    import pyglet

    music = pyglet.resource.media(sal2)
    music.play()
    pyglet.app.run()


textToVoice("Ding Dong", "dinDon")
