from flask import Flask, jsonify
from flask import request
from config import KuttConfig
from validators import url as urlValidate
from uuid import uuid4
preUrlv1 = KuttConfig.v1preUrl
app = Flask(__name__)


@app.route('/')
def index():
    return 'saeb on live dot com!'


@app.route(f'{preUrlv1}{KuttConfig.tgSecret}', methods=['POST', 'GET'])
def bot():
    request.args
    return 'hello saeb'


@app.route(f'{preUrlv1}/set-webhook')
def set_webhook():
    from telegramApi import return_python_telegram_bot
    bot = return_python_telegram_bot(KuttConfig.filterim)
    isSet = bot.setWebhook(f'{KuttConfig.tgWebhookUrl}'
                           f'{KuttConfig.v1preUrl}'
                           f'/{KuttConfig.tgSecret}')
    if isSet:
        return jsonify({'status': 'ok'})
    return jsonify({'status': 'failed'})


@app.route(f'{preUrlv1}/{KuttConfig.tgSecret}', methods=['POST'])
def telegram():
    from telegramApi import return_python_telegram_bot
    from telegram import Update, Message, InlineQueryResult,Bot
    from kuttit import short_url
    bot: Bot = return_python_telegram_bot(KuttConfig.filterim)
    msg = Update.de_json(request.get_json(force=True), bot)
    if msg.message is not None:
        message: Message = msg.effective_message
        for e in message.parse_entities('url'):
            url = message.parse_entity(e)
            msgForSend = f'short url for \n{url}\n is :\n{short_url(url)}'
            message.reply_text(msgForSend)
    if msg.inline_query is not None:
        message = msg.inline_query.query
        if not urlValidate(message): return 'ok'

        bot.answerInlineQuery(results=[InlineQueryResult()])
    return 'ok'
