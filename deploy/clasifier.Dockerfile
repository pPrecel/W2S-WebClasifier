FROM python

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD [ "gunicorn", "-w 4", "-b", "0.0.0.0:5050", "main:app" ]