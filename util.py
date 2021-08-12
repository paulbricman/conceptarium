from sentence_transformers import SentenceTransformer, util
from PIL import Image
import io
import pickle
import os
import time

metadata_path = 'conceptarium/metadata.pickle'


def init():
    if not os.path.exists(metadata_path):
        pickle.dump(list(), open(metadata_path, 'wb'))


def attach_metadata(thought):
    conceptarium = pickle.load(open(metadata_path, 'rb'))
    conceptarium += [thought]
    pickle.dump(conceptarium, open(metadata_path, 'wb'))


def get_thoughts(query, model):
    conceptarium = pickle.load(open(metadata_path, 'rb'))

    query_embedding = embed(query, model)
    query_modality = get_modality(query)

    modality_match = [e.modality == query_modality for e in conceptarium]
    corpus_embeddings = [e.embedding for e in conceptarium]

    results = util.semantic_search(
        [query_embedding], corpus_embeddings, top_k=len(corpus_embeddings))[0]
    results = [e if modality_match[e['corpus_id']]
               else compensate_modality_mismatch(e) for e in results]
    results = sorted(results, key=lambda x: x['score'], reverse=True)
    corpus_ids = [e['corpus_id'] for e in results]
    thoughts = [conceptarium[e] for e in corpus_ids][:10]

    # TODO propagate interest across other thoughts
    # TODO compute activation
    # TODO provde several default behaviors

    return thoughts


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
