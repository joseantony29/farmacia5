import os
from django.conf import settings

def link_callback(uri, rel):
	static_url = settings.STATIC_URL  # Typically /static/
	static_root = settings.STATIC_ROOT  # Typically /home/userX/project_static/
	media_url = settings.MEDIA_URL  # Typically /static/media/
	media_root = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

	if uri.startswith(media_url):
		path = os.path.join(media_root, uri.replace(media_url, ""))
	elif uri.startswith(static_url):
		path = os.path.join(static_root, uri.replace(static_url, ""))
	else:
		return uri

	if not os.path.isfile(path):
		raise Exception(f"Media URI must start with {static_url} or {media_url}")

	return path