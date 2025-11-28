build-lambda-zip:
	pip install -r requirements.txt -t package/
	cd package && zip -r9 ../function.zip .
	zip -g function.zip lambda_function.py message.py scrapper.py telegram_bot.py bible_profecy_map.json .env