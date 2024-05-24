#!/usr/bin/env python
# coding: utf-8

# In[111]:


import numpy as pd
import pandas as pd
pd.options.mode.copy_on_write = True



# In[2]:


movies = pd.read_csv('tmdb_5000_movies.csv')
credits = pd.read_csv('tmdb_5000_credits.csv')


# In[4]:


movies.head(1)


# In[9]:


credits.head(1)


# In[13]:


movies = movies.merge(credits,on='title')


# In[14]:


movies.head(1)


# In[20]:


# genres
# id
# keywords
# title
# overview
# cast
# crew

movies = movies[['movie_id','title','overview','genres','keywords','cast','crew']]


# In[18]:


movies.info()


# In[21]:


movies.head()


# In[23]:


movies.isnull().sum()


# In[29]:


movies.dropna(inplace=True)


# In[30]:


movies.duplicated().sum()


# In[31]:


movies.iloc[0].genres


# In[ ]:


# '[{"id": 28, "name": "Action"}, {"id": 12, "name": "Adventure"}, {"id": 14, "name": "Fantasy"}, {"id": 878, "name": "Science Fiction"}]'
# ['Action','Adventure','Fantasy','SciFi']


# In[59]:


def convert(obj):
    L= []
    for i in ast.literal_eval(obj):
     L.append(i['name'])
     return L


# In[42]:


movies['genres'] = movies['genres'].apply(convert)


# In[44]:


movies.head()


# In[46]:


movies['keywords']= movies['keywords'].apply(convert)


# In[58]:


def convert3(obj):
    L = []
    counter = 0
    for i in ast.literal_eval(obj):
        if counter != 3:
            L.append(i['name'])
            counter += 1
        else:
            break
    return L
  
        


# In[61]:


movies['cast'] = movies['cast'].apply(convert3)


# In[62]:


movies.head()


# In[63]:


movies['crew'][0]


# In[66]:


def fetch_director(obj):
    L = []
    for i in ast.literal_eval(obj):
        if i['job'] == 'Director':
            L.append(i['name'])
            break
    return L


# In[68]:


movies['crew'] = movies['crew'].apply(fetch_director)


# In[69]:


movies.head()


# In[70]:


movies['overview'][0]


# In[72]:


movies['overview'] = movies['overview'].apply(lambda x:x.split())


# In[73]:


movies.head()


# In[80]:


movies['genres'] = movies['genres'].apply(lambda x: [i.replace(" ", "") for i in x] if x is not None else x)
movies['keywords'] = movies['keywords'].apply(lambda x: [i.replace(" ", "") for i in x] if x is not None else x)
movies['cast'] = movies['cast'].apply(lambda x: [i.replace(" ", "") for i in x] if x is not None else x)
movies['crew'] = movies['crew'].apply(lambda x: [i.replace(" ", "") for i in x] if x is not None else x)


# In[81]:


movies.head()


# In[82]:


movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']


# In[83]:


movies.head()


# In[84]:


new_df = movies[['movie_id','title','tags']]


# In[95]:


new_df['tags'] = new_df['tags'].apply(lambda x: " ".join(x) if isinstance(x, list) else x)


# In[96]:


new_df.head()


# In[97]:


new_df['tags'][0]


# In[99]:


new_df['tags'] = new_df['tags'].apply(lambda x: x.lower() if isinstance(x, str) else x)


# In[100]:


new_df.head()


# In[139]:


import nltk


# In[143]:


from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()


# In[151]:


def stem(text):
    y = []
    for i in text.split():
        y.append(ps.stem(i))
        return" ".join(y)




# In[158]:


new_df['tags'] = new_df['tags'].apply(stem)


# In[101]:


new_df['tags'][0]


# In[102]:


new_df['tags'][1]


# In[115]:


from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=5000, stop_words='english')


# In[118]:


new_df['tags'] = new_df['tags'].fillna('')


# In[119]:


cv = CountVectorizer(max_features=5000, stop_words='english')


# In[128]:


cv.fit(new_df['tags'])


# In[129]:


vectors = cv.transform(new_df['tags'])


# In[122]:


array_shape = X.shape


# In[123]:


print(array_shape)


# In[125]:


# Transform the 'tags' column into a document-term matrix
X = cv.transform(new_df['tags'])


# In[132]:


# Convert the sparse matrix to a dense NumPy array
vector_array = X.toarray()

# Display the vector array
print(vector_array)



# In[134]:


# Access the first row of the vector array
first_row_array = vector_array[0]

# Display the first row as an array
print(first_row_array)


# In[159]:


cv.get_feature_names_out()


# In[150]:


ps.stem('dance')


# In[160]:


text = "in the 22nd century, a paraplegic marine is dispatched to the moon pandora on a unique mission, but becomes torn between following orders and protecting an alien civilization. action cultureclash samworthington zoesaldana sigourneyweaver jamescameron"
stemmed_text = stem(text)
print(stemmed_text) 


# In[161]:


from sklearn.metrics.pairwise import cosine_similarity


# In[169]:


similarity= cosine_similarity(vectors)


# In[178]:


sorted(list(enumerate(similarity[0])),reverse=True,key=lambda x:x[1])[1:6] 


# In[193]:


def recommend(movie):
    movie_index = new_df[new_df['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x: x[1])[1:6]

    for i in movies_list:
        print(new_df.iloc[i[0]].title)
        
    


# In[194]:


recommend('Batman Begins')


# In[195]:


new_df.iloc[3608].title


# In[ ]:




