import os
from telethon import TelegramClient
from telethon.sessions import StringSession

try:
    os.mkdir('generated')
except FileExistsError:
    pass

api_id = int(input('Api id: '))
api_hash = input('Api hash: ')
phone = input('Телефон: ')
save_method = int(input('Файл или строка 1/2: '))
if save_method == 1:
    tg_client = TelegramClient(os.path.join('generated', str(api_id)), api_id=api_id, api_hash=api_hash)
elif save_method == 2:
    try:
        f = open(f'generated/{api_id}.txt', 'r')
        session = f.read()
        f.close()
    except FileNotFoundError:
        session = ''
    tg_client = TelegramClient(StringSession(session), api_id=api_id, api_hash=api_hash)
else:
    raise Exception('Неправельный метод сохранения сессии')


async def create():
    await tg_client.connect()
    if not await tg_client.is_user_authorized():
        await tg_client.send_code_request(phone)
        await tg_client.sign_in(phone, input('Код из сообщения: '))
        await tg_client.disconnect()
    else:
        raise Exception(f'сессия уже авторизованна, уберите файл {api_id}.session/{api_id}.txt из папки generated или'
                        ' введите другие авторизационные данные')


tg_client.loop.run_until_complete(create())

if save_method == 2:
    open(f'generated/{api_id}.txt', 'w').write(tg_client.session.save())
