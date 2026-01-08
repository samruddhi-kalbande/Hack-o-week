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
   ```bash
   pip install -r requirements.txt
   ```

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
Built by [Your Name] for the Hack-o-Week challenge.
