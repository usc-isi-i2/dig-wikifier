import sys, os, json
import argparse
from collections import defaultdict
from etk.etk import ETK
from etk.extractors.glossary_extractor import GlossaryExtractor
from etk.etk_module import ETKModule
import time

class GlossaryETKModule(ETKModule):
    """
    Abstract class for extraction module
    """
    def __init__(self, etk):
        ETKModule.__init__(self, etk)
        self.name_extractor = GlossaryExtractor(self.etk.load_glossary("./glossary.txt"), "anchor_extractor",
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
        self.etk = ETK(modules=GlossaryETKModule)

    # Perform same cleaning as what was done while processing wikidata
    def clean(self, string: str):
        string = ' '.join(string.split()).strip()
        return string

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
            texts = doc.select_segments("$.anchor_text")
            for text in texts:
                data.extend(text.value)
        end = time.time()
        return data


