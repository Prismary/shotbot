import discord
import asyncio
import random
import string
import datetime
import time
import os
import time
import yaml

with open('config.yml', 'r') as cfgfile:
	config = yaml.load(cfgfile, Loader=yaml.FullLoader)
discord_token = config['tokens']['discord']['discord_token']
stop_code = config['stop_code']
default_host = config['default_host']

client = discord.Client()

def pf(preftype='t'):
	currenttime = str(datetime.datetime.now())[11:19]
	if preftype == 'rt':
		return currenttime
	elif preftype == 't':
		return '['+currenttime+'] '
	elif preftype == 'i':
		return '['+currenttime+'/Info] '
	elif preftype == 'e':
		return '['+currenttime+'/ERROR] '
	else:
		return '['+currenttime+'/'+preftype+'] '

async def send(channel, msg, type='default'):
	if type == 'cmd_i':
		msg = '`'+pf('i')+msg+'`'
	elif type == 'cmd_e':
		msg = '`'+pf('e')+msg+'`'
	elif type == 'cmd_t':
		msg = '`'+pf('t')+msg+'`'
	await channel.send(msg)

def get_url(type):
	if type == 'lightshot':
		url = 'https://prnt.sc/'
		for i in range(0, 2):
			url += random.choice(string.ascii_lowercase)
		for i in range(0, 4):
			url += str(random.randrange(0, 10))
	else:
		url = 'Unknown image host: ' + type
	return url

def process(message):
	mcl = message.content.lower()

	if mcl.startswith('+sc'):
		try:
			type = mcl.split(' ')[1]
		except:
			type = default_host

	return get_url(type)

@client.event
async def on_message(message):
	channel = message.channel
	mcl = message.content.lower()
	try:
		print(pf('Log')+str(message.author)+': '+message.content)
	except:
		print(pf('Log')+'[!]: Log failed due to unicode error.')
	if message.author == client.user:
		return
	global whitelist

	if mcl.startswith('sb.'):
		cmd = mcl.split(' ')[0]

		# Technical commands
		if cmd == 'sb.stop':
			try:
				if message.content.split(' ')[1] == stop_code:
					await send(channel, 'Client logout called.', 'cmd_i')
					await client.close()
				else:
					await send(channel, 'Invalid command.', 'cmd_e')
			except:
				await send(channel, 'Invalid command.', 'cmd_e')
		elif cmd == 'sb.ping':
			await send(channel, 'Pong!', 'cmd_i')
		elif cmd == 'sb.i':
			print(pf('i')+'Message ignored.')
		elif cmd == 'sb.api':
			await send(channel, discord.__version__, 'cmd_i')
		elif cmd == 'sb.cid':
			await send(channel, str(message.channel.id), 'cmd_i')
		elif cmd == 'sb.uid':
			await send(channel, str(message.author.id), 'cmd_i')
		else:
			await send(channel, 'Invalid command.', 'cmd_e')

	elif message.content.startswith('+'):
		await send(channel, process(message))

@client.event
async def on_ready():
	print(pf('i')+'> Username: '+client.user.name+'\n'+pf('i')+'> User-ID: '+str(client.user.id))
	print(pf('DONE')+'Shotbot ready!\n')

print(pf('HELLO!')+'Shotbot starting up!')
print(pf('i')+'Logging into Discord...')
client.run(discord_token)
