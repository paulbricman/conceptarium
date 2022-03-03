import json
from pathlib import Path


def set_ical(ical_url, auth):
    if not auth['custodian']:
        return {
            'message': 'Only the conceptarium\'s custodian can set its bibliography ical.'
        }

    records_path = Path('..') / 'knowledge' / 'records.json'
    records = json.load(open(records_path))
    records['bibliography_ical'] = ical_url
    records = json.dump(records, open(records_path, 'w'))

    return {
        'message': 'Successfully set bibliography ical.'
    }
