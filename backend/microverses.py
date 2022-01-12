import json
from pathlib import Path
from util import embed
import secrets
import time
from PIL import Image
import io


def create_microverse(modality, query, auth_result, encoder_model):
    knowledge_base_path = Path('..') / 'knowledge' / 'base'
    microverses_path = Path('microverses.json')

    if auth_result['custodian'] == False:
        return 'Only the conceptarium\'s custodian can create microverses in it.'
    else:
        if not microverses_path.exists():
            json.dump([], open(microverses_path, 'w'))

        embedding = [round(e, 6)
                     for e in embed(modality, query, encoder_model).tolist()]
        token = secrets.token_urlsafe(8)

        if modality == 'text':
            filename = secrets.token_urlsafe(8) + '.md'
            query = Image.open(io.BytesIO(query)).convert('RGB')
            query.save(knowledge_base_path / filename, quality=50)

            microverses = json.load(open(microverses_path))
            microverses += [{
                "filename": filename,
                "modality": modality,
                "timestamp": time.time(),
                "token": token,
                "embedding": embedding
            }]
            json.dump(microverses, open(microverses_path, 'w'))
        elif modality == 'image':
            filename = secrets.token_urlsafe(8) + '.jpg'
            open(knowledge_base_path / filename, 'wb').write(query)

            microverses = json.load(open(microverses_path))
            microverses += [{
                "filename": filename,
                "modality": modality,
                "timestamp": time.time(),
                "token": token,
                "embedding": embedding
            }]
            json.dump(microverses, open(microverses_path, 'w'))

        return token


def remove_microverse(auth_result, microverse_token):
    microverses_path = Path('microverses.json')

    if auth_result['custodian'] == False:
        return 'Only the conceptarium\'s custodian can create microverses in it.'
    else:
        microverses = json.load(open(microverses_path))
        microverses = [
            e for e in microverses if e['token'] != microverse_token]
        json.dump(microverses, open(microverses_path, 'w'))
