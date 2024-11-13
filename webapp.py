import streamlit as st
import pandas as pd
import numpy as np
import re
from sklearn.neighbors import NearestNeighbors
import scipy.sparse
import pickle

@st.cache_data
def load_data():
    return pd.read_csv('Data/recipes_food_com_cleaned.csv')

@st.cache_resource
def load_neighbors():
    with open('models/nearest_neighbors_model.pkl', 'rb') as f:
        nearest_neighbors = pickle.load(f)
    return nearest_neighbors

@st.cache_resource
def load_matrix():
    tfidf_matrix = scipy.sparse.load_npz('models/tfidf_matrix_updated.npz')
    return tfidf_matrix

@st.cache_resource
def load_vectorizer():
    with open('models/tfidf_vectorizer_updated.pkl', 'rb') as f:
        vectorizer = pickle.load(f)
    return vectorizer

with st.spinner('Loading models...'):
    nearest_neighbors = load_neighbors()
    tfidf_matrix = load_matrix()
    vectorizer = load_vectorizer()

with st.spinner('Loading data...'):
    data = load_data()

@st.cache_data
def recommend(ingredients_list, top_n=5):
    user_vector = vectorizer.transform([ingredients_list])
    distances, indices = nearest_neighbors.kneighbors(user_vector, n_neighbors=top_n)
    recommender = data.iloc[indices[0]].copy()
    recommender['Similarity'] = 1 - distances[0]
    return recommender

st.title('Dishcovery')
ingredients_list = st.text_input("Which Ingredients Are You Using?")
st.write(f'Your Ingredients List is: {ingredients_list}')

# Display each recipe in an expander
if st.button('Get Recommendations', key = 'Recommendations'):
    with st.spinner('Recommending...'):
        recommendations = recommend(ingredients_list)
        for index, row in recommendations.iterrows():
            with st.expander(row['Name']):
                st.markdown(f"## {row['Name']}")
                st.write(f"**Similarity:** {row['Similarity']:.2f}")
                st.write("**Ingredients:**")
                st.write(row['Cleaned_Ingredients'])

                # Display nutrition
                st.write("**Nutrition**")
                st.write(f"**Calories:** {row['Calories']:.2f}")
                st.write(f"**Fat:** {row['FatContent']:.2f}g")
                st.write(f"**Saturated Fat:** {row['SaturatedFatContent']:.2f}g")
                st.write(f"**Cholesterol:** {row['CholesterolContent']:.2f}mg")
                st.write(f"**Sodium:** {row['SodiumContent']:.2f}mg")
                st.write(f"**Total Carbohydrates:** {row['CarbohydrateContent']:.2f}g")
                st.write(f"**Dietary Fiber:** {row['FiberContent']:.2f}g")
                st.write(f"**Sugars:** {row['FiberContent']:.2f}g")
                st.write(f"**Protein:** {row['ProteinContent']:.2f}g")
                
                # Parse instructions into separate steps
                instructions_list = row['Instructions'].split('", "')
                st.write("**Instructions:**")
                for i, step in enumerate(instructions_list, 1):
                    step = step.replace('"', '').replace('[', '').replace(']', '')
                    st.write(f"{i}. {step}")
                st.write("------")
