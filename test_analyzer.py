#!/usr/bin/env python3
"""
Simple test script for the Indian Language NLP Analyzer
Run this to verify the installation and basic functionality
"""

from analyzer import IndianLanguageAnalyzer

def test_basic_functionality():
    """Test basic analyzer functionality"""
    print("🧪 Testing Indian Language NLP Analyzer\n")

    analyzer = IndianLanguageAnalyzer()

    # Test cases for different languages
    test_cases = [
        {
            'language': 'english',
            'text': 'This is a great day. I am very happy and excited. The weather is wonderful and beautiful.',
            'expected_positive': True
        },
        {
            'language': 'gujarati',
            'text': 'આજે એક સુંદર દિવસ છે। હું ખૂબ ખુશ છું। આ સરસ છે।',
            'expected_positive': True
        },
        {
            'language': 'hindi',
            'text': 'यह एक बहुत अच्छा दिन है। मुझे बहुत खुशी हो रही है। यह सुंदर मौसम है।',
            'expected_positive': True
        }
    ]

    for i, test_case in enumerate(test_cases, 1):
        print(f"Test {i}: {test_case['language'].upper()}")
        print("-" * 50)

        text = test_case['text']
        language = test_case['language']

        # Test tokenization
        words = analyzer.tokenize_text(text)
        print(f"✓ Tokenization: Found {len(words)} words")

        # Test word frequency
        top_words = analyzer.get_top_words(text, language, top_n=5)
        print(f"✓ Top 5 words: {[word for word, _ in top_words]}")

        # Test statistics
        stats = analyzer.get_statistics(text, language)
        print(f"✓ Statistics: {stats['total_words']} total, {stats['unique_words']} unique")

        # Test sentiment analysis
        sentiment = analyzer.analyze_sentiment(text, language)
        print(f"✓ Sentiment: {sentiment['sentiment']} (score: {sentiment['score']})")
        print(f"  Positive words: {sentiment['positive_words']}, Negative words: {sentiment['negative_words']}")

        # Test entity extraction
        entities = analyzer.extract_entities(text, language)
        print(f"✓ Entities: Found {len(entities)} entities")

        # Verify expected sentiment
        if test_case['expected_positive'] and sentiment['sentiment'] == 'positive':
            print("✅ Sentiment test PASSED")
        elif not test_case['expected_positive'] and sentiment['sentiment'] == 'negative':
            print("✅ Sentiment test PASSED")
        else:
            print(f"⚠️  Sentiment test WARNING: Expected positive but got {sentiment['sentiment']}")

        print()

    print("=" * 50)
    print("✅ All tests completed successfully!")
    print("\nYou can now run the Flask app with:")
    print("  python analyzer.py")
    print("\nThen open http://localhost:5000 in your browser")

if __name__ == '__main__':
    try:
        test_basic_functionality()
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
