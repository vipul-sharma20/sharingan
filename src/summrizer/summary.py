# -*- coding: utf-8 -*-

"""
Script to score sentences to get summary
"""

from nltk.corpus import stopwords
import util
import re


class Summrizer:
    def format_sentence(self, sentence):
        sentence = re.sub(r'\W+', '', sentence)
        return sentence

    def score_sentences(self, sen1, sen2):
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

    def remove_stopwords(self, sentences):
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

    def sentence_graph(self, sentences):
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
                sentence_score = 0
                if i == j:
                    continue
                else:
                    sentence_score = self.score_sentences(sentences[i],
                                                          sentences[j])
                weight.append(sentence_score)
            scoreGraph.append(weight)

        return scoreGraph

    def build(self, sentences, scoreGraph, orig_sentences):
        """
        Builds the content summary based on the graph
        :param sentences: (list) list of sentences
        :param scoreGraph: (list) 2 dimensional list-graph of scores
        :returns: Aggregate score of each sentence in `sentences`
        """
        aggregate_score = dict()
        sen = 0
        for scores in scoreGraph:
            aggregate = 0
            for i in scores:
                aggregate += i
            aggregate_score[orig_sentences[sen]] = aggregate
            sen += 1
        return aggregate_score

