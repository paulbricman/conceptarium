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


def memorize(thought):
    conceptarium = pickle.load(open(metadata_path, 'rb'))
    conceptarium += [thought]
    pickle.dump(conceptarium, open(metadata_path, 'wb'))


def remember(query, model, behavior='balanced', top_k=50):
    conceptarium = pickle.load(open(metadata_path, 'rb'))

    query_embedding = embed(query, model)
    query_modality = get_modality(query)

    modality_match = [e.modality == query_modality for e in conceptarium]
    corpus_embeddings = [e.embedding for e in conceptarium]

    results = util.semantic_search(
        [query_embedding], corpus_embeddings, top_k=len(corpus_embeddings))[0]
    results = [e if modality_match[e['corpus_id']]
               else compensate_modality_mismatch(e) for e in results]

    for result in results:
        conceptarium[result['corpus_id']].interest += result['score'] ** 4
    pickle.dump(conceptarium, open(metadata_path, 'wb'))

    for idx, result in enumerate(results):
        if behavior == 'balanced':
            results[idx]['activation'] = (result['score']
                                          + 0.02 *
                                          (np.log(
                                              conceptarium[result['corpus_id']].interest / (1 - 0.9))
                                           - 0.9 * np.log((time.time() - conceptarium[result['corpus_id']].timestamp) / 3600))) \
                * np.random.normal(1, 0.05)
        elif behavior == 'antimemory':
            results[idx]['activation'] = (result['score']
                                          - 0.02 *
                                          (np.log(
                                              conceptarium[result['corpus_id']].interest / (1 - 0.9))
                                           + 0.9 * np.log((time.time() - conceptarium[result['corpus_id']].timestamp) / 3600))) \
                * np.random.normal(1, 0.05)
        elif behavior == 'contextonly':
            results[idx]['activation'] = result['score']
        elif behavior == 'noisy':
            results[idx]['activation'] = (result['score']
                                          + 0.02 *
                                          (np.log(
                                              conceptarium[result['corpus_id']].interest / (1 - 0.9))
                                           - 0.9 * np.log((time.time() - conceptarium[result['corpus_id']].timestamp) / 3600))) \
                * np.random.normal(1, 0.2)

    results = sorted(
        results, key=lambda result: result['activation'], reverse=True)
    print(results)
    memories = [conceptarium[e['corpus_id']] for e in results][:top_k]
    return memories


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
    result['score'] *= 3.5
    return result


class Thought:
    def __init__(self, filename, content, model):
        self.filename = filename
        self.modality = get_modality(content)
        self.timestamp = time.time()
        self.interest = 1
        self.embedding = embed(content, model)
