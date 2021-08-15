def html_response(thoughts):
    html = '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">'
    html += '<link rel="stylesheet" type="text/css" href="/conceptarium/style.css" media="screen" />'
    html += '<div class="board">'

    for thought in thoughts:
        html += '<div class="card">'
        if thought.modality == 'language':
            content = open(thought.filename, 'r').read()
            html += '<div class="card-body">' + content + '</div>'
        else:
            html += '<img class="card-img" src=\"/' + \
                thought.filename + '\">'
        html += '</div>'

    html += '</div>'
    return html


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
    json = []

    for thought in thoughts:
        if thought.modality == 'language':
            thought = {
                'content': open(thought.filename, 'r').read(),
                'modality': thought.modality,
                'timestamp': thought.timestamp,
                'interest': thought.interest,
                'embedding': thought.embedding.tolist()
            }
        else:
            thought = {
                'content': '/' + thought.filename,
                'modality': thought.modality,
                'timestamp': thought.timestamp,
                'interest': thought.interest,
                'embedding': thought.embedding.tolist()
            }

        json += [thought]
    return json
