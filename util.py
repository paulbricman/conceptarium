from sentence_transformers import SentenceTransformer, util
from PIL import Image
import io
import pickle
import os
import time


def init():
    if not os.path.exists('conceptarium.db'):
        pickle.dump(list(), open('conceptarium.db', 'wb'))


def add_thought(thought):
    conceptarium = pickle.load(open('conceptarium.db', 'rb'))
    conceptarium += [thought]
    pickle.dump(conceptarium, open('conceptarium.db', 'wb'))


def get_thoughts(query, model):
    conceptarium = pickle.load(open('conceptarium.db', 'rb'))
    query_embedding = embed(query, model)
    query_modality = get_modality(query)

    modality_match = [e.modality == query_modality for e in conceptarium]
    corpus_embeddings = [e.embedding for e in conceptarium]

    results = util.semantic_search(
        [query_embedding], corpus_embeddings, top_k=len(corpus_embeddings))[0]
    results = [e if modality_match[e['corpus_id']]
               else compensate_modality_mismatch(e) for e in results]

    # TODO propagate interest across other thoughts
    # TODO compute activation
    # TODO provde several default behaviors

    return format_response(results, conceptarium)


def load_model():
    return SentenceTransformer('clip-ViT-B-32')


def embed(content, model):
    if get_modality(content) == 'language':
        return model.encode(content, convert_to_tensor=True)
    else:
        return model.encode(Image.open(io.BytesIO(content)), convert_to_tensor=True)


def get_modality(content):
    if isinstance(content, str):
        return 'language'
    else:
        return 'imagery'


def compensate_modality_mismatch(result):
    result['score'] *= 2.2
    return result


def format_response(results, conceptarium):
    results = sorted(results, key=lambda x: x['score'], reverse=True)
    print(results)
    corpus_ids = [e['corpus_id'] for e in results]
    corpus_scores = [e['score'] for e in results]
    return [{
        'content': conceptarium[e].content,
        'modality': conceptarium[e].modality,
        'timestamp': conceptarium[e].timestamp,
        'activation': corpus_scores[corpus_ids.index(e)]
    } if conceptarium[e].modality == 'language' else {
        'modality': conceptarium[e].modality,
        'timestamp': conceptarium[e].timestamp,
        'activation': corpus_scores[corpus_ids.index(e)]
    } for e in corpus_ids]


class Thought:
    def __init__(self, content, model):
        self.content = content
        self.modality = get_modality(content)
        self.timestamp = time.time()
        self.interest = 1
        self.embedding = embed(content, model)
