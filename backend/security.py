from pathlib import Path
import json
import bcrypt


def auth(token):
    if token == None:
        return {
            'custodian': False
        }

    path = Path('records.json')

    if not path.exists():
        salt = bcrypt.gensalt()
        hashed_token = bcrypt.hashpw(token.encode(
            'utf8'), salt).decode('utf8')

        records = {
            'custodian_hashed_token': hashed_token,
            'custodian_hashed_token_salt': salt.decode('utf8')
        }
        json.dump(records, open(path, 'w'))

        return {
            'custodian': True
        }
    else:
        records = json.load(open(path))
        hashed_token = bcrypt.hashpw(token.encode(
            'utf-8'), records['custodian_hashed_token_salt'].encode('utf8')).decode('utf8')

        if records['custodian_hashed_token'] == hashed_token:
            return {
                'custodian': True
            }
        else:
            return {
                'custodian': False
            }
