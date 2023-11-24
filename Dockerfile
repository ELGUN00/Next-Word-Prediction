FROM python:3.7.4

WORKDIR /next_word_prediction

COPY . .

# RUN pip install --no-cache-dir -r req.txt
RUN pip install torch
RUN pip install torchtext
RUN pip install pandas
RUN pip install numpy
RUN pip install fastapi
RUN pip install uvicorn
RUN pip install streamlit

