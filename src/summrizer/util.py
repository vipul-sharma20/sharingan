"""
Utility functions for filtering content
"""
from nltk import tokenize
from nltk.tokenize import word_tokenize


def getWords(sentence):
    """
    Extracts words/tokens from a sentence
    :param sentence: (str) sentence
    :returns: list of tokens
    """
    words = word_tokenize(sentence)
    return words


def getParagraphs(content):
    """
    Exctracts paragraphs from the the text content
    :param content: (str) text content
    :returns: list of paragraphs
    """
    paraList = content.split('\n\n')
    return paraList


def getSentences(paragraph):
    """
    Extracts sentences from a paragraph
    :param paragraph: (str) paragraph text
    :returns: list of sentences
    """
    indexed = {}
    sentenceList = tokenize.sent_tokenize(paragraph)
    for i, s in enumerate(sentenceList):
        indexed[i] = s
    return sentenceList, indexed
