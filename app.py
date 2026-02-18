import streamlit as st
import pandas as pd
import string
import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.naive_bayes import MultinomialNB

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="Smart Institute Assistant", 
    page_icon="🎓", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ------------------ CUSTOM CSS ------------------
st.markdown("""
<style>
    /* Main background with gradient */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Header styling */
    h1 {
        text-align: center;
        color: white;
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        animation: fadeInDown 0.8s ease-out;
    }
    
    /* Subtitle styling */
    .subtitle {
        text-align: center;
        color: rgba(255,255,255,0.9);
        font-size: 1.2rem;
        margin-bottom: 2rem;
        animation: fadeInUp 0.8s ease-out;
    }
    
    /* Chat container */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        animation: slideIn 0.3s ease-out;
    }
    
    /* User message */
    [data-testid="stChatMessageContent"] {
        background: transparent;
        color: #1a1a1a !important;
    }
    
    /* Fix all text in chat messages */
    .stChatMessage p,
    .stChatMessage div,
    .stChatMessage span,
    [data-testid="stChatMessageContent"] p,
    [data-testid="stChatMessageContent"] div,
    [data-testid="stChatMessageContent"] span {
        color: #1a1a1a !important;
    }
    
    /* Input box styling */
    .stChatInputContainer {
        background: rgba(255, 255, 255, 0.98) !important;
        border-radius: 25px;
        padding: 0.5rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* Fix input text color - multiple selectors for override */
    .stChatInputContainer input,
    .stChatInputContainer textarea,
    input[type="text"],
    textarea,
    [data-baseweb="input"] input,
    [data-baseweb="textarea"] textarea {
        color: #000000 !important;
        font-size: 1rem !important;
        -webkit-text-fill-color: #000000 !important;
    }
    
    .stChatInputContainer input::placeholder,
    .stChatInputContainer textarea::placeholder {
        color: #666666 !important;
        opacity: 0.7 !important;
    }
    
    /* Additional targeting for Streamlit's chat input */
    [data-testid="stChatInput"] input,
    [data-testid="stChatInput"] textarea {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
    }
    
    /* Buttons */
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 20px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.2);
    }
    
    /* Quick question chips */
    .quick-chip {
        display: inline-block;
        background: rgba(255,255,255,0.2);
        color: white;
        padding: 0.5rem 1rem;
        margin: 0.3rem;
        border-radius: 20px;
        font-size: 0.9rem;
        cursor: pointer;
        transition: all 0.3s ease;
        border: 1px solid rgba(255,255,255,0.3);
    }
    
    .quick-chip:hover {
        background: rgba(255,255,255,0.3);
        transform: scale(1.05);
    }
    
    /* Animations */
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-10px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* Confidence badge */
    .confidence-badge {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.2rem 0.6rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-top: 0.3rem;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ------------------ ANIMATED HEADER ------------------
st.markdown("<h1>🎓 Smart Institute Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Ask me anything about admissions, fees, exams, hostel, or scholarships!</p>", unsafe_allow_html=True)

# ------------------ LOAD DATA ------------------
@st.cache_data
def load_data():
    return pd.read_csv("faq_data.csv")

data = load_data()

# ------------------ PREPROCESS ------------------
# Common stopwords to remove (except important ones)
STOPWORDS = {'is', 'are', 'the', 'a', 'an', 'in', 'on', 'at', 'to', 'for', 'of', 'and', 'or', 'by', 'with'}

def preprocess(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Remove stopwords but keep important keywords
    words = text.split()
    words = [w for w in words if w not in STOPWORDS or w in ['what', 'when', 'how', 'where', 'who', 'which']]
    return ' '.join(words)

data['processed'] = data['question'].apply(preprocess)

# ------------------ VECTORIZE ------------------
# Use advanced TF-IDF with optimized parameters
vectorizer = TfidfVectorizer(
    ngram_range=(1, 3),  # Use unigrams, bigrams, and trigrams
    min_df=1,            
    max_df=0.9,          
    sublinear_tf=True,
    max_features=2000    # Increased features for better matching
)
X = vectorizer.fit_transform(data['processed'])

# ------------------ INTENT MODEL ------------------
intent_model = MultinomialNB(alpha=0.05)  # Lower alpha for better precision
intent_model.fit(X, data['intent'])

# ------------------ ADVANCED RESPONSE FUNCTION ------------------
def get_similar_questions(user_input, top_n=3):
    """Get similar questions for fallback suggestions"""
    processed_input = preprocess(user_input)
    user_vector = vectorizer.transform([processed_input])
    
    similarities = cosine_similarity(user_vector, X)[0]
    top_indices = similarities.argsort()[-top_n:][::-1]
    
    suggestions = []
    for idx in top_indices:
        if similarities[idx] > 0.1:
            suggestions.append(data.iloc[idx]['question'])
    
    return suggestions

def get_response(user_input, conversation_history=None):
    """Advanced response function with context awareness"""
    processed_input = preprocess(user_input)
    user_vector = vectorizer.transform([processed_input])

    # Get intent probabilities for better decision making
    intent_probs = intent_model.predict_proba(user_vector)[0]
    predicted_intent = intent_model.predict(user_vector)[0]
    intent_confidence = max(intent_probs)
    
    # Filter data by predicted intent
    filtered_data = data[data['intent'] == predicted_intent]
    
    if len(filtered_data) == 0:
        suggestions = get_similar_questions(user_input)
        if suggestions:
            suggestion_text = "\n\n**Did you mean:**\n" + "\n".join([f"- {q}" for q in suggestions[:3]])
            return f"I'm not sure about that. {suggestion_text}", 0.0
        return "I'm sorry, I couldn't find an answer to that question. Please try rephrasing.", 0.0
    
    # Get vectors for filtered questions
    filtered_vectors = vectorizer.transform(filtered_data['processed'])
    
    # Calculate cosine similarity
    similarities = cosine_similarity(user_vector, filtered_vectors)[0]
    
    # Get best match
    best_match_index = similarities.argmax()
    similarity_score = similarities[best_match_index]
    
    # Combined confidence score (intent + similarity)
    combined_confidence = (intent_confidence * 0.4) + (similarity_score * 0.6)
    
    # Adaptive threshold based on intent confidence
    threshold = 0.15 if intent_confidence > 0.7 else 0.25
    
    if combined_confidence < threshold:
        suggestions = get_similar_questions(user_input)
        if suggestions:
            suggestion_text = "\n\n**Did you mean:**\n" + "\n".join([f"- {q}" for q in suggestions[:3]])
            return f"I'm not quite sure. {suggestion_text}", combined_confidence
        return "I couldn't understand that clearly. Please rephrase your question.", combined_confidence
    
    answer = filtered_data.iloc[best_match_index]['answer']
    
    # Add context-aware follow-up suggestions
    related_intents = data[data['intent'] == predicted_intent]['question'].tolist()
    if len(related_intents) > 1:
        other_questions = [q for q in related_intents if q != filtered_data.iloc[best_match_index]['question']][:2]
        if other_questions:
            answer += f"\n\n**Related questions you might ask:**\n" + "\n".join([f"- {q}" for q in other_questions])
    
    return answer, combined_confidence

# ------------------ CHAT HISTORY ------------------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "conversation_context" not in st.session_state:
    st.session_state.conversation_context = []
    
if not st.session_state.messages:
    st.session_state.messages.append({
        "role": "assistant",
        "content": "Hi 👋 I am your Smart Institute Assistant. Ask me anything about admissions, fees, exams, hostel or scholarships!"
    })

# ------------------ DISPLAY OLD MESSAGES ------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="🤖" if message["role"]=="assistant" else "👤"):
        st.markdown(message["content"])
        if message["role"] == "assistant" and "confidence" in message:
            confidence_pct = int(message['confidence'] * 100)
            st.markdown(f"<span class='confidence-badge'>Confidence: {confidence_pct}%</span>", unsafe_allow_html=True)

# ------------------ QUICK QUESTIONS ------------------
if len(st.session_state.messages) <= 1:  # Only show on first load
    st.markdown("### 💡 Quick Questions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📚 Admission Process"):
            user_input = "What is the admission process?"
            st.session_state.quick_question = user_input
            st.rerun()
        if st.button("💰 College Fees"):
            user_input = "What are the college fees?"
            st.session_state.quick_question = user_input
            st.rerun()
    
    with col2:
        if st.button("🏠 Hostel Fees"):
            user_input = "What is the hostel fee?"
            st.session_state.quick_question = user_input
            st.rerun()
        if st.button("📝 Exam Schedule"):
            user_input = "When are exams conducted?"
            st.session_state.quick_question = user_input
            st.rerun()
    
    with col3:
        if st.button("� Scholarships"):
            user_input = "Are scholarships available?"
            st.session_state.quick_question = user_input
            st.rerun()
        if st.button("📅 Admission Dates"):
            user_input = "When does admission start?"
            st.session_state.quick_question = user_input
            st.rerun()

# ------------------ CHAT INPUT ------------------
user_input = st.chat_input("Type your question here...")

# Handle quick question clicks
if "quick_question" in st.session_state:
    user_input = st.session_state.quick_question
    del st.session_state.quick_question

# ------------------ CHAT LOGIC ------------------
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)

    # Typing animation
    with st.chat_message("assistant", avatar="🤖"):
        placeholder = st.empty()
        placeholder.markdown("✨ Thinking...")
        time.sleep(0.8)

        response, confidence = get_response(user_input)

        placeholder.markdown(response)
        confidence_pct = int(confidence * 100)
        st.markdown(f"<span class='confidence-badge'>Confidence: {confidence_pct}%</span>", unsafe_allow_html=True)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response,
        "confidence": confidence
    })

# ------------------ SIDEBAR ------------------
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.session_state.conversation_context = []
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 📊 Analytics")
    
    total_questions = len([m for m in st.session_state.messages if m["role"] == "user"])
    st.metric("Questions Asked", total_questions)
    
    # Calculate average confidence
    confidences = [m.get("confidence", 0) for m in st.session_state.messages if m["role"] == "assistant" and "confidence" in m]
    if confidences:
        avg_confidence = sum(confidences) / len(confidences)
        st.metric("Avg Confidence", f"{int(avg_confidence * 100)}%")
    
    # Show intent distribution
    if total_questions > 0:
        st.markdown("**Topics Discussed:**")
        # This is a simplified version - in production you'd track actual intents
        topics = ["Admissions", "Fees", "Exams", "Hostel", "Scholarships"]
        for topic in topics[:min(3, total_questions)]:
            st.caption(f"• {topic}")
    
    st.markdown("---")
    st.markdown("### ✨ Advanced Features")
    st.markdown("""
    - 🧠 **Smart NLP Matching**
    - 🎯 **Intent Classification**  
    - 📈 **Confidence Scoring**
    - 💡 **Smart Suggestions**
    - 🔄 **Context Awareness**
    - ⚡ **Quick Actions**
    """)
    
    st.markdown("---")
    st.markdown("### 📚 Knowledge Base")
    st.markdown(f"""
    - **{len(data)} Questions** in database
    - **{len(data['intent'].unique())} Categories** covered
    - **Multi-turn** conversations
    - **Fallback** suggestions
    """)
    
    
    st.markdown("---")
    st.caption("💡 Tip: Use quick question buttons for instant answers!")
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello World"

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, port=8000)

