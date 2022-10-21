from googletrans import Translator


def translate(message: str):
    """
    Translate message
    """
    translator = Translator()

    try:
        return translator.translate(text=message, dest="en", src="pt").text
    except:
        return message
