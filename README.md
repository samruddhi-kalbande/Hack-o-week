# Smart Institute Assistant 🎓

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
   ```bash
   pip install -r requirements.txt
   ```

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
