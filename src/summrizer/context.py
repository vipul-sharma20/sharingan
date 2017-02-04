# -*- coding: utf-8 -*-

"""
Script to extract important topics from content
"""

import nltk
from nltk.corpus import brown
import util


train = brown.tagged_sents(categories='news')

# backoff regex tagging
regex_tag = nltk.RegexpTagger([
     (r'^[-\:]?[0-9]+(.[0-9]+)?$', 'CD'),
     (r'.*able$', 'JJ'),
     (r'^[A-Z].*$', 'NNP'),
     (r'.*ly$', 'RB'),
     (r'.*s$', 'NNS'),
     (r'.*ing$', 'VBG'),
     (r'.*ed$', 'VBD'),
     (r'.*', 'NN')
])

unigram_tag = nltk.UnigramTagger(train, backoff=regex_tag)
bigram_tag = nltk.BigramTagger(train, backoff=unigram_tag)

# custom defined CFG
cfg = dict()
cfg['NNP+NNP'] = 'NNP'
cfg['NN+NN'] = 'NNI'
cfg['NNI+NN'] = 'NNI'
cfg['JJ+JJ'] = 'JJ'
cfg['JJ+NN'] = 'NNI'


class ContextExtract():
    """
    Extracts context of the text content, relevant topics from the text
    """

    def get_info(self, content):
        words = util.getWords(content)
        temp_tags = bigram_tag.tag(words)
        tags = self.re_tag(temp_tags)
        normalized = True
        while normalized:
            normalized = False
            for i in range(0, len(tags) - 1):
                tagged1 = tags[i]
                if i+1 >= len(tags):
                    break
                tagged2 = tags[i+1]
                key = tagged1[1] + '+' + tagged2[1]
                pos = cfg.get(key)
                if pos:
                    tags.pop(i)
                    tags.pop(i)
                    re_tagged = tagged1[0] + ' ' + tagged2[0]
                    tags.insert(i, (re_tagged, pos))
                    normalized = True

        final_context = []
        for tag in tags:
            if tag[1] == 'NNP' or tag[1] == 'NNI':
                final_context.append(tag[0])
        return final_context

    def re_tag(self, tagged):
        new_tagged = []
        for tag in tagged:
            if tag[1] == 'NP' or tag[1] == 'NP-TL':
                new_tagged.append((tag[0], 'NNP'))
            elif tag[1][-3:] == '-TL':
                new_tagged.append((tag[0], tag[1][:-3]))
            elif tag[1][-1:] == 'S':
                new_tagged.append((tag[0], tag[1][:-1]))
            else:
                new_tagged.append((tag[0], tag[1]))
        return new_tagged


def main():
        # content = raw_input("Content: ")
        content = """
            The BBC has been testing a new service called SoundIndex, which
            lists the top 1,000 artists based on discussions crawled from Bebo,
            Last.fm, Google Groups, iTunes, MySpace and YouTube. The top five
            bands according to SoundIndex right now are Coldplay, Rihanna, The
            Ting Tings, Duffy and Mariah Carey , but the index is refreshed
            every six hours. SoundIndex also lets users sort by popular tracks,
            search by artist, or create customized charts based on music
            preferences or filters by age range, sex or location. Results can
            also be limited to just one data source (such as Last.fm).
        """
        np = ContextExtract()
        context = np.get_info(content)
        print(context)
#main()
