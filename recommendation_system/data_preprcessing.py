import pandas as pd
import pymysql
import os

pd.options.display.width = 0
# read ratings files
ratingdf = []
os.chdir('../data/')
for filename in os.listdir():
    if filename.startswith('user_rating'):
        ratingdf.append(
            pd.read_csv('user_rating_0_to_1000.csv', sep=',', header=0, engine='python', encoding='latin-1'))
ratings_df = pd.concat(ratingdf)
# read books files
books_df = pd.read_csv('book1-100k.csv', sep=',', header=0, engine='python', encoding='latin-1')
books_df = books_df.loc[:, ['Name', 'Id']]
books_df = books_df.drop_duplicates(subset='Name', keep='last')
# build map dict
name_dict = books_df.set_index('Name')
name_dict = name_dict.to_dict()
# map name and ratings
ratings_df['Name'] = ratings_df['Name'].map(name_dict['Id'])
rat_dict = {'it was amazing': 5, 'really liked it': 4,
            'liked it': 3, 'did not like it': 1,
            "This user doesn't have any rating": None, 'it was ok': 2}
ratings_df['Rating'] = ratings_df['Rating'].map(rat_dict)
# drop NaN data
ratings_df = ratings_df.dropna()

user_rating_df = ratings_df.pivot_table(index='ID', columns='Name', values='Rating')
norm_user_rating_df = user_rating_df.fillna(0) / 5.0