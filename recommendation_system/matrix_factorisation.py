from sqlalchemy import create_engine
from sklearn.utils import shuffle
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Embedding, Dot, Add, Flatten
from tensorflow.keras.regularizers import l2
from tensorflow.keras.optimizers import SGD, Adam
from keras.models import load_model
import pymysql
pymysql.install_as_MySQLdb()
import os
import pandas as pd
import numpy as np


def load_data():
    engine = create_engine("mysql://root:19980420@127.0.0.1/Book", pool_size=5,echo_pool=True)

    conn = engine.connect()

    ratings_df = pd.read_sql_table("bookrating", conn)
    ratings_df = ratings_df.drop_duplicates(subset=['User_Id', 'Name', 'Rating'], keep='first')
    books_df = pd.read_sql_table("books", conn)
    books_df = books_df.loc[:, ['Name', 'Id']]
    books_df = books_df.drop_duplicates(subset='Name', keep='last')

    user_rating_df = ratings_df.pivot_table(index='User_Id', columns='Name', values='Rating')
    return books_df, ratings_df, user_rating_df


def train_model(K=10, epochs=25, reg=0.0005):
    (_, ratings_df, _) = load_data()

    N = ratings_df['User_Id'].max() + 1
    M = ratings_df['Name'].max() + 1
    trans = shuffle(ratings_df)
    cutoff = int(0.8 * len(trans))
    df_train = trans.iloc[:cutoff]
    df_test = trans.iloc[cutoff:]

    mu = df_train['Rating'].mean()

    # keras model

    # 输入层定义，有两个输入，分别是用户id和商品id
    u = Input(shape=(1,))
    m = Input(shape=(1,))

    # Embedding层负责把输入的单个数字转化为更深维度的数组
    u_embedding = Embedding(N, K, embeddings_regularizer=l2(reg))(u)  # (None, 1, K)
    m_embedding = Embedding(M, K, embeddings_regularizer=l2(reg))(m)  # (None, 1, K)

    u_bias = Embedding(N, 1, embeddings_regularizer=l2(reg))(u)  # (None, 1, 1)
    m_bias = Embedding(M, 1, embeddings_regularizer=l2(reg))(m)  # (None, 1, 1)
    x = Dot(axes=2)([u_embedding, m_embedding])  # (None, 1, 1)

    x = Add()([x, u_bias, m_bias])  # (None, 1, 1)
    x = Flatten()(x)  # (None, 1)

    model = Model(inputs=[u, m], outputs=x)
    model.compile(
        loss='mse',
        optimizer='adam',  # SGD(lr=0.01, momentum=0.9),'adam'
        metrics=['mse'])

    r = model.fit(
        x=[df_train['User_Id'], df_train['Name']],
        y=df_train["Rating"] - mu,
        epochs=epochs,
        batch_size=32,
        validation_data=(
            [df_test['User_Id'], df_test['Name']],
            df_test['Rating'] - mu
        )
    )
    root_path = os.path.abspath(os.path.dirname(__file__)).split('IRS_Project')[0]
    root_path = os.path.join(root_path, "IRS_Project", "recommendation_system")
    model_path = os.path.join(root_path, "MF_model.h5")
    model.save(model_path)


def do_recommendation(user_id, book_id):
    root_path = os.path.abspath(os.path.dirname(__file__)).split('IRS_Project')[0]
    root_path = os.path.join(root_path, "IRS_Project", "recommendation_system")
    model_path = os.path.join(root_path, "MF_model.h5")
    model = load_model(model_path)
    re = float(model.predict([np.expand_dims(user_id, 0), np.expand_dims(book_id, 0)]))
    return re
