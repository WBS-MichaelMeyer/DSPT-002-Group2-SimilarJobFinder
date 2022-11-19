# import
import streamlit as st # for web app
import pandas as pd  # For data handling
# visualisation
import visualisation
import matplotlib.pyplot as plt


# import data
url = 'https://drive.google.com/file/d/16EGubjXaeDwTH7sc6FnuQj7EI9ZfRYNL/view?usp=sharing'
path = 'https://drive.google.com/uc?export=download&id='+url.split('/')[-2]
df = pd.read_csv(path, sep = '\t')


# APP Structure
# header
st.image("header.png")

title = st.text_input('Enter one search term', 'Data Science')
st.write('The current serach term is: ', title)


visualisation.test_plot()


#tsnescatterplot(w2v_model, 'Kaufmann', [i[0] for i in w2v_model.most_similar(negative=["Kaufmann"])])

# plot columns
col1, col2 = st.columns(2)

with col1:
   st.header("A cat")
   st.image("https://static.streamlit.io/examples/cat.jpg")

with col2:
   st.header("A dog")
   st.image("https://static.streamlit.io/examples/dog.jpg")


st.write(df)