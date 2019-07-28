import json

from os.path import *
from datetime import *
from xattr import *


#####################################################################################################################


def xattr_metadata(file):
  Log("[FILE] %s" % file)

  # try xattr
  metadata = getxattr(file, 'net.filebot.metadata')

  # try plain file xattr store
  if metadata is None:
    metadata = getxattr_plain_file('.xattr', file, 'net.filebot.metadata')

  Log("[XATTR] %s" % metadata)
  if metadata is not None:
    return json.loads(metadata)
  else:
    return None


def getxattr_plain_file(store, file, name):
  if not isabs(store):
    store = join(dirname(file), store)

  xattr_file = join(store, basename(file), name)

  if not isfile(xattr_file):
    return None

  Log("[STORE] %s" % xattr_file)

  fd = open(xattr_file, "rb")
  buffer = fd.read()
  fd.close()
  return buffer.decode('UTF-8')


#####################################################################################################################


def movie_id(attr):
  imdb_id = attr['imdbId']
  if imdb_id > 0:
    imdb_id = "tt%07d" % imdb_id
    Log("[IMDB] %s" % imdb_id)
    return imdb_id

  tmdb_id = attr['tmdbId']
  if tmdb_id > 0:
    tmdb_id = str(tmdb_id)
    Log("[TMDB] %s" % tmdb_id)
    return tmdb_id

  return None


def movie_guid(attr):
  imdb_id = attr['imdbId']
  if imdb_id > 0:
    guid = "tt%07d" % imdb_id
    Log("[GUID] %s" % guid)
    return guid

  tmdb_id = attr['tmdbId']
  if tmdb_id > 0:
    guid = "com.plexapp.agents.themoviedb://%s?lang=%s" % (tmdb_id, movie_language(attr))
    Log("[GUID] %s" % guid)
    return guid


def movie_name(attr):     return attr.get('name')
def movie_year(attr):     return attr.get('year')
def movie_language(attr): return attr.get('language')


#####################################################################################################################


def tvdb_series_id(attr):
  if attr_get(attr, 'seriesInfo', 'database') == 'TheTVDB':
    id = attr_get(attr, 'seriesInfo', 'id')
    Log("[TheTVDB] %s" % id)
    return str(id)

  return None


def series_guid(attr):
  series_id = attr_get(attr, 'seriesInfo', 'id')
  if series_id > 0:
    db = attr_get(attr, 'seriesInfo', 'database')
    if db == 'TheTVDB':
      guid = "com.plexapp.agents.thetvdb://%s?lang=%s" % (series_id, series_language(attr))
    else:
      guid = "%s::%s" % (db, series_id)

    Log("[GUID] %s" % guid)
    return guid

  return None


def series_name(attr): return attr_get(attr, 'seriesName')
def series_year(attr): return attr_get(attr, 'seriesInfo', 'startDate', 'year')


def series_language(attr):      return attr_get(attr, 'seriesInfo', 'language')
def series_date(attr):          return attr_date(attr_get(attr, 'seriesInfo', 'startDate'))
def series_certification(attr): return attr_get(attr, 'seriesInfo', 'certification')
def series_network(attr):       return attr_get(attr, 'seriesInfo', 'network')
def series_runtime(attr):       return attr_get(attr, 'seriesInfo', 'runtime')
def series_rating(attr):        return attr_get(attr, 'seriesInfo', 'rating')
def series_genres(attr):        return attr_get(attr, 'seriesInfo', 'genres')


def episode_title(attr):           return attr.get('title')
def episode_absolute_number(attr): return attr.get('absolute')
def episode_date(attr):            return attr_date(attr_get(attr, 'airdate'))


def attr_get(attr, *keys):
  for k in keys:
    attr = attr.get(k)
    if attr is None:
      return None
  return attr


def attr_date(attr):
  if attr is not None:
    return datetime(year=attr['year'], month=attr['month'], day=attr['day'])
  return None
