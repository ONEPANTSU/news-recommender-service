from enum import Enum


class Category(str, Enum):
    CRIME = "Криминал"
    CULTURE = "Культура"
    ECONOMY = "Экономика"
    INCIDENT = "Происшествие"
    POLITICS = "Политика"
    SCIENCE = "Наука"
    SHOW = "Шоу-бизнес"
    SOCIETY = "Общество"
    SPORT = "Спорт"
    TRANSPORT = "Транспорт"
    WAR = "Вооружённый конфликт"
    WEATHER = "Погода"
