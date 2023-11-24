from fastapi import FastAPI
from backend import utils


utils = utils.Utils()
app = FastAPI()


@app.get("/predict/{text}")
def predict(text: str):
    print(text)
    next_word = utils.predict_next_word(str_original=text)
    return {'next_word':next_word}