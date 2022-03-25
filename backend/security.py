from pathlib import Path
import json
import os


def auth(token, compact=False):
    if not token:
        return {
            'custodian': False
        }

    knowledge_base_path = Path('..') / 'knowledge'
    records_path = knowledge_base_path / 'records.json'

    if not records_path.exists():
        if not knowledge_base_path.exists():
            os.mkdir(knowledge_base_path)

        records = {
            'custodian_token': token
        }
        json.dump(records, open(records_path, 'w'))

        return {
            'custodian': True
        }
    else:
        records = json.load(open(records_path))

        if records['custodian_token'] == token:
            return {
                'custodian': True
            }
        else:
            microverses_path = Path('..') / 'knowledge' / 'microverses.json'
            if not microverses_path.exists():
                json.dump([], open(microverses_path, 'w'))

            microverses = json.load(open(microverses_path))
            authorized_microverse = [
                e for e in microverses if e['token'] == token]

            if compact:
                if len(authorized_microverse) > 0:
                    authorized_microverse[0].pop('embeddings')

            return {
                'custodian': False,
                'authorized_microverse': authorized_microverse
            }
