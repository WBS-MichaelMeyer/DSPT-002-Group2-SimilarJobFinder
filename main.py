# import app and date handling
import pandas as pd  # For data handling
import streamlit as st  # for web app
import numpy as np
# visualisation
import visualisation
from polyfuzz.models import TFIDF
from polyfuzz import PolyFuzz

#import model
from gensim.models import Word2Vec
w2v_model = Word2Vec.load("word2vec.model")
#w2v_model.init_sims(replace=True)
most_frequent = w2v_model.wv.index_to_key[:1000]

# data import
#url = 'https://drive.google.com/file/d/16EGubjXaeDwTH7sc6FnuQj7EI9ZfRYNL/view?usp=sharing'
#path = 'https://drive.google.com/uc?export=download&id='+url.split('/')[-2]
df = pd.read_csv("jobs.csv", sep = '\t')


# APP Structure
# header
st.image("header.png")
st.subheader("Input Keyword")

try:
    [title] = st.multiselect(
            'Please choose ONE search keyword',
            most_frequent,
            "Data_Science" )

    #title = st.text_input('', 'Kaufmann')
    st.write('The current search term is: ', [title][0])
    st.markdown("***")

    with st.spinner('Wait for it...'):

        st.subheader("Most similar vs dissimilar keywords")
        visualisation.tsnescatterplot(w2v_model, title, [i[0] for i in w2v_model.wv.most_similar(negative=[title][0])])
        most_similar = w2v_model.wv.most_similar(positive=[title][0], topn=50)
        st.markdown("***")

        st.subheader("Wordcloud")
        text_wc = ' '.join(np.concatenate(most_similar))
        visualisation.wordcloud(text_wc)
        st.markdown("***")

        # second similarity search
        to_list = [i[0] for i in most_similar]
        from_list = df['full_description'].values.tolist()

        tfidf = TFIDF(n_gram_range=(3, 3))
        model_polyfuzz = PolyFuzz(tfidf)
        model_polyfuzz.match(from_list, to_list)

        df_matches = model_polyfuzz.get_matches()
        df_matches = df_matches.sort_values(by=['Similarity'], ascending=False).head(50)
        df_matches = df_matches.join(df, lsuffix='_caller', rsuffix='_other')[['job_title', 'To', 'Similarity']]

        st.subheader("Similar Job postings")
        st.dataframe(df_matches)
except:
    pass
