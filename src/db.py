import mysql.connector
from mysql.connector.connection import MySQLConnection
from telethon.tl.types import *

from config import get_db_config

db_config = get_db_config()

mydb = mysql.connector.connect(
    host=db_config['host'],
    port=db_config.getint('port'),
    user=db_config['user'],
    password=db_config['password'],
    database=db_config['database'],
)


class Db:
    db: MySQLConnection

    def __init__(self, db):
        self.db = db

    def on_create(self):
        with self.db.cursor() as c:
            with open('schema/mysql_1.sql', 'r', encoding='utf8') as f:
                sql = f.read()
                c.execute(sql, multi=True)
                print(sql)

    def mark_message_backup_status_done(self, message_id_from: int, message_id_to: int):
        self.db.reconnect()
        with self.db.cursor() as c:
            c.execute(
                'INSERT INTO MessageBackupStatus(message_id_from, message_id_to, done_time) '
                'VALUES(%s, %s, UTC_TIMESTAMP())',
                (message_id_from, message_id_to)
            )
        self.db.commit()

    def is_message_backup_status_done(self, message_id_from: int, message_id_to: int):
        self.db.reconnect()
        with self.db.cursor() as c:
            c.execute(
                'SELECT done_time FROM MessageBackupStatus WHERE message_id_from=%s AND message_id_to=%s',
                (message_id_from, message_id_to)
            )
            return c.fetchone() is not None

    def store_message(self, message: Message):
        peer_user_id = None
        peer_chat_id = None

        if isinstance(message.peer_id, PeerUser):
            peer_user_id = message.peer_id.user_id

        if isinstance(message.peer_id, PeerChat):
            peer_chat_id = message.peer_id.chat_id

        with self.db.cursor() as c:
            c.execute(
                'REPLACE INTO Message(id, message, peer_user_id, peer_chat_id, `date`, `out`, json_dump, backup_time) '
                'VALUES(%s, %s, %s, %s, %s, %s, %s, UTC_TIMESTAMP()) ',
                (message.id, message.message, peer_user_id, peer_chat_id, message.date, message.out, message.to_json())
            )


def get_db() -> Db:
    return Db(mydb)
