from telethon import TelegramClient
from telethon.tl.types import *

from config import get_telegram_api_config
from db import get_db, Db

from logging import info
import logging

async def backup_message_batches(client: TelegramClient, db: Db, highest_message_id: int):
    batch_size = 100
    message_id_from = highest_message_id // batch_size * batch_size
    message_id_to = message_id_from + batch_size

    # don't mark as stored if this is the first batch
    is_first_batch = True

    info(f'Getting message backup statuses')
    statuses = db.get_all_message_backup_statuses()

    while message_id_from >= 0:
        if message_id_from == 0:
            message_id_from = 1

        info(f'Processing message batch {message_id_from} .. {message_id_to}')

        if db.is_message_backup_status_done_quick(statuses, message_id_from, message_id_to):
            info(f'Message batch {message_id_from} .. {message_id_to} has already been backed up')

        else:
            messages: list[Message] = [
                m async for m in client.iter_messages(None, ids=list(range(message_id_from, message_id_to)))
                if m is not None
            ]
            db.store_messages(messages)
            info(f'Message batch {message_id_from} .. {message_id_to}: stored {len(messages)} messages')

            if not is_first_batch:
                db.mark_message_backup_status_done(message_id_from, message_id_to)
                info(f'Message batch {message_id_from} .. {message_id_to} is marked as backed up')

        # prepare next!
        message_id_from -= batch_size
        message_id_to = message_id_from + batch_size

        is_first_batch = False


async def client_main(client: TelegramClient):
    me = await client.get_me()
    info(me.stringify())

    highest_message_id = None

    info('Finding highest known message id')

    message: Message
    async for message in client.iter_messages(''):
        if isinstance(message.peer_id, (PeerUser, PeerChat)):
            highest_message_id = message.id
            break

    if highest_message_id is None:
        info('Error: ran out of messages when finding highest message id')
        return

    info(f'Highest known message id: {highest_message_id}')

    info('Setting up database')
    db = get_db()
    db.on_create()

    await backup_message_batches(client, db, highest_message_id)
    info('End of client_main')


def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
    telegram_api_config = get_telegram_api_config()
    api_id = telegram_api_config.getint('id')
    api_hash = telegram_api_config['hash']

    with TelegramClient('.session/current', api_id, api_hash) as client:
        client.loop.run_until_complete(client_main(client))


main()
