
class DatabaseConfig(object):
    dbhost = 'localhost'
    dbuser = 'root'
    dbpassword = 'Sk!pper2605'
    dbname = 'civil_crime_database'


class Config(object):
    PORT = 5000
    DEBUG = True
    threaded = True


class DevelopmentConfig(object):
    ENV='development'
    DEVELOPMENT = True
    DEBUG = True