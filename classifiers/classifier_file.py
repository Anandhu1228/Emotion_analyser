import sys
import os
import joblib
import string
import spacy
from nltk.corpus import stopwords

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  

nlp = spacy.load("en_core_web_sm")

stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    text = "".join([char for char in text if char not in string.punctuation])
    text = text.lower()

    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if token.text not in stop_words and not token.is_space]
    
    return " ".join(tokens)

def load_trained_model():
    base_dir = os.path.dirname(__file__)
    model_path = os.path.join(base_dir, 'Emotion_analysis.joblib')
    vectorizer_path = os.path.join(base_dir, 'CountVectorizer_Emotion_analysis.joblib')
    model = joblib.load(model_path)
    count_vec = joblib.load(vectorizer_path)
    
    return model, count_vec

def main():
    if len(sys.argv) < 2:
        sys.stderr.write("Error: Please provide a message to classify.\n")
        sys.exit(1)

    message_content = sys.argv[1].strip()
    preprocessed_message = preprocess_text(message_content)
    model, count_vec = load_trained_model()
    message_vectorized = count_vec.transform([preprocessed_message])
    predicted_emotion = model.predict(message_vectorized)[0]
    sys.stdout.write(predicted_emotion)

if __name__ == "__main__":
    main()

