import re
import demoji
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Download NLTK resources (if not already downloaded)
nltk.download('punkt')
nltk.download('stopwords')

stop_words = set(stopwords.words('english')) 
stop_words.add('rt')

def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def remove_html_character_codes(text):
    clean = re.compile('&.*;')
    return re.sub(clean, '', text)

def remove_emojis(text):
   return demoji.replace(text, '')

def remove_urls(text):
    clean = re.compile('https?://\S+|www\.\S+')
    return re.sub(clean, '', text)

def remove_punctuation(text):
    clean = re.compile('[^\w\s]')
    return re.sub(clean, '', text)

def make_lower_case(text):
    words = text.split() 
    lower_words = [word.lower() for word in words if word.isalpha()]
    return ' '.join(lower_words)
    
def remove_stop_words(text): 
    words = text.split() 
    filtered_words = [word for word in words if word not in stop_words] 
    return ' '.join(filtered_words)

def tokenize_text(text):
    return word_tokenize(text)

def preprocess_text_pipeline_twitter(text):
    text = remove_html_tags(text)
    text = remove_html_character_codes(text)
    text = remove_emojis(text)
    text = remove_urls(text)
    text = remove_punctuation(text)
    text = make_lower_case(text)
    text = remove_stop_words(text)
    text = tokenize_text(text)
    return text


def preprocess_data(data, source):
    if source == "twitter":
        data['preprocess_text'] = data['text'].apply(preprocess_text_pipeline_twitter)
        return data
  
