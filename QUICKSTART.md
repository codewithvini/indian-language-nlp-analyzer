# 🚀 Quick Start Guide

## ✅ Your Application is Now Running!

The server is currently running at: **http://localhost:5000**

### 📖 How to Use

1. **Open your web browser** (Chrome, Firefox, Edge, Safari)

2. **Navigate to**: `http://localhost:5000`

3. **Enter text** in the text area (English, Hindi, or Gujarati)

4. **Select your language**: English, Gujarati, or Hindi

5. **Click "Analyze Text"** and see the results!

---

## 📝 Example Texts to Try

### English
```
This is a great day. I am very happy and excited.
The weather is wonderful and beautiful today.
```

### Gujarati (ગુજરાતી)
```
આજે એક સુંદર દિવસ છે। હું ખૂબ ખુશ છું।
આ સરસ મોસમ છે। મને ખૂબ આનંદ થાય છે।
```

### Hindi (हिन्दी)
```
यह एक बहुत अच्छा दिन है। मुझे बहुत खुशी हो रही है।
आज का मौसम बहुत सुंदर है। मैं बहुत प्रसन्न हूं।
```

---

## 🔍 What You'll See

### 1. **Statistics Card** 📊
- Total words in your text
- Unique words count
- Words after removing stopwords
- Average word length

### 2. **Sentiment Analysis** 😊😐😞
- Overall sentiment (Positive/Neutral/Negative)
- Sentiment score
- Count of positive and negative words

### 3. **Named Entities** 🏷️
- Detected persons and entities
- Entity types and context

### 4. **Top Words** 🔤
- Most frequent words with visual bars
- Word frequency counts
- Interactive hover effects

---

## ⚙️ Settings You Can Adjust

- **Number of top words**: 1-50 (default: 10)
- **Remove stopwords**: Toggle on/off to include/exclude common words

---

## 🎯 Pro Tips

- Use **Ctrl+Enter** (or **Cmd+Enter** on Mac) to quickly analyze
- Try longer texts for better sentiment analysis
- Disable stopword removal to see ALL words
- Compare sentiment across different languages

---

## 🛑 To Stop the Server

Press **Ctrl+C** in the terminal where the server is running

---

## 🔄 To Restart Later

Just run:
```bash
./start.sh
```

Or manually:
```bash
source venv/bin/activate
python analyzer.py
```

---

## 🐛 Troubleshooting

### Can't access the page?
- Make sure the server is running (check terminal for output)
- Try `http://127.0.0.1:5000` instead
- Check if another application is using port 5000

### Error messages?
- Check the terminal for error details
- Make sure virtual environment is activated
- Verify all dependencies are installed

### Need help?
- Check the full [README.md](README.md) for detailed documentation
- Run `python test_analyzer.py` to test basic functionality

---

## 📁 Project Files

- `analyzer.py` - Main Flask application
- `templates/index.html` - Web interface
- `requirements.txt` - Python dependencies
- `test_analyzer.py` - Test script
- `start.sh` - Quick start script
- `README.md` - Full documentation

---

**Built with ❤️ for Indian language processing**

Enjoy analyzing! 🎉
