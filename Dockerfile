FROM python:3
ADD NewServer.py /
run pip install psycopg2
CMD [ "python", "./NewServer.py" ]
