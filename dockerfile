FROM python:alpine3.7

RUN adduser -D app

WORKDIR /home/app

ADD . .

RUN pip install pipenv
RUN pip install gunicorn
RUN pipenv install --system --deploy

ENV FLASK_APP service.py

RUN chown -R app:app ./ 
USER app

EXPOSE 8085
CMD ["gunicorn", "-b", ":8085", "--access-logfile", "-", "--error-logfile", "-", "wsgi:app"]