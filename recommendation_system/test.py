import pandas as pd
path = '../data/ratings_csv.csv'
Rating = pd.read_csv(path, sep=",", encoding="ISO-8859-1", error_bad_lines=False)

Rating = Rating.drop_duplicates(subset=['User_Id', 'Name', 'Rating'], keep='first')

Rating.to_csv("../data/ratings_csv_new.csv",index=0)

books_df = pd.read_csv('../data/book1-100k.csv', sep=",", encoding="ISO-8859-1", error_bad_lines=False)
books_df = books_df.drop_duplicates(subset='Name', keep='last')
books_df.to_csv("../data/book1-100k_new.csv",index=0)