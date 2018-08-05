import base64, quopri, re

def encoded_words_to_text(encoded_words):
    encoded_word_regex = r'=\?{1}(.+)\?{1}([B|Q])\?{1}(.+)\?{1}='
    charset, encoding, encoded_text = re.match(encoded_word_regex, encoded_words).groups()
    if encoding is 'B':
        byte_string = base64.b64decode(encoded_text)
    elif encoding is 'Q':
        byte_string = quopri.decodestring(encoded_text)
    return byte_string.decode(charset)

def decode_file_name(file_name):
    if file_name.lower().count('=?utf-8') != 0:
        file_name = file_name.split()
        full_name = list()
        for word in file_name:
            full_name.append(encoded_words_to_text(word))
        file_name = ''.join(full_name)
    return file_name







