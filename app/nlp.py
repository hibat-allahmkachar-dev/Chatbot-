import spacy


class NLPAnalyzer:
    def __init__(self):
        # Charge le modele UNE SEULE FOIS, au demarrage
        self.nlp = spacy.load("fr_core_news_sm")

    def analyze(self, text: str) -> dict:
        doc = self.nlp(text)

        tokens = [token.text for token in doc]
        lemmas = [token.lemma_ for token in doc]
        pos_tags = [(token.text, token.pos_) for token in doc]

        entities = [
            {"text": ent.text, "label": ent.label_}
            for ent in doc.ents
        ]

        keywords = [
            token.lemma_ for token in doc
            if token.pos_ in ["NOUN", "VERB", "ADJ"] and not token.is_stop
        ]

        return {
            "tokens": tokens, "lemmas": lemmas, "pos_tags": pos_tags,
            "entities": entities, "keywords": keywords
        }

    def extract_city(self, text: str):
        doc = self.nlp(text)
        for ent in doc.ents:
            if ent.label_ == "GPE":   # Geopolitical Entity (ville, pays)
                return ent.text
        return None