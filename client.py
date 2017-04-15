# -*- coding: utf-8 -*-
from irc3.plugins.command import command
import irc3
import socket
from pathlib import Path
from random import randint


@irc3.plugin
class ClientPlugin:
	requires = [
		'irc3.plugins.core',
		'irc3.plugins.userlist',
		'irc3.plugins.command',
		'irc3.plugins.human',
	]

	def __init__(self, bot):
		self.bot = bot
		self.log = self.bot.log

	def connection_made(self):
		"""triggered when connection is up"""

	def server_ready(self):
		"""triggered after the server sent the MOTD (require core plugin)"""

	def connection_lost(self):
		"""triggered when connection is lost"""

	@irc3.event(irc3.rfc.JOIN)
	def welcome(self, mask, channel, **kw):
		"""Welcome people who join a channel"""
		if mask.nick != self.bot.nick:
			self.bot.call_with_human_delay(
				self.bot.privmsg, channel, 'Welcome %s!' % mask.nick)
		else:
			self.bot.call_with_human_delay(
				self.bot.privmsg, channel, "Hi guys!")

	@irc3.event(irc3.rfc.ERR_NICKNAMEINUSE)
	def rename(self, srv=None, me=None, nick=None, data=None):
		self.bot.nick += str(randint(0, 9))

	@command
	def echo(self, mask, target, args):
		"""Echo command
			%%echo <words>...
		"""
		self.bot.privmsg(mask.nick, ' '.join(args['<words>']))

	@command
	def say(self, mask, target, args):
		"""Say command
			%%say <message>...
		"""
		yield ' '.join(args['<message>'])

	@command
	def pwd(self, mask, target, args):
		"""Echo working directory
			%%pwd [<directory>...]
		"""
		def print_dir(paths):
			for p in paths:
				yield str(Path(p).resolve())
		directories = args['<directory>'] or ['.']
		for path in print_dir(directories):
			yield path

	@command
	def ls(self, mask, target, args):
		"""ls a directory
			%%ls [<directory>...]
		"""
		def list_contents(paths):
			for p in paths:
				d = Path(p)
				yield str(d.resolve())
				yield ' ' + ' | '.join(f.name for f in d.iterdir())
		directories = args['<directory>'] or ['.']
		for content in list_contents(directories):
			yield content

	@command
	def stats(self, mask, target, args):
		"""Show stats of the channel using the userlist plugin
			%%stats [<channel>]
		"""
		if args['<channel>']:
			channel = args['<channel>']
			target = mask.nick
		else:
			channel = target
		if channel in self.bot.channels:
			channel = self.bot.channels[channel]
			message = '{0} users'.format(len(channel))
			for mode, nicknames in sorted(channel.modes.items()):
				message += ' - {0}({1})'.format(mode, len(nicknames))
			self.bot.privmsg(target, message)


def main(ip):
	name = 'BOT_' + socket.gethostname().replace('.', '_')
	config = {
		'nick':         name,
		'username':     name,
		'autojoins':    ['#main'],
		'host':         ip,
		'port':         6667,
		'ssl':          False,
		'includes':     [
			'irc3.plugins.core',
			'irc3.plugins.command',
			'irc3.plugins.human',
			__name__
		]
	}
	bot = irc3.IrcBot.from_config(config)
	bot.run(forever=True)

if __name__ == '__main__':
	import os
	main(os.environ.get('IP'))
