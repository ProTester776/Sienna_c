import re
import logging
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flask_limiter import Limiter  # Import Flask-Limiter
from flask_limiter.util import get_remote_address  # Import utility for getting the remote address
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from ctransformers import AutoModelForCausalLM

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5000"}})


# Initialize the limiter with a default rate limit of 5 requests per minute per IP address
limiter = Limiter(
    get_remote_address,
    default_limits=["5 per minute"]
)
# Set up logging
logging.basicConfig(filename='chatbot.log', level=logging.INFO)

# Download required NLTK data
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

# Load and preprocess knowledge base
def load_knowledge_base(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def preprocess_text(text):
    sections = re.split(r'\n(?=[A-Z][a-z]+(?: [A-Z][a-z]+)*\n)', text)
    chunks = []
    for section in sections:
        paragraphs = re.split(r'\n\n+', section)
        for para in paragraphs:
            clean_para = re.sub(r'\s+', ' ', para).strip()
            if len(clean_para.split()) > 5:
                chunks.append(clean_para)
    return chunks

knowledge_base_path = r"C:\Users\PavanPunna\Desktop\sienna_chatbot\knowledge_base.txt"
full_text = load_knowledge_base(knowledge_base_path)
knowledge_chunks = preprocess_text(full_text)

# Initialize TF-IDF vectorizer
vectorizer = TfidfVectorizer(stop_words='english')
chunk_vectors = vectorizer.fit_transform(knowledge_chunks)

# Initialize Orca Mini model
model_path = r"C:\Users\PavanPunna\Desktop\sienna_chatbot\orca-mini-3b.ggmlv3.q4_0.bin"
model = AutoModelForCausalLM.from_pretrained(model_path, model_type="llama")

def get_most_relevant_chunk(query, threshold=0.3):
    query_vector = vectorizer.transform([query])
    similarities = cosine_similarity(query_vector, chunk_vectors)
    most_relevant_index = similarities[0].argmax()
    if similarities[0][most_relevant_index] > threshold:
        relevant_chunk = knowledge_chunks[most_relevant_index]
        if most_relevant_index + 1 < len(knowledge_chunks):
            next_chunk = knowledge_chunks[most_relevant_index + 1]
            if re.search(r'\d{3}-\d{3}-\d{4}|www\.|http', next_chunk):
                relevant_chunk += "\n" + next_chunk
        return relevant_chunk, similarities[0][most_relevant_index]
    return None, 0

def get_orca_response(query):
    prompt = f"### Human: {query}\n### Assistant:"
    response = model(prompt, max_new_tokens=50, temperature=0.7)
    return response.strip()

def preprocess_query(query):
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(query.lower())
    return ' '.join([w for w in word_tokens if w not in stop_words])

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Log the incoming request data
        logging.info(f"Received query: {request.json}")
        
        if not request.json or 'message' not in request.json:
            return jsonify({"error": "Invalid input"}), 400
        
        user_message = request.json['message']
        processed_query = preprocess_query(user_message)
        
        kb_answer, similarity_score = get_most_relevant_chunk(processed_query)
        
        if kb_answer and similarity_score > 0.3:
            formatted_answer = kb_answer.replace("\n", "<br>")
            response = f"<small>According to A GUIDE TO PROGRAMS AND SERVICES FOR SENIORS IN ONTARIO:</small><br>{formatted_answer}"
        else:
            orca_answer = get_orca_response(user_message)
            if orca_answer:
                response = f"According to search results: {orca_answer}"
            else:
                response = "I'm sorry, I don't have specific information about that. Can you please rephrase your question or ask about something else?"
        
        logging.info(f"Response: {response}")
        return jsonify({'response': response})
    except Exception as e:
        logging.error(f"Error in chat function: {str(e)}", exc_info=True)
        return jsonify({"error": "An error occurred processing your request"}), 500

@app.after_request
def add_security_headers(response):
    csp = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' https://code.jquery.com; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' https://www.siennaliving.ca https://sigmahealthtech.com; "
        "font-src 'self'; "
        "object-src 'none';"
    )
    response.headers['Content-Security-Policy'] = csp
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    
    # Add this line for Referrer Policy
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    
    return response

# Preload the model
print("Preloading model...")
model("Warm up", max_new_tokens=1)
print("Model preloaded")

if __name__ == '__main__':
    app.run(debug=True)