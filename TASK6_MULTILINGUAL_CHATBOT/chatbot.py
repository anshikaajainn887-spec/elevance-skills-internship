from translator import translate_to_english, translate_back
from memory import add_message, get_history

def chatbot_response(user_message):

    english_message, detected_language = translate_to_english(user_message)

    history = get_history()

    if len(history) > 0:
        last_message = history[-1]["message"]
    else:
        last_message = ""

    message = english_message.lower()

    if any(word in message for word in ["hello", "hi", "hey"]):
        response = "Hello! How can I help you today?"

    elif "name" in message:
        response = "I am an AI multilingual chatbot."

    elif any(word in message for word in ["thank", "thanks"]):
        response = "You're welcome!"

    elif any(word in message for word in ["bye", "goodbye"]):
        response = "Goodbye! Have a great day."

    elif "previous" in message or "last" in message:
        if last_message:
            response = f"Our previous conversation was: {last_message}"
        else:
            response = "We haven't talked before in this session."

    else:
        response = "I understand your message. Please tell me more."

    
    add_message("user", english_message)
    add_message("assistant", response)

    
    final_response = translate_back(response, detected_language)

    return {
        "language": detected_language,
        "response": final_response
    }