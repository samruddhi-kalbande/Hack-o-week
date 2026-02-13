import streamlit as st
import pandas as pd
import string
import time
import speech_recognition as sr
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.naive_bayes import MultinomialNB

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="SYMBIOSIS INSTITUTE OF TECHNOLOGY CHATBOT", page_icon="🎓", layout="centered")

# ------------------ CUSTOM CSS ------------------
st.markdown("""
<style>
body {
    background-color: #0E1117;
    color: white;
}
.stChatMessage {
    border-radius: 15px;
    padding: 10px;
}
h1 {
    text-align: center;
    animation: fadeIn 2s ease-in;
}
@keyframes fadeIn {
    from {opacity: 0;}
    to {opacity: 1;}
}
</style>
""", unsafe_allow_html=True)

# ------------------ ANIMATED HEADER ------------------
st.markdown("<h1>🎓 Smart Institute Assistant</h1>", unsafe_allow_html=True)
st.caption("AI-Powered Hybrid College Chatbot")

# ------------------ LOAD DATA ------------------
@st.cache_data
def load_data():
    return pd.read_csv("faq_data.csv")

data = load_data()

# ------------------ PREPROCESS ------------------
def preprocess(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text

data['processed'] = data['question'].apply(preprocess)

# ------------------ VECTORIZE ------------------
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(data['processed'])

# ------------------ INTENT MODEL ------------------
intent_model = MultinomialNB()
intent_model.fit(X, data['intent'])

# ------------------ RESPONSE FUNCTION ------------------
def get_response(user_input):
    processed_input = preprocess(user_input)
    user_vector = vectorizer.transform([processed_input])

    predicted_intent = intent_model.predict(user_vector)[0]

    filtered_data = data[data['intent'] == predicted_intent]
    filtered_vectors = vectorizer.transform(filtered_data['processed'])

    similarity = cosine_similarity(user_vector, filtered_vectors)
    best_match_index = similarity.argmax()
    confidence = similarity[0][best_match_index]

    if confidence < 0.2:
        return "I'm sorry, I couldn't understand that. Please rephrase your question.", confidence

    answer = filtered_data.iloc[best_match_index]['answer']
    return answer, confidence

# ------------------ CHAT HISTORY ------------------
if "messages" not in st.session_state:
    st.session_state.messages = []
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
            st.caption(f"Confidence: {round(message['confidence'],2)}")

# ------------------ VOICE INPUT ------------------
def voice_to_text():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening...")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            return text
        except:
            return None

col1, col2 = st.columns([5,1])

with col1:
    user_input = st.chat_input("Ask your question here...")

with col2:
    if st.button("🎤"):
        spoken_text = voice_to_text()
        if spoken_text:
            user_input = spoken_text

# ------------------ CHAT LOGIC ------------------
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)

    # Typing animation
    with st.chat_message("assistant", avatar="🤖"):
        placeholder = st.empty()
        placeholder.markdown("Typing...")
        time.sleep(1.5)

        response, confidence = get_response(user_input)

        placeholder.markdown(response)
        st.caption(f"Confidence: {round(confidence,2)}")

    st.session_state.messages.append({
        "role": "assistant",
        "content": response,
        "confidence": confidence
    })

# ------------------ SIDEBAR ADMIN PANEL ------------------
with st.sidebar:
    st.header("⚙ Admin Panel")

    uploaded_file = st.file_uploader("Upload New FAQ CSV", type=["csv"])

    if uploaded_file:
        new_data = pd.read_csv(uploaded_file)
        new_data.to_csv("faq_data.csv", index=False)
        st.success("FAQ Updated! Please Refresh.")

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown("### Features")
    st.write("✔ TF-IDF Retrieval")
    st.write("✔ Intent Classification")
    st.write("✔ Voice Input")
    st.write("✔ Confidence Score")
