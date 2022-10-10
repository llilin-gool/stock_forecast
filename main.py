import nltk
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx


def sentence_similarity(sent1, sent2):
    sent1 = [w.lower() for w in sent1]
    sent2 = [w.lower() for w in sent2]

    all_words = list(set(sent1 + sent2))
    vector1 = [0] * len(all_words)
    vector2 = [0] * len(all_words)

    for w in sent1:
        vector1[all_words.index(w)] += 1
    for w in sent2:
        vector2[all_words.index(w)] += 1
    print(1 - cosine_distance(vector1, vector2))
    return 1 - cosine_distance(vector1, vector2)


def build_similarity_matrix(sentences):
    similarity_matrix = np.zeros((len(sentences),len(sentences)),dtype=float)
    print(similarity_matrix)
    for idx1 in range(len(sentences)):
        for idx2 in range(len(sentences)):
            if idx1 == idx2:
                continue
            similarity_matrix[idx1][idx2] = sentence_similarity(sentences[idx1], sentences[idx2])
    return similarity_matrix


def generate_summary(file_name, top_n=5):
    summarize_text = []
    file = open(file_name, "r")
    filedata = file.readlines()
    article = filedata[0].split(". ")
    sentences = []
    for sentence in article:
        sentences.append(sentence.split(" "))
    sentence_similarity_martix = build_similarity_matrix(sentences)
    sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_martix)
    print(sentence_similarity_graph.edges(data=True))
    scores = nx.pagerank(sentence_similarity_graph)
    ranked_sentence = sorted(((scores[i], s) for i, s in enumerate(sentences)), reverse=True)
    for i in range(top_n):
        summarize_text.append(" ".join(ranked_sentence[i][1]))
    print("Summarize: \n", " ".join(summarize_text))


generate_summary("sample.txt", 2)
G = nx.DiGraph(nx.path_graph(4))
print(G)
