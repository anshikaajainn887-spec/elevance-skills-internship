from flask import Flask, request, jsonify, render_template
from PIL import Image
import json
import os
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

MEMORY_FILE = "memory.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            try:
                return json.load(f)
            except:
                return []
    return []

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=4)

def extract_image_evidence(image_path, filename):
    try:
        img = Image.open(image_path)
        width, height = img.size
        format_type = img.format
        mode = img.mode
        evidence = f"Image Evidence: Filename {filename}, Format {format_type}, Dimensions {width}x{height}, Color Mode {mode}"
        return evidence, True
    except Exception as e:
        return f"Image processing failed: {str(e)}", False

def detect_ambiguity(user_text, image_evidence):
    if not user_text and not image_evidence:
        return "Input required. Please provide text or image for analysis.", 0.2
    if len(user_text.strip()) < 3 and not image_evidence:
        return "Query too short. Please provide more details for accurate analysis.", 0.4
    if user_text.lower() in ["hi", "hello", "hey"] and not image_evidence:
        return "Hello! I am a multi-modal AI assistant. Please provide a question with text or upload an image.", 0.5
    return None, 1.0

def generate_contextual_response(user_text, image_evidence, history, image_valid):
    context_summary = ""
    if history:
        recent_queries = [h['query'] for h in history[-2:] if h.get('query')]
        if recent_queries:
            context_summary = f"Previous context: {'; '.join(recent_queries)}. "
    
    if image_evidence and user_text and image_valid:
        response = f"{context_summary}Based on image analysis: {image_evidence}. Regarding your query '{user_text}', the visual data provides relevant context for intelligent reasoning."
        confidence = 0.92
        validation = "Evidence-based multi-modal response generated"
    elif image_evidence and image_valid:
        response = f"{context_summary}Image analysis complete: {image_evidence}. Please specify your question about this visual content for detailed reasoning."
        confidence = 0.85
        validation = "Image-only evidence extracted successfully"
    elif user_text:
        response = f"{context_summary}Processing text query: '{user_text}'. Analyzing contextual patterns for intelligent response generation."
        confidence = 0.75
        validation = "Text-based contextual reasoning applied"
    else:
        response = "Unable to process. No valid input detected."
        confidence = 0.1
        validation = "Input validation failed"
    
    if confidence < 0.6:
        validation += " | Low confidence detected - clarification recommended"
    
    return response, confidence, validation

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    memory = load_memory()
    user_text = request.form.get("text", "").strip()
    
    image_evidence = None
    image_valid = False
    filename = None
    
    if "image" in request.files:
        image_file = request.files["image"]
        if image_file.filename != '':
            filename = image_file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image_file.save(filepath)
            image_evidence, image_valid = extract_image_evidence(filepath, filename)
    
    ambiguous_response, ambiguity_score = detect_ambiguity(user_text, image_evidence)
    
    if ambiguous_response:
        ai_reply = ambiguous_response
        confidence = ambiguity_score
        validation = "Ambiguity handling protocol activated"
    else:
        ai_reply, confidence, validation = generate_contextual_response(user_text, image_evidence, memory, image_valid)
    
    conversation_history = memory[-5:]
    
    memory.append({
        "timestamp": datetime.now().isoformat(),
        "query": user_text,
        "image_filename": filename,
        "image_evidence": image_evidence,
        "ai_reply": ai_reply,
        "confidence": confidence,
        "validation": validation
    })
    save_memory(memory)
    
    return jsonify({
        "response": ai_reply,
        "image_analysis": image_evidence,
        "confidence_score": round(confidence, 2),
        "validation_status": validation,
        "conversation_history": conversation_history
    })

if __name__ == "__main__":
    app.run(debug=True)