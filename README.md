# 📰 News Recommender Service

## 📖 Description:
The REST API for getting filtered news by category. It parses a news-site and sends gRPC requests to the [**news-classifier-service**](https://github.com/ONEPANTSU/news-classifier-service) for texts classifying.

Now there is only 1 news resource to parse (`src/parser/lernta_parser.py`). If you want to extend it just inherit **BaseParser** class with implementation of **_get_news_from_page** method.

## ▶️ Run:
Before running you have to create an `.env` file according to the sample (`.env-sample`).
```
docker-compose build
docker-compose up
```