import json
from pathlib import Path
from ics import Calendar, Event
import requests


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


def get_ical_events():
    records_path = Path('..') / 'knowledge' / 'records.json'
    ical_url = json.load(open(records_path)).get('bibliography_ical')

    if not ical_url:
        return []

    cal = Calendar(requests.get(ical_url).text)
    events = list(cal.events)
    for e_idx, e in enumerate(events):
        event_dict = {}
        event_dict['name'] = e.name.replace('"', '')
        event_dict['timestamp'] = (e.begin.timestamp + e.end.timestamp) // 2
        events[e_idx] = event_dict

    events = sorted(events, key=lambda x: x['timestamp'])
    return events
