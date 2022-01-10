import json
from pathlib import Path
from PIL import Image
import io
from sentence_transformers import util
import torch
import base64


def find(modality, query, auth_result, encoder_model):
    authorized_thoughts = get_authorized_thoughts(auth_result)

    if len(authorized_thoughts) == 0:
        return []

    query_embedding = torch.Tensor([embed(modality, query, encoder_model)])
    print('query_embedding.size()', query_embedding.size())
    corpus_embeddings = torch.Tensor(
        [e['embedding'] for e in authorized_thoughts])
    results = util.semantic_search(
        query_embedding, corpus_embeddings, top_k=10 ** 10)

    for e in results[0]:
        authorized_thoughts[e['corpus_id']]['relatedness'] = e['score']
        authorized_thoughts[e['corpus_id']]['content'] = get_content(
            authorized_thoughts[e['corpus_id']])
        authorized_thoughts[e['corpus_id']].pop('filename', None)

    return authorized_thoughts


def get_authorized_thoughts(auth_result):
    metadata_path = Path('..') / 'knowledge' / 'base' / 'metadata.json'

    if auth_result['custodian'] == True:
        return json.load(open(metadata_path))
    else:
        return []


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
            content = base64.encodebytes(content).decode('utf8')

    return content
