from urlparse import urlparse, urljoin
from flask import request
import re
import translitcodec

_punct_re = re.compile(r"[\t !\"#$%&'()*\-/<=>?@\[\\\]^_`{|},.]+")


def slugify(text, delim=u"-"):
  """
  Generates an ASCII-only slug.
  """
  result = []
  for word in _punct_re.split(text.lower()):
    word = word.encode("translit/long")
    if word:
        result.append(word)
  return unicode(delim.join(result))[:64]


def is_safe_url(target):
  """
  Check if URL is safe
  """
  ref_url = urlparse(request.host_url)
  test_url = urlparse(urljoin(request.host_url, target))
  return test_url.scheme in ("http", "https") and \
         ref_url.netloc == test_url.netloc


def get_redirect_target():
  for target in request.args.get("next"), request.referrer:
    if not target:
      continue
    if is_safe_url(target):
      return target
