import spacy
from dateutil import parser # for date parsing
import json # for request body
from tkinter import Tk, filedialog # for file dialog

from src.read_mapping_file import read_mapping_file
from src.text_preprocessing import delete_punctuation
from src.booleanFormulas import generate_boolean_formula

def file_selection_dialog():
    root = Tk()
    root.withdraw()
    default_dir = 'training_data'
    file_path = filedialog.askopenfilename(parent=root, initialdir=default_dir, title='Please select a file')
    return file_path


def find_model_code(doc,ModelTyp_file):
    # read the ModelTyp's keywords
    (ModelTyp_keywords, ModelTyp_mapping) = read_mapping_file(ModelTyp_file)

    # find the keywords of model in the user's prompt
    model_keyword = [keyword for chunk in doc.noun_chunks for keyword in ModelTyp_keywords if keyword in chunk.text]
    # find the correspongding code of the model
    model_code = [ModelTyp_mapping[keyword] for keyword in model_keyword]
    return model_code


def find_data(doc):
    '''find the date in the user's prompt'''
    for ent in doc.ents:
        if ent.label_ == 'DATE':
            # parse the date using datetime.strptime
            date_obj = parser.parse(ent.text, fuzzy=True)
            formatted_date = date_obj.strftime("%Y-%m-%d")
            return formatted_date


if __name__ == "__main__":
    # load the english model
    nlp = spacy.load("en_core_web_sm")
    nlp.add_pipe("sentencizer")

    # read the user's prompt
    file_path = file_selection_dialog()
    with open(file_path, "r") as f:
        text = f.read()

    # delete the punctuation from the user's prompt
    text = delete_punctuation(text)

    doc = nlp(text)

    #ModelTypCodes
    ModelTyp_file = 'file\modelTyp_mapping.csv'
    model_code = find_model_code(doc,ModelTyp_file)

    # find the transformed code of config
    config_code = generate_boolean_formula(doc)

    # extract the dates from the user's prompt
    formatted_date = find_data(doc)

    # create the request body
    Request_body = {
        "modelTypeCodes": [model_code], 
        "booleanFormulas": [config_code], 
        "dates": [formatted_date],
    }
    # convert the request body to json
    json_str = json.dumps(Request_body)

    # print the request body
    print(json_str)
