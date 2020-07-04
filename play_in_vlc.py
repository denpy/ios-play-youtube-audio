#!python3
#
# Written by Den in 2020.
# https://github.com/denpy
#
# Script version: 2020.1
# This script allows to play the audio of a video from Youtube in the background using the VLC app
#
import sys
import webbrowser

try:
	# Try to import Pythonista app builtin modules
	# noinspection PyUnresolvedReferences
	import appex
	# noinspection PyUnresolvedReferences
	import clipboard
	# noinspection PyUnresolvedReferences
	import notification

	# Bind function names
	get_share_sheet_content = appex.get_text
	get_clipboard = clipboard.get
	schedule_notification = notification.schedule
	open_url_in_vlc = webbrowser.open
except ImportError:
	try:
		# Try to import Pyto app builtin modules
		# noinspection PyUnresolvedReferences
		import xcallback
		# noinspection PyUnresolvedReferences
		import notifications
		# noinspection PyUnresolvedReferences
		import pasteboard


		def get_share_sheet_content():
			# Pyto does not have this functionality, so we do nothing
			pass

		def schedule_notification(msg):
			notification = notifications.Notification(message=msg)
			notifications.schedule_notificatio(notification)

		# Bind function/method names
		get_clipboard = pasteboard.string
		open_url_in_vlc = xcallback.open_url
	except ImportError:
		print(f'Looks like you have no Pythonista3 or Pyto apps installed 🤦🏽‍♂️')
		sys.exit()

try:
	# Try to import the "youtube-dl", exit if failed
	import youtube_dl
	from youtube_dl.utils import YoutubeDLError
except ImportError:
	print('Please, make sure that "youtube-dl" is installed 🤨')
	sys.exit()


def get_audio_url(video_url):
	# Try to get the video info as dict
	try:
		# Do not download the video and redirect log messages to stderr (we are not interested in these log messages)
		ydl_kwargs = dict(cachedir=False, logtostderr=True)
		with youtube_dl.YoutubeDL(ydl_kwargs) as ydl:
			video_info = ydl.extract_info(video_url, download=False)

		# Filter only the audio URL
		audio_url = [fmt['url'] for fmt in video_info['formats'] if fmt['ext'] == 'm4a'][0]
		return audio_url
	except (YoutubeDLError, IndexError, KeyError):
		schedule_notification('Failed to get video info 😱️')


def main():
	# Get text passed in iOS share sheet or clipboard
	video_url = get_share_sheet_content() or get_clipboard()

	# If YouTube URL is not provided notify about that and exit
	if video_url is None or 'https://youtu' not in video_url:
		schedule_notification('No YouTube URL provided 🤷🏾‍♂️')
		sys.exit()

	# Get audio URL only
	audio_url = get_audio_url(video_url)
	if audio_url is None:
		schedule_notification("No audio URL was found 😱️")
		return

	# Open the audio URL in the VLC app for streaming
	open_url_in_vlc(audio_url)


if __name__ == '__main__':
	main()
