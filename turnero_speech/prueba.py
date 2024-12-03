import pyttsx3


def textToVoice(text):
    engine = pyttsx3.init()

    rate = engine.getProperty('rate')
    engine.setProperty('rate', 95)

    volume = engine.getProperty('volume')
    engine.setProperty('volume', 10.0)


    voices = engine.getProperty('voices')
    # engine.setProperty('voices', voices[1].id)
    for voice in voices:
        if "mbrola-es1" in voice.id:
            print(voice)
        """
    if "spanish" in voice.name.lower() and "latin" in voice.name.lower(): """
    """
    if "spanish" in voice.name.lower() and "spanish" in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break

engine.say(text)
engine.runAndWait()
"""


textToVoice("Que podemos querer comer")
