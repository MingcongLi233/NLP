***Description***
The purpose of this program is to take unstructured prompts written by the user and convert them into a request body:
{
  "modelTypeCodes": ["8G32"],
  "booleanFormulas": ["+(S205A / S2TBA)+S609A+LL"],
  "dates": ["2019-04-01"]
}


***environment***
python 3.9.1
spacy 3.5.2


***How to use***
In the folder where the program is located,run the program by typing:
 "python main.py" 
 in the terminal. The program will prompt you to choose an input text and will print out the request body.


***What to do next***
---The program is not able to handle the case where the user inputs a prompt that contains multiple model types.
---The program is not able to handle the multiple date types.

