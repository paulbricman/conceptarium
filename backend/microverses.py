import json
from pathlib import Path
from util import encode
import secrets
import time
from PIL import Image
import io


def create_microverse(modality, query, auth_result, text_encoder, text_image_encoder):
    knowledge_base_path = Path('..') / 'knowledge' / 'base'
    microverses_path = Path('microverses.json')

    if auth_result['custodian'] == False:
        return {
            'message': 'Only the conceptarium\'s custodian can create microverses in it.'
        }
    else:
        if not microverses_path.exists():
            json.dump([], open(microverses_path, 'w'))

        query_embedding = encode(
            modality, query, text_encoder, text_image_encoder)
        token = secrets.token_urlsafe(8)

        if modality == 'text':
            filename = secrets.token_urlsafe(8) + '.md'
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
            filename = secrets.token_urlsafe(8) + '.jpg'
            query = Image.open(io.BytesIO(query)).convert('RGB')
            query.save(knowledge_base_path / filename, quality=50)

            microverses = json.load(open(microverses_path))
            microverses += {
                "filename": filename,
                "modality": modality,
                "timestamp": time.time(),
                "token": token,
                "embeddings": query_embedding
            }
            json.dump(microverses, open(microverses_path, 'w'))

        return {
            "token": token
        }


def remove_microverse(auth_result, microverse_token):
    microverses_path = Path('microverses.json')

    if auth_result['custodian'] == False:
        return {
            'message': 'Only the conceptarium\'s custodian can create microverses in it.'
        }
    else:
        microverses = json.load(open(microverses_path))
        microverses = [
            e for e in microverses if e['token'] != microverse_token]
        json.dump(microverses, open(microverses_path, 'w'))
