
# SYMBIOSIS INSTITUTE OF TECHNOLOGY CHATBOT 🎓

An AI-powered hybrid chatbot for college/institute queries using NLP and Machine Learning.

## Features

✅ **TF-IDF Retrieval** - Efficient question matching using Term Frequency-Inverse Document Frequency  
✅ **Intent Classification** - Naive Bayes classifier for categorizing user queries  
✅ **Voice Input** - Speech recognition for hands-free interaction  
✅ **Confidence Scoring** - Shows how confident the bot is about each answer  
✅ **Admin Panel** - Upload and update FAQ data on the fly  
✅ **Modern UI** - Clean, animated Streamlit interface  

## Installation

1. **Clone or download this repository**

2. **Install dependencies:**
=======
# Institute FAQ Chatbot (Week 1)
A rule-based chatbot designed to answer common institute-related queries (FAQs) using simple pattern matching. This project serves as the foundation (Week 1) of a 5-week plan to build an intelligent academic assistant.

## Features
- **Rule-Based Matching**: Answers 15 fixed categories of questions (e.g., timings, fees, admissions).
- **Web Interface**: A clean, modern, and responsive chat UI built with Flask, HTML, CSS, and JS.
- **Glassmorphism Design**: Premium visual aesthetics with animated backgrounds.
- **Extensible Data**: FAQ data is stored in `data.json` for easy updates.

## Project Structure
```
Hack-o-week/
├── app.py              # Flask application entry point
├── chatbot_logic.py    # Logic for processing user input
├── data.json           # FAQ dataset (intents, patterns, responses)
├── requirements.txt    # Python dependencies
├── static/
│   ├── style.css       # CSS styles
│   └── script.js       # Frontend JavaScript
└── templates/
    └── index.html      # Main HTML page
```

## Installation
1. **Clone the repository** (or navigate to the project folder):
   ```bash
   cd Hack-o-week
   ```

2. **Install dependencies**:
>>>>>>> d5e8a4b050bb30d9982bf93ea54cd3298a02baac
   ```bash
   pip install -r requirements.txt
   ```

<<<<<<< HEAD
3. **Run the application:**
   ```bash
   streamlit run app.py
   ```

4. **Open in browser:**
   The app will automatically open at `http://localhost:8501`

## Usage

- Type your question in the chat input
- Or click the 🎤 button to use voice input
- The bot will respond with relevant answers and confidence scores
- Use the admin panel to upload new FAQ CSV files

## FAQ Data Format

The `faq_data.csv` file should have three columns:
- `question` - The user's question
- `answer` - The bot's response
- `intent` - Category (admissions, fees, exams, hostel, scholarship, etc.)

## Technologies Used

- **Streamlit** - Web interface
- **Pandas** - Data handling
- **Scikit-learn** - TF-IDF vectorization and Naive Bayes classification
- **SpeechRecognition** - Voice input processing

## Project Structure

```
Hack-o-week/
├── app.py              # Main Streamlit application
├── faq_data.csv        # FAQ dataset
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Future Enhancements

- Add more FAQ categories
- Implement context-aware conversations
- Add multilingual support
- Deploy to cloud platform

## License

This project is created for educational purposes.
=======
3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Access the Chatbot**:
   Open your browser and navigate to `http://localhost:8000`.

## Dataset
The project currently uses a mixed dataset stored in `data.json`.
- **Base Data**: Fixed 15 FAQs designed for the Week 1 requirements.
- **Imported Data**: General conversational intents (greeting, goodbye, etc.) and college-specific queries imported from the [College Enquiry Chatbot](https://github.com/abhik-b/college-enquiry-chatbot) dataset, which is a common resource also found on Kaggle.

Structure of `data.json`:
- `tag`: Category label.
- `patterns`: List of user query keywords/phrases.
- `responses`: List of bot answers.

## Roadmap
- **Week 1**: Basic Rule-Based FAQ Responder (Completed)
- **Week 2**: Preprocessing Student Queries (Tokenization, Stopword removal).
- **Week 3**: Synonym-Aware FAQ Bot.
- **Week 4**: FAQ Retrieval with TF-IDF.
- **Week 5**: Intent Classification with Machine Learning.

## Author
Built by Samruddhi Kalbande,Ishika Dubey & Samruddhi Kalbande for the Hack-o-Week challenge.
