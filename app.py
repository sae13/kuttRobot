from flask import Flask, jsonify
from flask import request
from config import KuttConfig
from validators import url as urlValidate
import logging

logging.basicConfig(filename='telegram.log',
                    level=logging.DEBUG,
                    format='%(asctime)-15s %(message)s'
                    )
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
    from telegram import Update, Message, InlineQueryResult, Bot, InlineKeyboardButton, InputTextMessageContent, \
        InlineQueryResultArticle, InlineKeyboardMarkup, ParseMode
    from kuttit import short_url
    try:
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
            short = short_url(message)

            repley_mark_up = [[InlineKeyboardButton(text='Open Url',
                                                    url=f"{short['link']}")],
                              # [InlineKeyboardButton(text='Bot Source ',
                              #                       url="https://github.com/sae13/kuttRobot")],
                              [InlineKeyboardButton(text='👤', url="https://t.me/saeb_m"),
                               InlineKeyboardButton(text='🌎', url="https://kutt.it/kuttRobot"),
                               # InlineKeyboardButton(text='📞', url="https://t.me/mesShahrbabak/17")
                               ]]

            bot.answerInlineQuery(inline_query_id=msg.inline_query.id, results=[InlineQueryResultArticle(
                reply_markup=InlineKeyboardMarkup(
                    repley_mark_up,
                    resize_keyboard=True),
                type='article',
                id=short['id'],
                title=short['address'],
                input_message_content=InputTextMessageContent(
                    f'{short["link"]}',
                    parse_mode=ParseMode.MARKDOWN,
                    disable_web_page_preview=False),
                thumb_url='https://kutt.it/sm748'
            ),

            ])
    except Exception as e:
        logging.error(e, exc_info=True)

    return 'ok'


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)
