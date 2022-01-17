from pathlib import Path
import json


def auth(token):
    if token == None:
        return {
            'custodian': False
        }

    path = Path('records.json')

    if not path.exists():
        records = {
            'custodian_token': token
        }
        json.dump(records, open(path, 'w'))

        return {
            'custodian': True
        }
    else:
        records = json.load(open(path))

        if records['custodian_token'] == token:
            return {
                'custodian': True
            }
        else:
            microverses_path = Path('microverses.json')
            if not microverses_path.exists():
                json.dump([], open(microverses_path, 'w'))

            microverses = json.load(open(microverses_path))
            authorized_microverse = [
                e for e in microverses if e['token'] == token]

            return {
                'custodian': False,
                'authorized_microverse': authorized_microverse
            }
