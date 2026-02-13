import json
import os
import string
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Ensure NLTK data is downloaded (using a safe check to avoid excessive re-downloads)
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('tokenizers/punkt_tab')
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('punkt')
    nltk.download('punkt_tab')
    nltk.download('stopwords')

# Load data from JSON file
def load_data():
    try:
        base_path = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(base_path, 'data.json')
        with open(data_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading data: {e}")
        return {"intents": []}

data = load_data()

def preprocess_text(text):
    """
    Week 2: Preprocessing Student Queries
    1. Lowercasing
    2. Punctuation handling
    3. Tokenization
    4. Stopword removal (optional but good for specific keyword matching)
    5. Basic normalization
    """
    # 1. Lowercasing
    text = text.lower()
    
    # 2. Punctuation handling (remove punctuation)
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # 3. Tokenization
    tokens = word_tokenize(text)
    
    # 4. Stopword removal & Normalization
    # We keep words that are NOT stopwords to focus on keywords
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word not in stop_words]
    
    # If filtering removes everything (e.g. user said "the"), fallback to original tokens
    if not filtered_tokens:
        return tokens
        
    return filtered_tokens

def get_response(user_input):
    # Week 2: Use preprocessed tokens for matching
    cleaned_tokens = preprocess_text(user_input)
    
    # Debugging: Print tokens to console to show Week 2 logic is working
    print(f"Processed User Input: {cleaned_tokens}")
    
    # Iterate through intents in the JSON data
    for intent in data['intents']:
        for pattern in intent['patterns']:
            # Week 1 & 2 Hybrid Matching:
            # Check if any important word from the user's input matches the pattern keywords
            # For multi-word patterns in JSON, we might need simple string matching, 
            # but for single key words, token matching is better.
            
            # Simple approach: Check if pattern is IN the text (original behavior) OR matches a token
            
            # 1. Direct Pattern Match (Good for multi-word phrases)
            if pattern.lower() in user_input.lower():
                return intent['responses'][0]
            
            # 2. Token-based Match (Good for keywords)
            # If the pattern is a single word, check if it exists in our cleaned tokens
            if len(pattern.split()) == 1 and pattern.lower() in cleaned_tokens:
                 return intent['responses'][0]

    return "I'm sorry, I didn't understand that. Please ask about timings, fees, courses, or admissions."


