# import required libraries
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from flask import Flask, jsonify
import math
import re

from flask import Flask, render_template, request, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask import Flask, render_template, request
import logging



#gathering data in list so that TF-IDF can be applied

# data is file on which TF-IDF is applied,it has question name and question text
data=[]
# Q_name is list of question name
Q_name=[]
# Q_link is list of question link
Q_link=[]
# Q_difficulty is list of question difficulty
Q_difficulty=[]
# i is counter in loop 
i=0
# extracting data
with open("web scraping/question_name.txt", 'r', encoding='utf-8') as f:
   for line in f:
      i+=1
      text=line.strip()
      extracted_question_name=text.split('.',1)[-1]
      Q_name.append(extracted_question_name)      
      extracted_question_name=extracted_question_name.replace('-', ' ')     

      folder_path = f"web scraping/Question_data/{i}"
      file_path = os.path.join(folder_path, f"{i}.txt")
      with open(file_path, 'r',encoding='latin-1') as file:
         extracted_question_text = file.read()
         index = extracted_question_text.find("Example")
         extracted_question_text=extracted_question_text[:index]
         extracted_question_text=extracted_question_text.replace('-', ' ')
      data.append(extracted_question_name.lower()+" "+extracted_question_name.lower()+" "+extracted_question_name.lower()+" "+extracted_question_name.lower()+" "+extracted_question_text.lower())

with open("web scraping/question_index_with_link.txt", 'r', encoding='utf-8') as f:
   for line in f:
      text=line.strip()
      extracted_question_link=text.split('.',1)[-1]
      Q_link.append(extracted_question_link)

with open("web scraping/question_difficulty.txt", 'r', encoding='utf-8') as f:
   for line in f:
      Q_difficulty.append(line.strip())      

# applying TF-IDF on data
# Initialize the TfidfVectorizer
vectorizer = TfidfVectorizer()


vectorizer.fit(data)


tfidf_data = vectorizer.transform(data)
tfidf_matrix_=tfidf_data.toarray()
tfidf_matrix=np.array(tfidf_matrix_)



def get_similar_documents(query, top_k=20):
    print(query)
    query_vector = vectorizer.transform([query.lower()])
    similarity_scores = cosine_similarity(tfidf_matrix, query_vector)
    sorted_indices = similarity_scores.argsort(axis=0)[::-1].squeeze()

    similar_documents = []
    j = 0
    for i in sorted_indices:
        if similarity_scores[i] >= 0.001:
            similar_documents.append({
                "Q_name": Q_name[i],
                "similarity_score": similarity_scores[i],
                "Q_link": Q_link[i],
                "Q_difficulty": Q_difficulty[i]
            })
            j += 1
        if j >= top_k:
            break

    return similar_documents      






app=Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'

class SearchForm(FlaskForm):
    search = StringField('Enter your search term')
    submit = SubmitField('Search')

@app.route("/<query>")
def return_links(query):
    serialized_matrix = tfidf_matrix.tolist()

    # Call get_similar_documents with the serialized matrix
    result = get_similar_documents(query)

    # Return the result as a JSON response
    return jsonify(result)



@app.route('/',methods=['GET', 'POST'])
def home():
   form = SearchForm()
   query = form.search.data
   print(query)
   results = []
   if form.validate_on_submit():
      results = get_similar_documents(query)
   return render_template('index.html',form=form,results=results)

