from diary import app
from flask import request
from urlparse import urlparse, urljoin
import html2text
import re
import translitcodec

try:
  from PIL import Image
except:
  import Image

_punct_re = re.compile(r"[\t !\"#$%&'()*\-/<=>?@\[\\\]^_`{|},.]+")
internal = ["pages", "favicon.ico", "create", "delete", "login", "logout", "facebook", "diary"]


def slugify(text, delim=u"-"):
  """
  Generates an ASCII-only slug.
  """
  result = []
  for word in _punct_re.split(text.lower()):
    word = word.encode("translit/long")
    if word:
      result.append(word)
  my_slug = unicode(delim.join(result))[:64]
  if any(my_slug in s for s in internal):
    return "diary-%s" % my_slug
  else:
    return my_slug


def is_safe_url(target):
  """
  Check if URL is safe
  """
  ref_url = urlparse(request.host_url)
  test_url = urlparse(urljoin(request.host_url, target))
  return test_url.scheme in ("http", "https") and ref_url.netloc == test_url.netloc


def get_redirect_target():
  for target in request.args.get("next"), request.referrer:
    if not target:
      continue
    if is_safe_url(target):
      return target


def allowed_file(filename):
  return '.' in filename and filename.rsplit('.', 1)[1] in app.config["ALLOWED_EXTENSIONS"]


def generate_thumb(source, target, box, fit=True):
  """
  Downsample the image.

  @param source: string - path to the image
  @param target: string - path to the save the thumbnail-image
  @param box:    tuple(x, y) - the bounding box of the result image
  @param fit:    boolean - crop the image to fill the box
  """
  if source:
    img = Image.open(source)

    # preresize image with factor 2, 4, 8 and fast algorithm
    factor = 1
    while img.size[0] / factor > 2 * box[0] and img.size[1] * 2 / factor > 2 * box[1]:
      factor *= 2
    if factor > 1:
      img.thumbnail((img.size[0] / factor, img.size[1] / factor), Image.NEAREST)

    # calculate the cropping box and get the cropped part
    if fit:
      x1 = y1 = 0
      x2, y2 = img.size
      wRatio = 1.0 * x2 / box[0]
      hRatio = 1.0 * y2 / box[1]
      if hRatio > wRatio:
        y1 = int(y2 / 2 - box[1] * wRatio / 2)
        y2 = int(y2 / 2 + box[1] * wRatio / 2)
      else:
        x1 = int(x2 / 2 - box[0] * hRatio / 2)
        x2 = int(x2 / 2 + box[0] * hRatio / 2)
      img = img.crop((x1, y1, x2, y2))

    # resize the image with best quality algorithm ANTI-ALIAS
    img.thumbnail(box, Image.ANTIALIAS)
    img.save(target)

    return target


def cleanup(input):
  h = html2text.HTML2Text()
  h.ignore_links = True
  return h.handle(input).replace(u'&nbsp_place_holder;', u' ')
