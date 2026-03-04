from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import re
from collections import Counter
import nltk
from nltk.stem import PorterStemmer, SnowballStemmer
from nltk.tokenize import word_tokenize
from nltk.util import bigrams, trigrams

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except (LookupError, OSError):
    print("Downloading NLTK punkt tokenizer...")
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('tokenizers/punkt_tab')
except (LookupError, OSError):
    try:
        print("Downloading NLTK punkt_tab tokenizer...")
        nltk.download('punkt_tab', quiet=True)
    except Exception as e:
        print(f"Note: punkt_tab not available (NLTK version may not require it): {e}")
        pass  # punkt_tab might not be needed for older NLTK versions

app = Flask(__name__)
CORS(app)

class IndianLanguageAnalyzer:
    """Advanced NLP analyzer for Indian languages with sentiment analysis and entity recognition"""

    def __init__(self):
        # Initialize stemmers
        self.porter_stemmer = PorterStemmer()
        self.snowball_stemmer = SnowballStemmer('english')

        # English stopwords
        self.english_stopwords = {
            'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i',
            'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at',
            'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she',
            'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their', 'what',
            'so', 'up', 'out', 'if', 'about', 'who', 'get', 'which', 'go', 'me',
            'when', 'make', 'can', 'like', 'time', 'no', 'just', 'him', 'know', 'take',
            'people', 'into', 'year', 'your', 'good', 'some', 'could', 'them', 'see', 'other',
            'than', 'then', 'now', 'look', 'only', 'come', 'its', 'over', 'think', 'also',
            'back', 'after', 'use', 'two', 'how', 'our', 'work', 'first', 'well', 'way',
            'even', 'new', 'want', 'because', 'any', 'these', 'give', 'day', 'most', 'us',
            'is', 'was', 'are', 'been', 'has', 'had', 'were', 'said', 'did', 'having',
            'may', 'should', 'am', 'being', 'does', 'did', 'done', 'doing'
        }

        # Expanded Hindi stopwords
        self.hindi_stopwords = {
            'का', 'के', 'की', 'को', 'में', 'से', 'पर', 'है', 'हैं', 'था',
            'थे', 'थी', 'हो', 'और', 'या', 'एक', 'यह', 'वह', 'इस', 'उस',
            'ने', 'भी', 'तो', 'ही', 'कि', 'जो', 'कर', 'गया', 'दिया',
            'हुआ', 'हुई', 'हुए', 'कब', 'कहाँ', 'कैसे', 'क्या', 'क्यों',
            'किसी', 'किसे', 'कोई', 'कुछ', 'जब', 'तब', 'जहाँ', 'तहाँ',
            'यहाँ', 'वहाँ', 'सब', 'लिए', 'दिए', 'बाद', 'साथ', 'द्वारा',
            'तक', 'अभी', 'फिर', 'बहुत', 'कम', 'ज्यादा', 'सकता', 'सकते',
            'सकती', 'रहा', 'रहे', 'रही', 'होता', 'होती', 'होते', 'लेकिन',
            'परन्तु', 'किन्तु', 'अगर', 'मगर', 'जैसे', 'वैसे', 'ऐसे', 'कैसे'
        }

        # Expanded Gujarati stopwords
        self.gujarati_stopwords = {
            'અને', 'છે', 'કે', 'તે', 'એ', 'ને', 'માટે', 'સાથે', 'પર', 'થી',
            'આ', 'તો', 'હતી', 'હતા', 'હોય', 'જે', 'પણ', 'હું', 'તું', 'તમે',
            'અમે', 'અમારા', 'તમારા', 'તેમના', 'કોઈ', 'શું', 'ક્યાં', 'ક્યારે',
            'કેવી', 'કેવું', 'કેમ', 'હા', 'ના', 'જો', 'તો', 'પછી', 'પહેલા',
            'વધુ', 'ઓછું', 'ખૂબ', 'ઘણું', 'બધા', 'બધી', 'બધું', 'કરે', 'કરી',
            'કર્યું', 'થયું', 'થયો', 'થયા', 'હશે', 'હતો', 'હતાં', 'રહે', 'રહી'
        }

        # Sentiment word dictionaries (simplified for demo)
        self.english_positive_words = {
            'good', 'great', 'excellent', 'wonderful', 'amazing', 'fantastic', 'awesome',
            'happy', 'joy', 'love', 'beautiful', 'best', 'perfect', 'brilliant', 'superb',
            'delighted', 'pleased', 'success', 'successful', 'win', 'winner', 'victory',
            'positive', 'benefit', 'advantage', 'profit', 'gain', 'improve', 'better',
            'outstanding', 'exceptional', 'magnificent', 'marvelous', 'splendid',
            # Engagement/interest words
            'interesting', 'exciting', 'fascinating', 'engaging', 'compelling', 'captivating',
            'intriguing', 'enjoyable', 'fun', 'entertaining', 'inspiring', 'motivating',
            # Learning/growth words
            'learning', 'educational', 'informative', 'enlightening', 'insightful', 'valuable',
            'useful', 'helpful', 'beneficial', 'productive', 'effective', 'efficient',
            # Satisfaction words
            'satisfied', 'content', 'glad', 'grateful', 'thankful', 'appreciate', 'impressed',
            'proud', 'confident', 'comfortable', 'relaxed', 'calm', 'peaceful',
            # Quality words
            'quality', 'premium', 'superior', 'fine', 'nice', 'lovely', 'pretty', 'cute',
            'elegant', 'stylish', 'modern', 'fresh', 'new', 'innovative', 'creative',
            # More positive adjectives
            'incredible', 'remarkable', 'phenomenal', 'spectacular', 'stunning', 'gorgeous',
            'fabulous', 'terrific', 'tremendous', 'extraordinary', 'sensational', 'glorious',
            'delightful', 'charming', 'pleasant', 'admirable', 'praiseworthy', 'commendable',
            # Smooth/easy/friendly
            'smooth', 'easy', 'simple', 'effortless', 'convenient', 'accessible', 'friendly',
            'welcoming', 'warm', 'kind', 'gentle', 'caring', 'thoughtful', 'considerate',
            # Strong positive
            'powerful', 'strong', 'robust', 'solid', 'reliable', 'trustworthy', 'dependable',
            'consistent', 'stable', 'secure', 'safe', 'protected', 'guaranteed',
            # Achievement
            'achievement', 'accomplished', 'skilled', 'talented', 'gifted', 'capable',
            'competent', 'proficient', 'expert', 'masterful', 'professional'
        }

        self.english_negative_words = {
            'bad', 'terrible', 'awful', 'horrible', 'poor', 'worst', 'sad', 'unhappy',
            'hate', 'angry', 'upset', 'disappointed', 'frustrating', 'annoying', 'difficult',
            'problem', 'issue', 'fail', 'failure', 'loss', 'lost', 'defeat', 'pain',
            'hurt', 'damage', 'harm', 'worry', 'concern', 'fear', 'scared', 'negative',
            'wrong', 'error', 'mistake', 'worse', 'decline', 'drop', 'fall',
            # Aggressive/violent words
            'punch', 'kick', 'hit', 'slap', 'beat', 'attack', 'fight', 'kill', 'die', 'death',
            'violent', 'violence', 'abuse', 'cruel', 'nasty', 'mean', 'rude', 'insult',
            # Extreme negative emotions
            'disgusting', 'gross', 'sick', 'vomit', 'puke', 'terrible', 'dreadful', 'pathetic',
            'useless', 'worthless', 'stupid', 'dumb', 'idiot', 'fool', 'trash', 'garbage',
            'sucks', 'rubbish', 'crap', 'waste', 'disaster', 'catastrophe', 'nightmare',
            # Suffering/distress
            'suffering', 'agony', 'torture', 'misery', 'despair', 'hopeless', 'depressed',
            'depression', 'anxiety', 'stress', 'trauma', 'tragic', 'tragedy', 'miserable',
            # Danger/threat
            'danger', 'dangerous', 'threat', 'threatening', 'warning', 'risk', 'risky',
            'unsafe', 'hazard', 'emergency', 'critical', 'severe', 'serious',
            # Rejection/disapproval
            'reject', 'rejection', 'deny', 'denial', 'refuse', 'disapprove', 'dislike',
            'avoid', 'ignore', 'exclude', 'abandon', 'betray', 'cheat', 'lie', 'fraud',
            # More negative adjectives
            'weak', 'broken', 'flawed', 'defective', 'faulty', 'inferior', 'substandard',
            'inadequate', 'insufficient', 'lacking', 'mediocre', 'unacceptable', 'unpleasant',
            'uncomfortable', 'awkward', 'clumsy', 'sloppy', 'messy', 'dirty', 'filthy',
            'ugly', 'hideous', 'repulsive', 'offensive', 'harsh', 'rough', 'hard',
            'complicated', 'complex', 'confusing', 'unclear', 'ambiguous', 'vague',
            'slow', 'sluggish', 'lazy', 'boring', 'dull', 'bland', 'tasteless', 'stale',
            'old', 'outdated', 'obsolete', 'ancient', 'worn', 'tired', 'exhausted'
        }

        self.hindi_positive_words = {
            'अच्छा', 'सुंदर', 'बढ़िया', 'शानदार', 'उत्कृष्ट', 'खुश', 'प्रसन्न',
            'खुशी', 'आनंद', 'उत्साह', 'सफल', 'जीत', 'प्यार', 'स्नेह', 'मित्र',
            'सुखद', 'लाभ', 'फायदा', 'विकास', 'प्रगति', 'उन्नति', 'महान', 'श्रेष्ठ',
            # Engagement/interest
            'दिलचस्प', 'रोचक', 'मजेदार', 'रोमांचक', 'प्रेरक',
            # Learning/growth
            'सीखना', 'शिक्षाप्रद', 'ज्ञानवर्धक', 'उपयोगी', 'लाभदायक', 'प्रभावी',
            # Satisfaction
            'संतुष्ट', 'आभारी', 'गर्व', 'आत्मविश्वास', 'शांत',
            # Quality
            'गुणवत्ता', 'उत्तम', 'बेहतरीन', 'नया', 'नवीन', 'सृजनात्मक'
        }

        self.hindi_negative_words = {
            'बुरा', 'खराब', 'दुःख', 'गम', 'दुखी', 'नाराज', 'क्रोध', 'गुस्सा',
            'असफल', 'हार', 'घृणा', 'नफरत', 'दुश्मन', 'समस्या', 'मुश्किल',
            'नुकसान', 'हानि', 'पतन', 'बीमार', 'दर्द', 'चिंता', 'भय', 'डर',
            # Aggressive/violent
            'मारना', 'पीटना', 'लड़ाई', 'हमला', 'मारो', 'हिंसा', 'क्रूर',
            # Extreme negative
            'घिनौना', 'गंदा', 'बेकार', 'निकम्मा', 'मूर्ख', 'बेवकूफ', 'कचरा',
            # Suffering
            'पीड़ा', 'यातना', 'निराशा', 'अवसाद', 'तनाव', 'दुर्भाग्य', 'त्रासदी',
            # Danger
            'खतरा', 'खतरनाक', 'धमकी', 'आपातकाल', 'गंभीर',
            # Rejection
            'अस्वीकार', 'इनकार', 'धोखा', 'झूठ', 'धोखाधड़ी', 'छोड़ना'
        }

        self.gujarati_positive_words = {
            'સારું', 'સુંદર', 'સરસ', 'શાનદાર', 'ઉત્તમ', 'ખુશ', 'આનંદ', 'હર્ષ',
            'સફળ', 'જીત', 'પ્રેમ', 'મિત્ર', 'સુખ', 'લાભ', 'વિકાસ', 'પ્રગતિ',
            # Engagement/interest
            'રસપ્રદ', 'રોચક', 'મજાનું', 'રોમાંચક', 'પ્રેરક',
            # Learning/growth
            'શીખવું', 'શૈક્ષણિક', 'માહિતીપ્રદ', 'ઉપયોગી', 'લાભદાયી', 'અસરકારક',
            # Satisfaction
            'સંતુષ્ટ', 'આભારી', 'ગર્વ', 'આત્મવિશ્વાસ', 'શાંત',
            # Quality
            'ગુણવત્તા', 'ઉત્તમ', 'સુંદર', 'નવું', 'નવીન', 'સર્જનાત્મક'
        }

        self.gujarati_negative_words = {
            'ખરાબ', 'દુઃખ', 'ગમ', 'નારાજ', 'ક્રોધ', 'ગુસ્સો', 'અસફળ', 'હાર',
            'ધૃણા', 'દુશ્મન', 'સમસ્યા', 'મુશ્કેલી', 'નુકસાન', 'બીમાર', 'ચિંતા',
            # Aggressive/violent
            'મારવું', 'મારો', 'લડાઈ', 'હુમલો', 'હિંસા', 'ક્રૂર',
            # Extreme negative
            'ઘૃણાસ્પદ', 'ગંદું', 'બેકાર', 'નકામું', 'મૂર્ખ', 'કચરો',
            # Suffering
            'પીડા', 'યાતના', 'નિરાશા', 'તણાવ', 'દુર્ભાગ્ય', 'દુર્ઘટના',
            # Danger
            'ખતરો', 'ખતરનાક', 'ધમકી', 'ગંભીર',
            # Rejection
            'અસ્વીકાર', 'ઇનકાર', 'છેતરપિંડી', 'જૂઠું', 'છોડી'
        }

        self.stopwords = {
            'english': self.english_stopwords,
            'hindi': self.hindi_stopwords,
            'gujarati': self.gujarati_stopwords
        }

        self.positive_words = {
            'english': self.english_positive_words,
            'hindi': self.hindi_positive_words,
            'gujarati': self.gujarati_positive_words
        }

        self.negative_words = {
            'english': self.english_negative_words,
            'hindi': self.hindi_negative_words,
            'gujarati': self.gujarati_negative_words
        }

        # Common name patterns for basic NER
        self.name_patterns = {
            'english': ['Mr.', 'Mrs.', 'Ms.', 'Dr.', 'Prof.', 'Sir', 'Madam'],
            'hindi': ['श्री', 'श्रीमती', 'कुमार', 'कुमारी', 'डॉ', 'प्रो'],
            'gujarati': ['શ્રી', 'શ્રીમતી', 'ડૉ', 'પ્રો']
        }

    def tokenize_text(self, text, language='english', use_nltk=True):
        """Enhanced tokenization for English and Indian languages using NLP libraries"""
        if language == 'english' and use_nltk:
            # Use NLTK for better English tokenization
            try:
                words = word_tokenize(text.lower())
                # Filter only alphabetic words
                words = [word for word in words if word.isalpha()]
            except:
                # Fallback to regex if NLTK fails
                pattern = r'\b[a-zA-Z]+\b'
                words = re.findall(pattern, text.lower())
        elif language == 'english':
            # For English, use standard word tokenization
            pattern = r'\b[a-zA-Z]+\b'
            words = re.findall(pattern, text.lower())
        else:
            # Supports multiple Indic scripts with combining marks
            # Devanagari (Hindi): U+0900-U+097F
            # Gujarati: U+0A80-U+0AFF
            # Bengali: U+0980-U+09FF
            # Tamil: U+0B80-U+0BFF
            # Telugu: U+0C00-U+0C7F
            # Kannada: U+0C80-U+0CFF
            # Malayalam: U+0D00-U+0D7F

            # Remove punctuation first (both English and Indic)
            text = re.sub(r'[।.!?,;:()\[\]{}"\'-]+', ' ', text)

            # This pattern includes base characters AND combining marks (vowel signs, etc.)
            # The + at the end ensures we capture the entire grapheme cluster
            pattern = r'[\u0900-\u097F\u0980-\u09FF\u0A80-\u0AFF\u0B80-\u0BFF\u0C00-\u0CFF\u0D00-\u0D7F]+'
            words = re.findall(pattern, text)
            # Filter out very short words (single combining marks)
            words = [word for word in words if len(word) > 1]
        return words

    def stem_words(self, words, language='english'):
        """Apply stemming to reduce words to their root form"""
        if language == 'english':
            # Use Snowball stemmer for better results
            return [self.snowball_stemmer.stem(word) for word in words]
        else:
            # For Indian languages, return as-is (basic stemming not available)
            return words

    def remove_stopwords(self, words, language='english'):
        """Remove common stopwords using built-in dictionaries"""
        stopwords = self.stopwords.get(language, set())
        filtered_words = [word for word in words if word not in stopwords]
        return filtered_words

    def get_word_frequency(self, text, language='english', remove_stops=True, apply_stemming=False):
        """Get word frequency from text with optional NLP processing"""
        words = self.tokenize_text(text, language, use_nltk=True)

        if remove_stops:
            words = self.remove_stopwords(words, language)

        if apply_stemming:
            words = self.stem_words(words, language)

        word_freq = Counter(words)
        return word_freq

    def get_top_words(self, text, language='english', top_n=10, remove_stops=True, apply_stemming=False):
        """Get top N most frequent words"""
        word_freq = self.get_word_frequency(text, language, remove_stops, apply_stemming)
        return word_freq.most_common(top_n)

    def get_statistics(self, text, language='english', apply_stemming=False):
        """Get comprehensive text statistics with NLP processing"""
        words = self.tokenize_text(text, language, use_nltk=True)
        words_no_stops = self.remove_stopwords(words, language)

        # Get stemmed version if requested
        if apply_stemming and language == 'english':
            stemmed_words = self.stem_words(words_no_stops, language)
            unique_after_stemming = len(set(stemmed_words))
        else:
            unique_after_stemming = len(set(words_no_stops))

        stats = {
            'total_words': len(words),
            'unique_words': len(set(words)),
            'unique_words_after_stopwords': len(set(words_no_stops)),
            'unique_after_stemming': unique_after_stemming if apply_stemming else None,
            'stopwords_removed': len(words) - len(words_no_stops),
            'avg_word_length': sum(len(word) for word in words) / len(words) if words else 0,
            'nlp_processing': {
                'stopword_removal': True,
                'stemming': apply_stemming,
                'tokenization': 'NLTK' if language == 'english' else 'Regex'
            }
        }

        return stats

    def analyze_sentiment(self, text, language='english'):
        """Simple sentiment analysis based on positive/negative word counts"""
        words = self.tokenize_text(text, language, use_nltk=True)

        positive_words = self.positive_words.get(language, set())
        negative_words = self.negative_words.get(language, set())

        pos_count = sum(1 for word in words if word in positive_words)
        neg_count = sum(1 for word in words if word in negative_words)

        # Calculate sentiment score
        total_sentiment_words = pos_count + neg_count

        if total_sentiment_words == 0:
            return {
                'sentiment': 'neutral',
                'score': 0,
                'positive_words': pos_count,
                'negative_words': neg_count
            }

        score = (pos_count - neg_count) / total_sentiment_words

        if score > 0.2:
            sentiment = 'positive'
        elif score < -0.2:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'

        return {
            'sentiment': sentiment,
            'score': round(score, 2),
            'positive_words': pos_count,
            'negative_words': neg_count
        }

    def extract_entities(self, text, language='english'):
        """Basic named entity recognition for English and Indian languages"""
        # Split by appropriate sentence delimiter
        if language == 'english':
            sentences = text.split('.')
        else:
            sentences = text.split('।')  # Devanagari full stop
            if len(sentences) == 1:
                sentences = text.split('.')  # Fallback to English period

        entities = []
        patterns = self.name_patterns.get(language, [])
        stopwords = self.stopwords.get(language, set())

        for sentence in sentences:
            words = self.tokenize_text(sentence, language, use_nltk=True)

            for i, word in enumerate(words):
                # Check if word follows a title pattern
                if i > 0 and words[i-1] in patterns:
                    entities.append({
                        'text': word,
                        'type': 'PERSON',
                        'context': words[i-1]
                    })
                # For English, check for capitalized words in the original text
                elif language == 'english' and len(word) > 2:
                    # Find the word in original text to check capitalization
                    pattern = r'\b' + re.escape(word) + r'\b'
                    matches = re.finditer(pattern, sentence, re.IGNORECASE)
                    for match in matches:
                        original_word = match.group()
                        # Only add if capitalized and not a stopword
                        if original_word[0].isupper() and word.lower() not in stopwords:
                            entities.append({
                                'text': original_word,
                                'type': 'ENTITY',
                                'context': 'capitalized'
                            })
                            break
                # For Indian languages, only add longer words that are not stopwords
                elif language != 'english' and len(word) > 3 and word not in stopwords:
                    # Use word frequency as a heuristic - less common words might be entities
                    entities.append({
                        'text': word,
                        'type': 'ENTITY',
                        'context': 'potential'
                    })

        # Remove duplicates and limit results
        unique_entities = []
        seen = set()
        for entity in entities:
            if entity['text'].lower() not in seen:
                seen.add(entity['text'].lower())
                unique_entities.append(entity)
                if len(unique_entities) >= 15:  # Limit to 15 entities
                    break

        return unique_entities

    def detect_language(self, text):
        """Auto-detect language (English, Hindi, or Gujarati) based on character analysis"""
        if not text or len(text.strip()) == 0:
            return 'english'  # default

        # Count characters in different scripts
        english_chars = len(re.findall(r'[a-zA-Z]', text))
        hindi_chars = len(re.findall(r'[\u0900-\u097F]', text))  # Devanagari
        gujarati_chars = len(re.findall(r'[\u0A80-\u0AFF]', text))  # Gujarati

        total_chars = english_chars + hindi_chars + gujarati_chars

        if total_chars == 0:
            return 'english'

        # Calculate percentages
        english_pct = (english_chars / total_chars) * 100
        hindi_pct = (hindi_chars / total_chars) * 100
        gujarati_pct = (gujarati_chars / total_chars) * 100

        # Determine language based on majority script
        if gujarati_pct > 30:
            return 'gujarati'
        elif hindi_pct > 30:
            return 'hindi'
        else:
            return 'english'

    def get_ngrams(self, text, language='english', n=2, top_n=10, remove_stops=True):
        """Extract n-grams (bigrams or trigrams) from text"""
        words = self.tokenize_text(text, language, use_nltk=True)

        if remove_stops:
            words = self.remove_stopwords(words, language)

        if n == 2:
            ngram_list = list(bigrams(words))
        elif n == 3:
            ngram_list = list(trigrams(words))
        else:
            return []

        # Count frequency of each n-gram
        ngram_freq = Counter(ngram_list)

        # Format as readable phrases
        top_ngrams = []
        for ngram, freq in ngram_freq.most_common(top_n):
            phrase = ' '.join(ngram)
            top_ngrams.append({'phrase': phrase, 'frequency': freq})

        return top_ngrams

    def get_word_cloud_data(self, text, language='english', remove_stops=True, max_words=50):
        """Get word frequency data for word cloud visualization with sentiment colors"""
        words = self.tokenize_text(text, language, use_nltk=True)

        if remove_stops:
            words = self.remove_stopwords(words, language)

        word_freq = Counter(words)

        # Get sentiment word sets
        positive_words = self.positive_words.get(language, set())
        negative_words = self.negative_words.get(language, set())

        # Create word cloud data with sentiment colors
        word_cloud_data = []
        for word, freq in word_freq.most_common(max_words):
            # Determine color based on sentiment
            if word in positive_words:
                color = 'positive'
            elif word in negative_words:
                color = 'negative'
            else:
                color = 'neutral'

            word_cloud_data.append({
                'word': word,
                'frequency': freq,
                'sentiment': color
            })

        return word_cloud_data

