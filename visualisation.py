# import lib for visualisation
import streamlit as st
import numpy as np
import pandas as pd  # For data handling
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import seaborn as sns


def tsnescatterplot(model, word, list_names):
    f1 = plt.figure()
    """ Plot in seaborn the results from the t-SNE dimensionality reduction algorithm of the vectors of a query word,
    its list of most similar words, and a list of words.
    """
    arrays = np.empty((0, 300), dtype='f')
    word_labels = [word]
    color_list = ['grey']
    # adds the vector of the query word
    arrays = np.append(arrays, model.wv.__getitem__([word]), axis=0)
    # gets list of most similar words
    close_words = model.wv.most_similar([word])
    # adds the vector for each of the closest words to the array
    for wrd_score in close_words:
        wrd_vector = model.wv.__getitem__([wrd_score[0]])
        word_labels.append(wrd_score[0])
        color_list.append('green')
        arrays = np.append(arrays, wrd_vector, axis=0)
    # adds the vector for each of the words from list_names to the array
    for wrd in list_names:
        wrd_vector = model.wv.__getitem__([wrd])
        word_labels.append(wrd)
        color_list.append('red')
        arrays = np.append(arrays, wrd_vector, axis=0)

    # Reduces the dimensionality from 300 to 21 dimensions with PCA
    reduc = PCA(n_components=21).fit_transform(arrays)

    # Finds t-SNE coordinates for 2 dimensions
    np.set_printoptions(suppress=True)
    Y = TSNE(n_components=2, random_state=0, perplexity=15).fit_transform(reduc)
    # Sets everything up to plot
    df = pd.DataFrame({'x': [x for x in Y[:, 0]],
                       'y': [y for y in Y[:, 1]],
                       'words': word_labels,
                       'color': color_list})
    fig, _ = plt.subplots()
    fig.set_size_inches(8, 4)

    # Basic plot
    p1 = sns.regplot(data=df,
                     x="x",
                     y="y",
                     fit_reg=False,
                     marker="o",
                     scatter_kws={'s': 40,
                                  'facecolors': df['color']
                                  }
                     )
    # Adds annotations one by one with a loop
    for line in range(0, df.shape[0]):
        p1.text(df["x"][line],
                df['y'][line],
                '  ' + df["words"][line].title(),
                horizontalalignment='left',
                verticalalignment='bottom', size='small',
                color=df['color'][line],
                weight='normal'
                ).set_size(12)

    #plt.xlim(Y[:, 0].min() -20, Y[:, 0].max() + 20)
    #plt.ylim(Y[:, 1].min() - 20, Y[:, 1].max() + 20)
    #plt.grid(False)
    plt.axis('off')


    st.pyplot(fig)

def wordcloud(text_wc):

    f2 = plt.figure()
    # Create and generate a word cloud image:
    stopwords = set(STOPWORDS)
    fin_stopwords = ["Frau","bzw"]
    for x in range(len(fin_stopwords)):
        stopwords.add(fin_stopwords[x])

    wordcloud = WordCloud(background_color='#0E1117', width=1600, height=800, stopwords=stopwords)
    wordcloud = wordcloud.generate(text_wc)

    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=6)

    st.pyplot(f2)
