from util import get_doc_paths
from zipfile import ZipFile


def html_response(thoughts):
    html = '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">'
    html += '<link rel="stylesheet" type="text/css" href="/conceptarium/style.css" media="screen" />'
    html += '<div class="header"><h2>conceptarium.</h2></div>'
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


def success_response():
    return open('conceptarium/success.html').read()


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
            'modality': thought.modality,
            'embedding': thought.embedding.tolist(),
        }

        if thought.modality == 'language':
            thought_json['content'] = open(thought.filename, 'r').read()
        else:
            thought_json['filename'] = '/' + thought.filename

        response_json += [thought_json]
    return response_json
