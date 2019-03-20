import sys, os, json
import argparse
from collections import defaultdict
from etk.etk import ETK
#from etk.extractors.glossary_extractor import GlossaryExtractor
from glossary_extractor import GlossaryExtractor
from etk.etk_module import ETKModule
import time, string

class GlossaryETKModule(ETKModule):
    """
    Abstract class for extraction module
    """
    def __init__(self, etk):
        ETKModule.__init__(self, etk)
        self.name_extractor = GlossaryExtractor("anchor_extractor",
                                                self.etk.default_tokenizer,
                                                case_sensitive=True, ngrams=4)
    def process_document(self, doc):
        """
        Add your code for processing the document
        """

        descriptions = doc.select_segments("text_description")
        # First phase of extraction
        for d in descriptions:
            names = doc.extract(self.name_extractor, d)
            doc.store(names, "anchor_text")

        return list()

class AnchorTextExtractor():
    """
    Class that wraps the ETK Glossary extractor module. This module is what interfaces with the Flask APIs

    """
    def __init__(self):
        """
        Sets up the class by initializing the glossary extractor which loads the glossary into an in memory trie
        """
        self.etk = ETK(modules=GlossaryETKModule, use_spacy_tokenizer=True)

    # Perform same cleaning as what was done while processing wikidata
    def clean(self, st: str):
        punc_dict = dict.fromkeys(string.punctuation)
        translator = str.maketrans(punc_dict)
        st = ' '.join(st.split()).strip()
        st = st.translate(translator)
        return st

    def eliminate_sub_mentions(self, arr):
        arr = sorted(arr, key=lambda x: x['start'])
        st = []
        for interval in arr:
            st.append(interval)
            while len(st) > 1 and ((st[-1]['start'] <= st[-2]['end']) and (st[-2]['start'] < st[-1]['end'])):
                t = st.pop()
                if t['end'] - t['start'] > st[-1]['end'] - st[-1]['start']:
                    st[-1] = {'text': t['text'], 'start': min(t['start'], st[-1]['start']),
                              'end': max(t['end'], st[-1]['end'])}
                else:
                    st[-1] = {'text': st[-1]['text'], 'start': min(t['start'], st[-1]['start']),
                              'end': max(t['end'], st[-1]['end'])}
        return list(st)

    def extract_tokens(self, text):
        """

        :param text:  The text to extract tokens from
        :return: set of tokens
        """
        text["text_description"] = self.clean(text["text_description"])
        doc = self.etk.create_document(text)
        start = time.time()
        docs = self.etk.process_ems(doc)
        data = list()
        for doc in docs:
            extractions = doc.extractions
            all_names = list()
            for key,value in extractions.items():
                for name in value:
                    all_names.append(
                        {'text': name.value, 'start': name.provenance['start_char'], 'end': name.provenance['end_char']})
            extractions = self.eliminate_sub_mentions(all_names)
            for ext in extractions:
                data.append(ext['text'])
        end = time.time()
        return data



