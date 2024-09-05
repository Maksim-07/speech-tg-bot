from gtts import gTTS


def text_to_voice(text, language="ru"):
    tts = gTTS(text=text, lang=language)
    tts.save("voice.ogg")
    return "voice.ogg"
