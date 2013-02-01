import re
import unicodedata


def slugify(value):
  value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore")
  value = unicode(re.sub("[^\w\s-]", "", value).strip().lower())
  value = re.sub("[-\s]+", "-", value)

  return value
