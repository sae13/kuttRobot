def short_url(url):
    import validators
    from time import time
    from config import KuttConfig
    from json import dumps, loads
    from requests import post
    assert validators.url(url)
    sub = -3
    rand_int = int(str(int(time()))[sub:])
    header = {"X-API-KEY": KuttConfig.kuttItApi,
              "Content-Type": "application/json"}
    respStatus = 500
    tries = 0;
    while respStatus >= 300:
        body = {
            "target": url,
            "customurl": f'sm{rand_int + 1}',
        }
        tries += 1
        if tries > 4: del body['customurl']
        resp = post(KuttConfig.kuttItUrl, data=dumps(body), headers=header)
        sub = -5
        rand_int = int(str(int(time()))[sub:])
        respStatus = resp.status_code

    return loads(resp.content)['link']
