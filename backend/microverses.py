import json
from pathlib import Path
from util import encode, get_content
import secrets
import time
from PIL import Image
import io
import os


def create_microverse(modality, query, auth_result, text_encoder, text_image_encoder):
    knowledge_base_path = Path('..') / 'knowledge'
    microverses_path = knowledge_base_path / 'microverses.json'

    if auth_result['custodian'] == False:
        return {
            'message': 'Only the conceptarium\'s custodian can create microverses in it.'
        }
    else:
        if not microverses_path.exists():
            json.dump([], open(microverses_path, 'w'))

        query_embedding = encode(
            modality, query, text_encoder, text_image_encoder)
        token = secrets.token_urlsafe(16)

        if modality == 'text':
            filename = secrets.token_urlsafe(16) + '.md'
            open(knowledge_base_path / filename, 'w').write(query)

            microverses = json.load(open(microverses_path))
            microverses += [{
                "filename": filename,
                "modality": modality,
                "timestamp": time.time(),
                "token": token,
                "embeddings": query_embedding
            }]
            json.dump(microverses, open(microverses_path, 'w'))
        elif modality == 'image':
            filename = secrets.token_urlsafe(16) + '.jpg'
            query = Image.open(io.BytesIO(query)).convert('RGB')
            query.save(knowledge_base_path / filename, quality=50)

            microverses = json.load(open(microverses_path))
            microverses += [{
                "filename": filename,
                "modality": modality,
                "timestamp": time.time(),
                "token": token,
                "embeddings": query_embedding
            }]
            json.dump(microverses, open(microverses_path, 'w'))

        return {
            "token": token
        }


def remove_microverse(auth_result, microverse_token):
    knowledge_base_path = Path('..') / 'knowledge'
    microverses_path = knowledge_base_path / 'microverses.json'

    if auth_result['custodian'] == False:
        return {
            'message': 'Only the conceptarium\'s custodian can create microverses in it.'
        }
    else:
        microverses = json.load(open(microverses_path))
        microverses = [
            e for e in microverses if e['token'] != microverse_token]
        removal_target = [
            e for e in microverses if e['token'] == microverse_token]
        json.dump(microverses, open(microverses_path, 'w'))
        if len(removal_target) > 0:
            os.remove(knowledge_base_path / removal_target[0]['filename'])


def list_microverses(auth_result):
    microverses_path = Path('..') / 'knowledge' / 'microverses.json'

    if auth_result['custodian'] == False:
        return {
            'message': 'Only the conceptarium\'s custodian can list all microverses in it.'
        }
    else:
        if not microverses_path.exists():
            json.dump([], open(microverses_path, 'w'))

        microverses = json.load(open(microverses_path))

        for e_idx, e in enumerate(microverses):
            microverses[e_idx]['content'] = get_content(
                e, True)
        return microverses
