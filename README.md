# 🇮🇳 Indian Language NLP Analyzer

A powerful Flask-based web application for analyzing text in Indian languages with advanced NLP features including word frequency analysis, sentiment analysis, and named entity recognition.

## ✨ Features

- **📊 Word Frequency Analysis** - Identify the most common words in your text
- **😊 Sentiment Analysis** - Detect positive, negative, or neutral sentiment
- **🏷️ Named Entity Recognition** - Identify persons and entities in the text
- **📈 Text Statistics** - Get comprehensive statistics about your text
- **🎯 Stopword Removal** - Filter out common words for better analysis
- **🌐 Multi-language Support** - Supports Hindi, Gujarati, and Marathi

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python analyzer.py
```

3. Open your browser and navigate to:
```
http://localhost:5000
```

## 📖 Usage

1. **Enter text** in Hindi, Gujarati, or Marathi in the text area
2. **Select the language** from the dropdown menu
3. **Configure options**:
   - Number of top words to display (1-50)
   - Toggle stopword removal on/off
4. **Click "Analyze Text"** to see results

### Example Texts

**Hindi:**
```
यह एक बहुत अच्छा दिन है। मुझे बहुत खुशी हो रही है।
```

**Gujarati:**
```
આજે એક સુંદર દિવસ છે। હું ખૂબ ખુશ છું।
```

**Marathi:**
```
आज एक चांगला दिवस आहे। मला खूप आनंद होत आहे।
```

## 🏗️ Architecture

### Backend (`analyzer.py`)
- **Flask** web framework
- **IndianLanguageAnalyzer** class with methods:
  - `tokenize_text()` - Enhanced tokenization for Indic scripts
  - `remove_stopwords()` - Filters common stopwords
  - `get_word_frequency()` - Calculates word frequencies
  - `analyze_sentiment()` - Performs sentiment analysis
  - `extract_entities()` - Basic named entity recognition

### Frontend (`templates/index.html`)
- Modern, responsive design with gradient theme
- Real-time API communication
- Interactive visualizations with progress bars
- Separate cards for statistics, sentiment, entities, and word frequency

## 🔧 API Endpoints

### POST `/analyze`
Analyzes text and returns comprehensive results.

**Request:**
```json
{
  "text": "यह एक अच्छा दिन है",
  "language": "hindi",
  "top_n": 10,
  "remove_stopwords": true
}
```

**Response:**
```json
{
  "top_words": [
    {"word": "अच्छा", "frequency": 1},
    {"word": "दिन", "frequency": 1}
  ],
  "statistics": {
    "total_words": 4,
    "unique_words": 4,
    "unique_words_after_stopwords": 2,
    "avg_word_length": 2.5
  },
  "sentiment": {
    "sentiment": "positive",
    "score": 1.0,
    "positive_words": 1,
    "negative_words": 0
  },
  "entities": [
    {"text": "entity_name", "type": "PERSON", "context": "श्री"}
  ],
  "language": "hindi"
}
```

### GET `/health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "Indian Language NLP Analyzer"
}
```

## 🌍 Supported Languages & Scripts

| Language | Script | Unicode Range |
|----------|--------|---------------|
| Hindi | Devanagari | U+0900-U+097F |
| Marathi | Devanagari | U+0900-U+097F |
| Gujarati | Gujarati | U+0A80-U+0AFF |
| Bengali* | Bengali | U+0980-U+09FF |
| Tamil* | Tamil | U+0B80-U+0BFF |
| Telugu* | Telugu | U+0C00-U+0C7F |
| Kannada* | Kannada | U+0C80-U+0CFF |
| Malayalam* | Malayalam | U+0D00-U+0D7F |

*Tokenization supported, full features coming soon

## 📊 Stopwords Coverage

- **Hindi**: 60+ common stopwords
- **Gujarati**: 45+ common stopwords
- **Marathi**: 50+ common stopwords

## 🎯 Sentiment Analysis

Uses dictionaries of positive and negative words for each language:
- **Hindi**: 23 positive, 23 negative words
- **Gujarati**: 16 positive, 15 negative words
- **Marathi**: 15 positive, 15 negative words

Sentiment is calculated based on the ratio of positive to negative words:
- **Positive**: Score > 0.2
- **Negative**: Score < -0.2
- **Neutral**: Score between -0.2 and 0.2

## 🔮 Future Enhancements

- [ ] Add more Indian languages (Tamil, Telugu, Bengali, etc.)
- [ ] Integrate advanced NER with spaCy/Stanza
- [ ] Add Part-of-Speech (POS) tagging
- [ ] Implement n-gram analysis
- [ ] Add text summarization
- [ ] Export results to CSV/JSON
- [ ] Add language auto-detection
- [ ] Batch processing support
- [ ] API authentication and rate limiting

## 🛠️ Development

### Project Structure
```
indian-language-nlp-analyzer/
├── analyzer.py              # Flask backend
├── templates/
│   └── index.html          # Frontend UI
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

### Running Tests
```bash
# Test the health endpoint
curl http://localhost:5000/health

# Test the analyze endpoint
curl -X POST http://localhost:5000/analyze \
  -H "Content-Type: application/json" \
  -d '{"text":"यह एक अच्छा दिन है","language":"hindi","top_n":10,"remove_stopwords":true}'
```

## 📝 License

This project is open source and available for educational purposes.

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Adding more languages and stopwords
- Improving sentiment dictionaries
- Enhancing entity recognition
- Adding more NLP features
- UI/UX improvements

## 💡 Tips

- Use **Ctrl+Enter** (or **Cmd+Enter** on Mac) to quickly analyze text
- Adjust the number of top words to see more or fewer results
- Try disabling stopword removal to see all words in your text
- The sentiment analysis works best with longer texts

## 📧 Support

For issues or questions, please create an issue in the repository.

---

**Built with ❤️ for Indian language processing**
