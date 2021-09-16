from util import get_doc_paths
from zipfile import ZipFile
import numpy as np
import time


def html_response(thoughts):
    html = '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">'
    html += '<link rel="stylesheet" type="text/css" href="/assets/style.css" media="screen" />'
    html += '<div class="header"><h2>🌿&nbspconceptarium.</h2></div>'
    html += '<div class="board">'

    for thought in thoughts:
        html += '<div class="card">'
        if thought.modality == 'language':
            content = open(thought.filename, 'r').read()
            html += '<div class="card-body">' + content + '</div>'
        else:
            html += '<img class="card-img" src=\"/' + \
                thought.filename + '\">'
        html += '</div><br/>'

    html += '</div>'
    return html


def save_success_response():
    return open('assets/success.html').read()


def save_lang_form_response():
    return open('assets/save_lang.html').read()


def save_imag_form_response():
    return open('assets/save_imag.html').read()


def find_lang_form_response():
    return open('assets/find_lang.html').read()


def find_imag_form_response():
    return open('assets/find_imag.html').read()


def archive_response():
    paths = get_doc_paths('conceptarium')
    with ZipFile('conceptarium.zip', 'w') as zip:
        for path in paths:
            zip.write(path)

    return 'conceptarium.zip'


def plaintext_response(thoughts):
    plaintext = ''

    for thought in thoughts:
        if thought.modality == 'language':
            content = open(thought.filename, 'r').read()
            plaintext += '\"' + content + '\"\n'

    return plaintext


def file_response(thoughts):
    for thought in thoughts:
        if thought.modality == 'imagery':
            return thought.filename


def json_response(thoughts):
    response_json = []

    for thought in thoughts:
        thought_json = {
            'timestamp': thought.timestamp,
            'interest': thought.interest,
            'activation': np.log(thought.interest / (1 - 0.9)) - 0.9 * np.log((time.time() - thought.timestamp) / (3600 * 24) + 0.1),
            'modality': thought.modality,
            'embedding': thought.embedding.tolist(),
        }

        if thought.modality == 'language':
            thought_json['content'] = open(thought.filename, 'r').read()
        else:
            thought_json['filename'] = '/' + thought.filename

        response_json += [thought_json]
    return response_json
