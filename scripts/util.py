from sentence_transformers import SentenceTransformer, util
from PIL import Image
import io
import pickle
import os
import time
import numpy as np
import pprint

metadata_path = 'conceptarium/metadata.pickle'


def init():
    if not os.path.exists(metadata_path):
        os.mkdir('conceptarium')
        pickle.dump(list(), open(metadata_path, 'wb'))


def save(thought):
    conceptarium = pickle.load(open(metadata_path, 'rb'))

    if len(conceptarium) > 0:
        modality_match = [e.modality == thought.modality for e in conceptarium]
        corpus_embeddings = [e.embedding for e in conceptarium]

        results = util.semantic_search(
            [thought.embedding], corpus_embeddings, top_k=len(corpus_embeddings), score_function=util.dot_score)[0]
        results = [e if modality_match[e['corpus_id']]
                   else compensate_modality_mismatch(e) for e in results]

        for result in results:
            conceptarium[result['corpus_id']
                         ].interest += result['score']

    if len(list(filter(lambda x: open(x.filename, 'rb').read() == open(thought.filename, 'rb').read(), conceptarium))) == 0:
        conceptarium += [thought]
        pickle.dump(conceptarium, open(metadata_path, 'wb'))


def find(query, model, relatedness, serendipity, noise, silent, top_k):
    conceptarium = pickle.load(open(metadata_path, 'rb'))

    query_embedding = embed(query, model)
    query_modality = get_modality(query)

    modality_match = [e.modality == query_modality for e in conceptarium]
    corpus_embeddings = [e.embedding for e in conceptarium]

    results = util.semantic_search(
        [query_embedding], corpus_embeddings, top_k=len(corpus_embeddings), score_function=util.dot_score)[0]
    results = [e if modality_match[e['corpus_id']]
               else compensate_modality_mismatch(e) for e in results]

    if not silent:
        for result in results:
            conceptarium[result['corpus_id']
                         ].interest += result['score']
        pickle.dump(conceptarium, open(metadata_path, 'wb'))

    for idx, result in enumerate(results):
        results[idx]['score'] = (relatedness * result['score']
                                 - serendipity *
                                 (np.log(conceptarium[result['corpus_id']].interest / (1 - 0.9)) - 0.9 * np.log((time.time() - conceptarium[result['corpus_id']].timestamp) / (3600 * 24) + 0.1))) \
            * np.random.normal(1, noise)

    results = sorted(
        results, key=lambda result: result['score'], reverse=True)
    memories = [conceptarium[e['corpus_id']] for e in results][:top_k]
    return memories


def get_doc_paths(directory):
    paths = []

    for root, directories, files in os.walk(directory):
        for filename in files:
            path = os.path.join(root, filename)
            paths.append(path)

    return paths


def load_model():
    return SentenceTransformer('clip-ViT-B-32')


def embed(content, model):
    if get_modality(content) == 'language':
        return model.encode(content, convert_to_tensor=True, normalize_embeddings=True)
    else:
        return model.encode(Image.open(io.BytesIO(content)), convert_to_tensor=True, normalize_embeddings=True)


def reset_embeddings(model):
    conceptarium = pickle.load(open(metadata_path, 'rb'))
    for thought_idx, thought in enumerate(conceptarium):
        if thought.modality == 'language':
            content = open(thought.filename, 'r').read()
        else:
            content = open(thought.filename, 'rb').read()
        conceptarium[thought_idx].embedding = embed(content, model)

    pickle.dump(conceptarium, open(metadata_path, 'wb'))


def get_modality(content):
    if isinstance(content, str):
        return 'language'
    else:
        return 'imagery'


def compensate_modality_mismatch(result):
    result['score'] *= 2.5
    return result


class Thought:
    def __init__(self, filename, content, model):
        self.filename = filename
        self.modality = get_modality(content)
        self.timestamp = time.time()
        self.interest = 1
        self.embedding = embed(content, model)

    def get_content(self):
        if self.modality == 'language':
            return open(self.filename).read()
        elif self.modality == 'imagery':
            return open(self.filename, 'rb').read()


'''
import json
thoughts = json.load(open('knowledge/base/metadata.json', 'rb'))

from datetime import datetime
new_thoughts = []
for thought in thoughts:
    new_thought = {}
    new_thought['filename'] = thought.filename
    new_thought['modality'] = thought.modality
    new_thought['timestamp'] = thought.timestamp
    new_thought['interest'] = thought.interest
    new_thought['embedding'] = thought.embedding
    new_thoughts += [new_thought]

for e_idx, e in enumerate(new_thoughts):
    if e['modality'] == 'language':
        new_thoughts[e_idx]['modality'] = 'text'
    elif e['modality'] == 'imagery':
        new_thoughts[e_idx]['modality'] = 'image'
    else:
        print(e['modality'])

for e_idx, e in enumerate(new_thoughts):
    new_thoughts[e_idx]['embedding'] = e['embedding'].tolist()

for e_idx, e in enumerate(new_thoughts):
    new_thoughts[e_idx]['embedding'] = [round(f, 5) for f in e['embedding']]

for e_idx, e in enumerate(new_thoughts):
    new_thoughts[e_idx]['filename'] = e['filename'].split('/')[-1]

def get_content(thought, json_friendly=False):
    knowledge_base_path = Path('conceptarium')
    if thought['modality'] == 'text':
        content = open(knowledge_base_path / thought['filename']).read()
    elif thought['modality'] == 'image':
        content = open(knowledge_base_path / thought['filename'], 'rb').read()
        if json_friendly:
            content = thought['filename']
    return content

from sentence_transformers import SentenceTransformer, util
from pathlib import Path
from PIL import Image
import io

text_image_encoder = SentenceTransformer('clip-ViT-B-32')
text_encoder = SentenceTransformer(
    'sentence-transformers/multi-qa-mpnet-base-cos-v1')

for e_idx, e in enumerate(new_thoughts):
    if 'embedding' in e.keys():
        new_thoughts[e_idx].pop('embedding')
    embs = encode(new_thoughts[e_idx]['modality'], get_content(new_thoughts[e_idx]), text_encoder, text_image_encoder)
    new_thoughts[e_idx]['embeddings'] = embs

new_thoughts[0]
json.dump(new_thoughts, open('conceptarium/metadata.json', 'w'))
'''
