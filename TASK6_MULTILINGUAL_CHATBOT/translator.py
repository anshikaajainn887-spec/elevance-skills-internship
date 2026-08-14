from langdetect import detect
from deep_translator import GoogleTranslator

SUPPORTED_LANGUAGES = {
    "en": "English",
    "hi": "Hindi",
    "es": "Spanish",
    "fr": "French",
    "de": "German"
}

def detect_language(text):
    try:
        lang = detect(text)

        if lang not in SUPPORTED_LANGUAGES:
            lang = "en"

        return lang

    except:
        return "en"


def translate_to_english(text):

    lang = detect_language(text)

    if lang == "en":
        return text, lang

    translated = GoogleTranslator(
        source="auto",
        target="en"
    ).translate(text)

    return translated, lang


def translate_back(text, lang):

    if lang == "en":
        return text

    return GoogleTranslator(
        source="en",
        target=lang
    ).translate(text)