# Initialize analyzer
analyzer = IndianLanguageAnalyzer()

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_text():
    """API endpoint to analyze text with advanced NLP features"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        language = data.get('language', 'auto').lower()
        top_n = int(data.get('top_n', 10))
        remove_stops = data.get('remove_stopwords', True)
        apply_stemming = data.get('apply_stemming', False)

        if not text:
            return jsonify({'error': 'No text provided'}), 400

        # Auto-detect language if set to 'auto'
        detected_language = None
        if language == 'auto':
            detected_language = analyzer.detect_language(text)
            language = detected_language

        # Get analysis results with NLP processing
        top_words = analyzer.get_top_words(text, language, top_n, remove_stops, apply_stemming)
        statistics = analyzer.get_statistics(text, language, apply_stemming)
        sentiment = analyzer.analyze_sentiment(text, language)
        entities = analyzer.extract_entities(text, language)

        # Get word cloud data
        word_cloud = analyzer.get_word_cloud_data(text, language, remove_stops, max_words=50)

        # Format response
        result = {
            'top_words': [{'word': word, 'frequency': freq} for word, freq in top_words],
            'statistics': statistics,
            'sentiment': sentiment,
            'entities': entities,
            'language': language,
            'detected_language': detected_language,
            'word_cloud': word_cloud,
            'nlp_features': {
                'stopword_removal': remove_stops,
                'stemming': apply_stemming,
                'library': 'NLTK + Custom'
            }
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'Indian Language NLP Analyzer'})

if __name__ == '__main__':
    print("🚀 Starting Language NLP Analyzer...")
    print("📊 Supported languages: English, Gujarati, Hindi")
    print("✨ Features: Sentiment Analysis, Key Terms Detection, Text Statistics")
    print("🧠 NLP Libraries: NLTK (Stemming, Tokenization, Stop Word Removal)")
    print("🌐 Server running on http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
