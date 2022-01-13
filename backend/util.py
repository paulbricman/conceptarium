import json
from pathlib import Path
from PIL import Image
import io
from sentence_transformers import util
import torch
import secrets
import time
import numpy as np
from numpy.linalg import norm


def find(modality, query, auth_result, encoder_model):
    authorized_thoughts = get_authorized_thoughts(auth_result)

    if len(authorized_thoughts) == 0:
        return []

    query_embedding = torch.Tensor([embed(modality, query, encoder_model)])
    corpus_embeddings = torch.Tensor(
        [e['embedding'] for e in authorized_thoughts])
    results = util.semantic_search(
        query_embedding, corpus_embeddings, top_k=10 ** 10)

    for e in results[0]:
        authorized_thoughts[e['corpus_id']]['relatedness'] = e['score']
        authorized_thoughts[e['corpus_id']]['content'] = get_content(
            authorized_thoughts[e['corpus_id']], True)
        authorized_thoughts[e['corpus_id']].pop('filename', None)

    authorized_thoughts = sorted(
        authorized_thoughts, key=lambda x: x['relatedness'], reverse=True)

    return authorized_thoughts


def save(modality, query, auth_result, encoder_model):
    knowledge_base_path = Path('..') / 'knowledge' / 'base'

    if auth_result['custodian'] == False:
        return {
            'message': 'Only the conceptarium\'s custodian can save thoughts in it.'
        }
    else:
        if not (knowledge_base_path / 'metadata.json').exists():
            json.dump([], open(knowledge_base_path / 'metadata.json', 'w'))

        query_embedding = [round(e, 6)
                           for e in embed(modality, query, encoder_model).tolist()]
        thoughts = json.load(open(knowledge_base_path / 'metadata.json'))

        if modality == 'text':
            duplicates = [e for e in thoughts if e['modality'] ==
                          'text' and open(knowledge_base_path / e['filename']).read() == query]

            if len(duplicates) == 0:
                filename = secrets.token_urlsafe(8) + '.md'
                open(knowledge_base_path / filename, 'w').write(query)
        elif modality == 'image':
            duplicates = [e for e in thoughts if e['modality'] ==
                          'image' and open(knowledge_base_path / e['filename'], 'rb').read() == query]

            if len(duplicates) == 0:
                filename = secrets.token_urlsafe(8) + '.jpg'
                query = Image.open(io.BytesIO(query)).convert('RGB')
                query.save(knowledge_base_path / filename, quality=50)

        if len(duplicates) == 0:
            new_thought = {
                'filename': filename,
                'modality': modality,
                'timestamp': time.time(),
                'interest': 1,
                'embedding': query_embedding
            }

            thoughts += [new_thought]
            json.dump(thoughts, open(
                knowledge_base_path / 'metadata.json', 'w'))

            return new_thought
        else:
            return {
                'message': 'Duplicate thought found.'
            }


def get_authorized_thoughts(auth_result):
    metadata_path = Path('..') / 'knowledge' / 'base' / 'metadata.json'
    thoughts = json.load(open(metadata_path))

    if auth_result['custodian'] == True:
        return thoughts
    else:
        similarity_threshold = 0.7
        authorized_microverse = auth_result['authorized_microverse']

        results = util.semantic_search(
            torch.Tensor(authorized_microverse['embedding']), torch.Tensor([e['embedding'] for e in thoughts]), top_k=10 ** 10)
        authorized_thoughts = [thoughts[result['corpus_id']]
                               for result in results[0] if result['score'] > similarity_threshold]

        return authorized_thoughts


def embed(modality, content, encoder_model):
    if modality == 'text':
        return encoder_model.encode(content)
    elif modality == 'image':
        return encoder_model.encode(Image.open(io.BytesIO(content)))


def get_content(thought, json_friendly=False):
    knowledge_base_path = Path('..') / 'knowledge' / 'base'

    if thought['modality'] == 'text':
        content = open(knowledge_base_path / thought['filename']).read()
    elif thought['modality'] == 'image':
        content = open(knowledge_base_path / thought['filename'], 'rb').read()

        if json_friendly:
            content = thought['filename']

    return content
