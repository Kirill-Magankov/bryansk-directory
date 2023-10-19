from app.api.model.neighborhood import NeighborhoodModel
from app.api.model.place import PlaceModel
from app.api.model.place_type import PlaceTypeModel
from app.api.model.user import UserModel
from app.db import db
from app.utils.security_utils import password_hash_generate


def preload_data():
    try:
        db.create_all()

        users = [
            UserModel('admin', password_hash_generate('admin')),
            UserModel('developer', password_hash_generate('developer')),
        ]

        neighborhoods = [
            NeighborhoodModel('Бежицкий'),  # 0
            NeighborhoodModel('Советский'),  # 1
            NeighborhoodModel('Фокинский'),  # 2
            NeighborhoodModel('Володарский'),  # 3
        ]

        place_types = [
            PlaceTypeModel('ТРЦ'),  # 0
            PlaceTypeModel('Кафе'),  # 1
            PlaceTypeModel('Рестораны'),  # 2
            PlaceTypeModel('ДК'),  # 3
            PlaceTypeModel('Музеи'),  # 4
        ]

        db.session.add_all(users)
        db.session.add_all(neighborhoods)
        db.session.add_all(place_types)
        db.session.flush()

        places = [
            _create_place(model=PlaceModel('Аэропарк', 'Объездная ул.,30', grade=4.7),  # noqa
                          type_=place_types[0], neighborhood=neighborhoods[1]),
            _create_place(model=PlaceModel('Бум сити', 'ул. 3 Интернационала, 8', grade=4.4),  # noqa
                          type_=place_types[0], neighborhood=neighborhoods[0]),
            _create_place(model=PlaceModel('Весна', 'ул. 3 Интернационала, 17А', grade=4.3),  # noqa
                          type_=place_types[0], neighborhood=neighborhoods[0]),

            _create_place(model=PlaceModel('Щебетун', 'ул. Фокина, 22', grade=5.0, phone_number='89006940660'),  # noqa
                          type_=place_types[1], neighborhood=neighborhoods[1]),

            _create_place(model=PlaceModel('Seven', 'пл. Карла Маркса, 7', grade=4.5),  # noqa
                          type_=place_types[2], neighborhood=neighborhoods[1]),
            _create_place(model=PlaceModel('Понтиле', 'ул. Фокина, 27/43', grade=4.9, phone_number='84832741752'), # noqa
                          type_=place_types[2], neighborhood=neighborhoods[1]),

            _create_place(model=PlaceModel('ДК БМЗ', 'ул. Майской Стачки, 6', grade=5.0),  # noqa
                          type_=place_types[3], neighborhood=neighborhoods[0]),

            _create_place(model=PlaceModel('Музей братьев Ткачёвых', 'ул. Куйбешева, 2', grade=4.5),  # noqa
                          type_=place_types[4], neighborhood=neighborhoods[0]),

            _create_place(model=PlaceModel('Художественный музей', 'ул. Ермлютина, 39', grade=4.3),  # noqa
                          type_=place_types[4], neighborhood=neighborhoods[1]),
        ]
        db.session.add_all(places)
        db.session.commit()
        print('Preload data successfully loaded')

    except Exception as e:
        print('Unexpected error.\nError: %s' % e)


def _create_place(model, type_, neighborhood):
    model.place_type = type_
    model.neighborhood = neighborhood
    return model
