user_db = {}

user_dict_template = {
    'locations': {
        'Уфа': (54.7431, 55.9678),
        'second': (22.7431, 22.9678),
    },
    'flag_daily_forecast': False,
    'flag_weekly_forecast': False,
    'default_location': 'Уфа',
    # Здесь значение False указывает, что по умолчанию выбрана точка default_location, а True — что будет запрашиваться геопозиция
    'flag_default_location': False,
}
