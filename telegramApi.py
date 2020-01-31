def return_telethon_telegram_bot(filterim=True):
    from telethon import TelegramClient, connection
    from config import KuttConfig
    if not filterim:
        botConfig = TelegramClient(
            'kuttrobot',
            api_id=KuttConfig.tgApiId,
            api_hash=KuttConfig.tgApiHash,
        )
    else:
        botConfig = TelegramClient(
            'kuttrobot',
            api_id=KuttConfig.tgApiId,
            api_hash=KuttConfig.tgApiHash,
            connection=connection.ConnectionTcpMTProxyRandomizedIntermediate,
            proxy=('Rick.And.Morty.P2P.Giize.com', 443, 'dd00000000000000000000000000000000'))
    return botConfig.start(bot_token=KuttConfig.tgSecret)


def return_python_telegram_bot(filterim=True):

    from config import KuttConfig
    from telegram import Bot
    from telegram.utils.request import Request
    if filterim:
        return Bot(KuttConfig.tgSecret, request=Request(proxy_url=KuttConfig.proxy))
    return Bot(KuttConfig.tgSecret)
