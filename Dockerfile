FROM python:3.13
WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src/ .
CMD [ "python", "./mylisp.py" ]