# -*- coding: utf-8 -*-

"""
Script to score sentences to get summary
"""

import nltk
from nltk.corpus import stopwords
import util
import re


def format_sentence(sentence):
    sentence = re.sub(r'\W+', '', sentence)
    return sentence


def scoreSentences(sen1, sen2):
    """
    Compares two sentences, find intersection and scores them
    :param sen1: (str) sentence
    :param sen2: (str) sentence
    :returns: score
    """
    # TODO: Better scoring algorithm
    # sen1 = format_sentence(sen1)
    # sen2 = format_sentence(sen2)
    s1 = set(sen1.lower().split())
    s2 = set(sen2.lower().split())
    score = 0
    if s1 and s2:
        avg = len(s1)+len(s2) / 2.0
        score = len(s1.intersection(s2)) / avg
    return score


def remove_stopwords(sentences):
    """
    Removes stopwords from the sentence
    :param sentences: (list) sentences
    :returns: cleaned sentences without any stopwords
    """
    sw = set(stopwords.words('english'))
    cleaned = []
    for sentence in sentences:
        words = util.getWords(sentence)
        sentence = ' '.join([c for c in words if c not in sw])
        cleaned.append(sentence)
    return cleaned


def sentenceGraph(sentences):
    """
    Creates all pair score graph of sentences
    :param sentences: (list) list of sentences
    :returns: graph containing of all pair of sentence scores
    """
    scoreGraph = []
    len_sen = len(sentences)
    for i in range(len_sen):
        weight = []
        for j in range(len_sen):
            sentenceScore = 0
            if i == j:
                continue
            else:
                sentenceScore = scoreSentences(sentences[i], sentences[j])
            weight.append(sentenceScore)
        scoreGraph.append(weight)

    return scoreGraph


def build(sentences, scoreGraph, orig_sentences):
    """
    Builds the content summary based on the graph
    :param sentences: (list) list of sentences
    :param scoreGraph: (list) 2 dimensional list-graph of scores
    :returns: Aggregate score of each sentence in `sentences`
    """
    aggregateScore = dict()
    sen = 0
    for scores in scoreGraph:
        aggregate = 0
        for i in scores:
            aggregate += i
        sentence = sentences[sen]
        aggregateScore[orig_sentences[sen]] = aggregate
        sen += 1
    return aggregateScore


def main():
    """
    Exectution starts here.
    Input's the content to be summarized.
    """
    # content = raw_input('Content: ')
    content = """
    The BBC has been testing a new service called SoundIndex, which lists the
    top 1,000 artists based on discussions crawled from Bebo, Last.fm, Google
    Groups, iTunes, MySpace and YouTube. The top five bands according to
    SoundIndex right now are Coldplay, Rihanna, The Ting Tings, Duffy and
    Mariah Carey , but the index is refreshed every six hours. SoundIndex also
    lets users sort by popular tracks, search by artist, or create customized
    charts based on music preferences or filters by age range, sex or location.
    Results can also be limited to just one data source (such as Last.fm).
    """
    paragraphs = util.getParagraphs(content)
    count = 0
    for paragraph in paragraphs:
        if paragraph:
            orig_sentences, indexed = util.getSentences(paragraph)
            sentences = remove_stopwords(orig_sentences)
            graph = sentenceGraph(sentences)
            score = build(sentences, graph, orig_sentences)
        print('Paragraph: ', count)
        count += 1
        for i in indexed:
            print(indexed[i], score[indexed[i]])
main()
