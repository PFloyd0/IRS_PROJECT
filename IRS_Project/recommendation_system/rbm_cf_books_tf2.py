import os

import tensorflow as tf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pymysql
pymysql.install_as_MySQLdb()
from sqlalchemy import create_engine

# def read_table(cur, sql_order):  # sql_order is a string
#     try:
#         cur.execute(sql_order)  # 多少条记录
#         data = cur.fetchall()
#         frame = pd.DataFrame(list(data))
#     except:
#         frame = pd.DataFrame()
#     return frame
#
# con = pymysql.connect(host='127.0.0.1', user='root', passwd='19990520', db='Book', port=3306)  # 连接
# cur = con.cursor()
# select_rating_sql = '''Select * from Bookrating'''
# ratings_df = read_table(cur, select_rating_sql)
# con.commit()
# cur.close()
def load_data():
    engine = create_engine("mysql://root:19990520@127.0.0.1/Book", pool_size=5,echo_pool=True)

    conn = engine.connect()

    ratings_df = pd.read_sql_table("bookrating", conn)
    ratings_df = ratings_df.drop_duplicates(subset=['User_Id', 'Name', 'Rating'], keep='first')
    books_df = pd.read_sql_table("books", conn)
    books_df = books_df.loc[:, ['Name', 'Id']]
    books_df = books_df.drop_duplicates(subset='Name', keep='last')

    user_rating_df = ratings_df.pivot_table(index='User_Id', columns='Name', values='Rating')
    return books_df, ratings_df, user_rating_df



# Phase 1: Input Processing
def draw_sample_h0(v0, W, hb):  # h0
    h0_prob = tf.nn.sigmoid(tf.matmul(v0, W) + hb)
    return tf.nn.relu(tf.sign(h0_prob - tf.random.uniform(tf.shape(h0_prob))))  # drawing a sample from the distribution


# Phase 2: Reconstruction
def draw_sample_v1(h0, W, vb):  # v1
    v1_prob = tf.nn.sigmoid(tf.matmul(h0, tf.transpose(W)) + vb)
    return tf.nn.relu(
        tf.sign(v1_prob - tf.random.uniform(tf.shape(v1_prob))))  # sampling from visible units distribution


def calculate_h1(v1, W, hb):  # h1
    return tf.nn.sigmoid(tf.matmul(v1, W) + hb)  # correspondent hidden units


# Calculate Contrastive Divergence
def calculate_CD(v0, h0, v1, h1):  # CD
    w_pos_grad = tf.matmul(tf.transpose(v0), h0)
    w_neg_grad = tf.matmul(tf.transpose(v1), h1)
    # Calculate the Contrastive Divergence to maximize
    return (w_pos_grad - w_neg_grad) / tf.cast(tf.shape(v0)[0], dtype=tf.float32)


# Calculate reconstruction error
def calculate_error_sum(v0, v1):  # err_sum
    err = v0 - v1
    return tf.reduce_mean(err * err)


def generate_path():
    root_path = os.path.abspath(os.path.dirname(__file__)).split('IRS_Project')[0]
    root_path = os.path.join(root_path, "IRS_Project", "recommendation_system")
    prv_w_path = os.path.join(root_path, "prv_w.npy")
    prv_hb_path = os.path.join(root_path, "prv_hb.npy")
    prv_vb_path = os.path.join(root_path, "prv_vb.npy")
    return prv_w_path, prv_hb_path, prv_vb_path


def train_model():
    """Variable initialisations"""
    (_, _, user_rating_df) = load_data()
    norm_user_rating_df = user_rating_df.fillna(0) / 5.0
    trX = norm_user_rating_df.values
    trX = tf.cast(trX, dtype=tf.float32)

    hiddenUnits = 20
    visibleUnits = len(user_rating_df.columns)
    alpha = 1.0

    # Current weight
    cur_w = np.zeros([visibleUnits, hiddenUnits], np.float32)
    # Current visible unit biases
    cur_vb = np.zeros([visibleUnits], np.float32)
    # Current hidden unit biases
    cur_hb = np.zeros([hiddenUnits], np.float32)
    # Previous weight
    prv_w = np.zeros([visibleUnits, hiddenUnits], np.float32)
    # Previous visible unit biases
    prv_vb = np.zeros([visibleUnits], np.float32)
    # Previous hidden unit biases
    prv_hb = np.zeros([hiddenUnits], np.float32)

    epochs = 15
    batchsize = 100
    errors = []
    for i in range(epochs):
        for start, end in zip(range(0, len(trX), batchsize), range(batchsize, len(trX), batchsize)):
            batch = trX[start:end]
            v0 = batch
            h0 = draw_sample_h0(v0, cur_w, cur_hb)
            v1 = draw_sample_v1(h0, cur_w, cur_vb)
            h1 = calculate_h1(v1, cur_w, cur_hb)
            CD = calculate_CD(v0, h0, v1, h1)
            cur_w = prv_w + alpha * CD
            cur_vb = prv_vb + alpha * tf.reduce_mean(v0 - v1, 0)
            cur_hb = prv_hb + alpha * tf.reduce_mean(h0 - h1, 0)
            prv_w = cur_w
            prv_vb = cur_vb
            prv_hb = cur_hb
        errors.append(calculate_error_sum(trX, draw_sample_v1(draw_sample_h0(trX, cur_w, cur_hb), cur_w, cur_vb)))
        print(errors[-1])
    plt.plot(errors)
    plt.ylabel('Error')
    plt.xlabel('Epoch')
    plt.show()
    prv_w_path, prv_hb_path, prv_vb_path = generate_path()
    np.save(prv_w_path, prv_w.numpy())
    np.save(prv_hb_path, prv_hb.numpy())
    np.save(prv_vb_path, prv_vb.numpy())
    return 0


def do_recommendation(mock_user_id, top_n=20):
    # load model
    prv_w_path, prv_hb_path, prv_vb_path = generate_path()
    prv_w = np.load(prv_w_path)
    prv_hb = np.load(prv_hb_path)
    prv_vb = np.load(prv_vb_path)

    #load data
    (books_df, ratings_df, user_rating_df) = load_data()

    # Selecting the input user
    norm_user_rating_df = user_rating_df.fillna(0) / 5.0
    trX = norm_user_rating_df.values
    trX = tf.cast(trX, dtype=tf.float32)
    inputUser = tf.reshape(trX[mock_user_id - 1], [1, -1])

    # Feeding in the user and reconstructing the input
    feed = tf.nn.sigmoid(tf.matmul(inputUser, prv_w) + prv_hb)
    rec = tf.nn.sigmoid(tf.matmul(feed, tf.transpose(prv_w)) + prv_vb)


    scored_books_df_mock = books_df[books_df['Id'].isin(user_rating_df.columns)]
    scored_books_df_mock = scored_books_df_mock.assign(RecommendationScore=rec[0].numpy())

    books_df_mock = ratings_df[ratings_df['User_Id'] == mock_user_id]
    # Merging books_df with ratings_df by Id and Name
    merged_df_mock = scored_books_df_mock.merge(books_df_mock, left_on='Id', right_on='Name', how='outer')
    df_filter = merged_df_mock['User_Id'].isin(books_df_mock['Name'])
    merged_df_mock = merged_df_mock[~ df_filter]
    result = merged_df_mock.sort_values(["RecommendationScore"], ascending=False).head(top_n)
    result = result.loc[:, ['Name_x', 'Id_x', 'RecommendationScore']]
    return result
# train_model()
a = do_recommendation(2)['Id_x']

print(a.values)
