import string

def delete_punctuation(text):

    # delete punctuation from the text
    no_punct_text = text.translate(str.maketrans('', '', string.punctuation))

    # return the text without punctuation
    return no_punct_text