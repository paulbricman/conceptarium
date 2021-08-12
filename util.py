from sentence_transformers import SentenceTransformer, util
from PIL import Image
import io
import pickle
import os
import time
import numpy as np

metadata_path = 'conceptarium/metadata.pickle'


def init():
    if not os.path.exists(metadata_path):
        pickle.dump(list(), open(metadata_path, 'wb'))


def attach_metadata(thought):
    conceptarium = pickle.load(open(metadata_path, 'rb'))
    conceptarium += [thought]
    pickle.dump(conceptarium, open(metadata_path, 'wb'))


def remember(query, model, behavior='balanced'):
    conceptarium = pickle.load(open(metadata_path, 'rb'))

    # Prepare query
    query_embedding = embed(query, model)
    query_modality = get_modality(query)

    # Prepare corpus
    modality_match = [e.modality == query_modality for e in conceptarium]
    corpus_embeddings = [e.embedding for e in conceptarium]

    # Semantic search
    results = util.semantic_search(
        [query_embedding], corpus_embeddings, top_k=len(corpus_embeddings))[0]
    results = [e if modality_match[e['corpus_id']]
               else compensate_modality_mismatch(e) for e in results]

    # Propagate interest
    for result in results:
        conceptarium[result['corpus_id']].interest += result['score']
    pickle.dump(conceptarium, open(metadata_path, 'wb'))

    if behavior == 'balanced':
        results = sorted(
            results,
            key=lambda x: ((
                x['score']
                + 0.1 * np.log(conceptarium[x['corpus_id']].interest / (1 - 0.9)) - 0.9 * np.log(conceptarium[x['corpus_id']].timestamp / 3600 * 24))
                * np.random.normal(1, 0.1)
            ),
            reverse=True)
    elif behavior == 'antimemory':
        results = sorted(
            results,
            key=lambda x: ((
                x['score']
                - 0.1 * np.log(conceptarium[x['corpus_id']].interest / (1 - 0.9)) - 0.9 * np.log(conceptarium[x['corpus_id']].timestamp / 3600 * 24))
                * np.random.normal(1, 0.1)
            ),
            reverse=True)
    elif behavior == 'context-only':
        results = sorted(
            results,
            key=lambda x: x['score'],
            reverse=True)
    if behavior == 'noisy':
        results = sorted(
            results,
            key=lambda x: ((
                x['score']
                + 0.1 * np.log(conceptarium[x['corpus_id']].interest / (1 - 0.9)) - 0.9 * np.log(conceptarium[x['corpus_id']].timestamp / 3600 * 24))
                * np.random.normal(1, 0.5)
            ),
            reverse=True)

    memories = [conceptarium[e['corpus_id']] for e in results][:10]

    return memories


def html_response(thoughts):
    html = ''

    for thought in thoughts:
        if thought.modality == 'language':
            content = open(thought.filename, 'r').read()
            html += '<p>' + content + '</p>'
        else:
            html += '<img src=\"/' + thought.filename + '\" width="20%">'

    return html


def plaintext_response(thoughts):
    plaintext = ''

    for thought in thoughts:
        if thought.modality == 'language':
            content = open(thought.filename, 'r').read()
            plaintext += '\"' + content + '\"\n'

    return plaintext


def json_response(thoughts):
    json = []

    for thought in thoughts:
        if thought.modality == 'language':
            thought = {
                'content': open(thought.filename, 'r').read(),
                'modality': thought.modality,
                'timestamp': thought.timestamp,
                'interest': thought.interest,
                'embedding': thought.embedding.tolist()
            }
        else:
            thought = {
                'content': '/' + thought.filename,
                'modality': thought.modality,
                'timestamp': thought.timestamp,
                'interest': thought.interest,
                'embedding': thought.embedding.tolist()
            }

        json += [thought]
    return json


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
    result['score'] *= 2.8
    return result


class Thought:
    def __init__(self, filename, content, model):
        self.filename = filename
        self.modality = get_modality(content)
        self.timestamp = time.time()
        self.interest = 1
        self.embedding = embed(content, model)
