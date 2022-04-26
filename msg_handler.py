import asyncio
import configparser
import re
from telethon.errors import SessionPasswordNeededError
from telethon import TelegramClient, events, sync
from telethon.tl.functions.messages import (GetHistoryRequest)
from telethon.tl.types import (
PeerChannel
)
from datetime import datetime
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from db_config import *

from contextlib import contextmanager
##### credentials for login in telegram api app
api_id = 12754734
api_hash = '2c533fb2a03bb2e12239cae7eb12c921'

##### create an object of TelegramClient and connect to it
client = TelegramClient('freedom_ukraine', api_id, api_hash)
client.connect()

##### channel to fetch messages from
user_input_channel = 'https://t.me/ukrainianfreedomnews'


##### creating session for sqlalchemy
# Session = sessionmaker(engine)
# session = Session()
# inspector = inspect(engine)

@contextmanager
def session_scope():
        # self.db_engine = create_engine(self.db_config, pool_pre_ping=True,echo=True) # echo=True if needed to see background SQL        
    Session = sessionmaker(engine)
    session = Session()
    inspector = inspect(engine)
    try:
            # this is where the "work" happens!
        yield session
            # always commit changes!
        session.commit()
    except:
            # if any kind of exception occurs, rollback transaction
        session.rollback()
        raise
    finally:
        session.close()


@client.on(events.NewMessage(chats=user_input_channel))
async def newMessageListener(event):
	short = ''
	time = ''
	##### quantity of rows in table
	with session_scope() as session:
		rows = session.query(QuickNews).count()
		first_row = session.query(QuickNews).order_by('creation_time').all()

		if rows >= 30:
			session.query(QuickNews).filter(QuickNews.id==first_row[0].id).delete()
			session.commit()


	##### characters which are allowed to be in text
	whitelist = set('abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!?.,:;-""')
	short = event.message.text

	##### formatting message (one paragraph,ends with '.') and adding time field to db 
	if event.message.message != '':
		time  = str(event.message.date)
		time = time[11:16] + ', ' + time[8:10] + '.' + time[5:7]
		if len(''.join(filter(whitelist.__contains__, short))) <= 100:
			if short.count('\n') >= 1:
				print('aaaaaaaaaaaaaaaaaaaaaa')
				enter_n = short.find('\n')
				short = short[:enter_n]
			short = ''.join(filter(whitelist.__contains__, short))
			if short[0] == ' ':
				short = short[1:]
			if short[len(short)-1] == ' ':
				short = short[:len(short)-1]
			if short[len(short)-1] == ',':
				short = short[:len(short)-1]
			if short[len(short)-1] != '.' and short[len(short)-2] != '.' and short[len(short)-1] != '!' and short[len(short)-2] != '!' and short[len(short)-1] != '?' and short[len(short)-2] != '?':
				short = short + '.'
		else:
			if short.count('\n') >= 1:
				enter_n = short.find('\n')
				short = short[:enter_n]
			short = ''.join(filter(whitelist.__contains__, short))
			if short[0] == ' ':
				short = short[1:]
			if short[len(short)-1] == ' ':
				short = short[:len(short)-1]
			if short[len(short)-1] == ',':
				short = short[:len(short)-1]
			if short[len(short)-1] != '.':
				short = short + '.'

	# 	##### inserting data to table
	# 	##### QuickNews - name of model in db_config.py
		news = QuickNews(
			text = short,
			time = time,
			creation_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f") 
		  )
		with session_scope() as session:
			session.add(news)
			session.commit()
		##### send message to your favorites
		# await client.forward_messages(entity = 'me', messages = event.message)

##### make script running until stopped manually
with client:
	client.run_until_disconnected()