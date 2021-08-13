def html_response(thoughts):
    html = ''

    for thought in thoughts:
        if thought.modality == 'language':
            content = open(thought.filename, 'r').read()
            html += '<p>' + content + '</p>'
        else:
            html += '<img src=\"/' + thought.filename + '\" width="20%">'

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
