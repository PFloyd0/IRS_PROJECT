from keras.models import load_model
import joblib
import pandas as pd
from keras.preprocessing.sequence import pad_sequences
from book_re import models
from recommendation_system import hybird
import os
from django.db.models import Min, Max
# WORD2VEC
W2V_SIZE = 300
W2V_WINDOW = 7
W2V_EPOCH = 32
W2V_MIN_COUNT = 10

# KERAS
SEQUENCE_LENGTH = 300
EPOCHS = 8
BATCH_SIZE = 1024

# SENTIMENT
POSITIVE = "POSITIVE"
NEGATIVE = "NEGATIVE"
NEUTRAL = "NEUTRAL"
SENTIMENT_THRESHOLDS = (0.4, 0.7)

# EXPORT
KERAS_MODEL = "model.h5"
WORD2VEC_MODEL = "model.w2v"
TOKENIZER_MODEL = "tokenizer.pkl"
ENCODER_MODEL = "encoder.pkl"


def decode_sentiment(score, include_neutral=True):
    if include_neutral:
        label = NEUTRAL
        if score <= SENTIMENT_THRESHOLDS[0]:
            label = NEGATIVE
        elif score >= SENTIMENT_THRESHOLDS[1]:
            label = POSITIVE

        return label
    else:
        return NEGATIVE if score < 0.5 else POSITIVE


def predict(text, include_neutral=True):
    root_path = os.path.abspath(os.path.dirname(__file__)).split('IRS_Project')[0]
    root_path = os.path.join(root_path, "IRS_Project", "SentimentParser")
    model_path = os.path.join(root_path, "model.h5")
    token_path = os.path.join(root_path, "tokenizer.pkl")
    model = load_model(model_path)
    tokenizer = joblib.load(token_path)
    # Tokenize text
    x_test = pad_sequences(tokenizer.texts_to_sequences([text]), maxlen=SEQUENCE_LENGTH)
    # Predict
    score = model.predict([x_test])[0]
    # Decode sentiment
    label = decode_sentiment(score, include_neutral=include_neutral)

    return label


def nameMatch(text, namelist):
    target = 0
    for bookname in namelist:
        if text == bookname:
            target = 1
    return target


def recomMatch(text):
    target = 0
    if "recommend" in text:
        target = 2
    return target


def doSearch(text,  user_id):
    try:
        re = models.Books.objects.filter(name__contains=text)
        print("this is a book name. just return this book")
        print(re)
        if len(re) != 0:
            str = "You may want these books: "
            for i in re:
                if len(str) < 100:
                    str += i.name+" "
                else:
                    break
            print(str)
            return str
    except:
        pass
    if recomMatch(text) == 1:
        book_re = hybird.do_recommendation(user_id)
        re = []
        for row in book_re.itertuples():
            re.append({'name': getattr(row, 'Name_x'), 'id': getattr(row, 'Id_x')})
        re = re[0]
        re = 'You may like this book: %s' % re
        print("a recommend request. just recom")
        return re
    else:
        if predict(text) == 'NEUTRAL':
            book_re = hybird.do_recommendation(user_id)
            re = []
            for row in book_re.itertuples():
                re.append({'name': getattr(row, 'Name_x'), 'id': getattr(row, 'Id_x')})
            re = re[0]["name"]
            re = 'You may like this book: %s' % re
            return re
        elif predict(text) == 'NEGATIVE':
            ra = models.Bookrating.objects.filter(user_id=user_id).aggregate(Min('rating'))
            re = models.Bookrating.objects.filter(rating=ra["rating__min"])[0]
            re = models.Books.objects.get(id=re.name)
            print(re)
            re = "Bad book, like %s" % re.name
            print(re)
            return re
        elif predict(text) == 'POSITIVE':
            ra = models.Bookrating.objects.filter(user_id=user_id).aggregate(Max('rating'))
            re = models.Bookrating.objects.filter(rating=ra["rating__max"])[0]
            re = models.Books.objects.get(id=re.name)
            print(re)
            re = "Good book, like %s" % re.name
            print(re)
            return re
    return




def do_chat(Input, user_id):
    # df = pd.read_csv('data/book100k-200k.csv')
    # namelist = df['Name']

    return doSearch(Input, user_id)
print(do_chat("a String", 1))