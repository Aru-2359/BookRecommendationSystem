# -*- coding: utf-8 -*-
"""model.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1AtPGtyUpDV88_12JY99tsCFm382JmaSE
"""

import numpy as np
import pandas as pd

books = pd.read_csv('Books.csv')
users = pd.read_csv('Users.csv')
ratings = pd.read_csv('Ratings.csv')

books.info()

users.info()

ratings.info()

books.head(5)

ratings.head(5)

users.head(5)

books.isnull().sum()

ratings.isnull().sum()

users.isnull().sum()

import matplotlib.pyplot as plt
import seaborn as sns

top_books = ratings['ISBN'].value_counts().head(50)
top_books

top_books_df = pd.DataFrame({'ISBN': top_books.index, 'ratings_count': top_books.values})
top_books_merged = top_books_df.merge(books, on='ISBN', how='left')

plt.figure(figsize=(12, 10))
sns.barplot(x='ratings_count', y='Book-Title', data=top_books_merged)
plt.title('Top 50 Books with Most Ratings')
plt.xlabel('Number of Ratings')
plt.ylabel('Book Title')
plt.show()

ratings_with_book_name = ratings.merge(books,on='ISBN')
ratings_with_book_name

num_rating_df = ratings_with_book_name.groupby('Book-Title').count()['Book-Rating'].reset_index()
num_rating_df.rename(columns={'Book-Rating':'num_ratings'},inplace=True)
num_rating_df

# Convert 'Book-Rating' to numeric, handling errors
ratings_with_book_name['Book-Rating'] = pd.to_numeric(ratings_with_book_name['Book-Rating'], errors='coerce')

# Calculate average rating, ignoring non-numeric values
avg_rating_df = ratings_with_book_name.groupby('Book-Title')['Book-Rating'].mean().reset_index()
avg_rating_df.rename(columns={'Book-Rating':'avg_rating'},inplace=True)
avg_rating_df

popular_df = num_rating_df.merge(avg_rating_df,on='Book-Title')
popular_df

ratings_with_book_name

x = ratings_with_book_name.groupby('User-ID').count()['Book-Rating'] > 200
users_having_morethan_200_ratings = x[x].index

users_having_morethan_200_ratings

filtered_ratings = ratings_with_book_name[ratings_with_book_name['User-ID'].isin(users_having_morethan_200_ratings)]

filtered_ratings

y = filtered_ratings.groupby('Book-Title').count()['Book-Rating'] >= 50
books_having_morethan_50_ratings = y[y].index

books_having_morethan_50_ratings

final_ratings = filtered_ratings[filtered_ratings['Book-Title'].isin(books_having_morethan_50_ratings)]

final_ratings

pivot = final_ratings.pivot_table(index = 'Book-Title', columns = 'User-ID', values = 'Book-Rating')

pivot

pivot.fillna(0, inplace = True)

pivot

from sklearn.metrics.pairwise import cosine_similarity

cosine_similarity(pivot)

similarity_scores = cosine_similarity(pivot)

similarity_scores.shape

np.where(pivot.index == 'You Belong To Me')[0][0]

similarity_scores[0]

sorted(list(enumerate(similarity_scores[0])),key = lambda x:x[1], reverse = True)[1:11]

def recommend(book_name):
  if book_name in pivot.index:
    index = np.where(pivot.index == book_name)[0][0]
    similar_books = sorted(list(enumerate(similarity_scores[index])),key = lambda x:x[1], reverse = True)[1:11]
    for i in similar_books:
      print(pivot.index[i[0]])
  else:
    print(f"Book '{book_name}' not found in the dataset.")

recommend('You Belong To Me')

recommend('The Notebook')

recommend('The Fault in Our Stars')

recommend('The Giving Tree')

recommend('Second Nature')

recommend('The Da Vinci Code')

import pickle

pickle.dump(popular_df,open('popular.pkl','wb'))
