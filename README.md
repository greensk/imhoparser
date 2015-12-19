imhoparser
==========

Утилита для извлечения данных профиля с сайта imhonet.ru и сохранения их в формате JSON.

## Использование

Для извлечения данных введите:

	./imhoparser.py username > mydata.json

Где username — имя профиля на сайте imhonet.ru.

## Формат выводимых данных

	{
		"books": [
			{
				"content": {
					"authors": "Лев Толстой",
					"genre": [
						"Проза XIX-XX веков"
					],
					"link": "http://books.imhonet.ru/element/169253/",
					"title": "Воскресение"
				},
				"info": [
					"Оценил 20 августа"
				],
				"rate": 10
			},
			...
		],
		"films" : [
			{
				"content": {
					"origin": "США, 2006 год",
					"link": "http://films.imhonet.ru/element/187576/",
					"title": "V значит Вендетта"
				},
				"info": [
					"Оценил 30 августа 2012"
				],
				"rate": 8
			},
			...
		]
	}
