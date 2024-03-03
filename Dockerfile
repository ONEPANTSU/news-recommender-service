FROM python:3.10

WORKDIR /news_recommender_agent

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "run.py"]