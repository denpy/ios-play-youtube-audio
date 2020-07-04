#!python3
#
# Written by Den in 2020.
# https://github.com/denpy
#
# This script allows to play the audio of a video from Youtube in the background using the VLC app
#
import sys
import webbrowser

PYTHONISTA_APP_NAME = 'pythonista'
PYTO_APP_NAME = 'pyto'
PYTHON_IOS_APP_NAME = None

# Import needed module according to the Python app
script_name = sys.argv[0].lower()
if PYTHONISTA_APP_NAME in script_name:
	PYTHON_IOS_APP_NAME = PYTHONISTA_APP_NAME

	# Pythonista app builtin modules
	# noinspection PyUnresolvedReferences
	import appex
	# noinspection PyUnresolvedReferences
	import clipboard
	# noinspection PyUnresolvedReferences
	import notification
elif PYTO_APP_NAME in script_name:
	PYTHON_IOS_APP_NAME = {PYTO_APP_NAME}
	# Pyto app builtin module
	# noinspection PyUnresolvedReferences
	import xcallback
	# noinspection PyUnresolvedReferences
	import notifications
	# noinspection PyUnresolvedReferences
	import pasteboard
else:
	print(f'Looks like you have no {PYTHONISTA_APP_NAME.title()} or {PYTO_APP_NAME.title()} apps installed')
	sys.exit()

# Try to import the "youtube-dl", exit it failed
try:
	import youtube_dl
	from youtube_dl.utils import YoutubeDLError
except ImportError:
	print('Please, make sure that "youtube-dl" is installed')
	sys.exit()


def notify(msg):
	# Present the iOS notification banner
	if PYTHON_IOS_APP_NAME == PYTHONISTA_APP_NAME:
		# Pythonista
		notification.schedule(message=msg)
	else:
		# Pyto
		pn = notifications.Notification(message=msg)
		notifications.schedule_notification(pn)


def get_video_url():
	# Get text passed in the iOS share sheet or clipboard
	if PYTHON_IOS_APP_NAME == PYTHONISTA_APP_NAME:
		# Pythonista
		return appex.get_text() or clipboard.get()

	# Pyto
	return pasteboard.string()


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
		notify("Can't get video info 😱️")


def open_url_in_vlc(url):
	# Open the VLC app with the audio URL
	vlc_x_callback_url = f'vlc://{url}'
	if PYTHON_IOS_APP_NAME == PYTHONISTA_APP_NAME:
		# Pythonista
		webbrowser.open(vlc_x_callback_url)
	else:
		# Pyto
		xcallback.open_url(vlc_x_callback_url)


def main():
	video_url = get_video_url()

	# If YouTube URL is not provided notify about that and exit
	if video_url is None or 'https://youtu' not in video_url:
		notify('No YouTube URL provided 🤷🏾‍♂️')
		sys.exit()

	# Get audio only URL
	audio_url = get_audio_url(video_url)
	if audio_url is None:
		notify("Can't get video info 😱️")
		return

	# Open the audio URL in the VLC app for streaming
	open_url_in_vlc(audio_url)


if __name__ == '__main__':
	main()
