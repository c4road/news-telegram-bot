FROM python:3.9

COPY . /app/telegram-bot

WORKDIR /app/telegram-bot

RUN pip install -r requirements.txt
RUN pip install -r requirements-dev.txt

CMD ["python", "bot.py"]