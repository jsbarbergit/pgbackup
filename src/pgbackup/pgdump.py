import subprocess
import sys
from time import strftime, localtime

def dump(url):
    try:
        return subprocess.Popen(['pg_dump', url], stdout=subprocess.PIPE)
    # Catch OSError which will catch pg_dump not being installed
    except OSError as err:
        print(f'Error: {err}')
        sys.exit(1)

# Return a file name for the DB backup
# Optionally with a timestamp
def dump_file_name(url, timestamp=None):
    # from format of url, last field split on / will be db
    dbname = url.split('/')[-1]
    # As this is a url it could have query params after dbname - split
    dbname = dbname.split('?')[0]
    # None is a Falsy type - so if true - timestamp has been set
    if timestamp:
        return dbname + '_' + timestamp.replace(':', '_') + '.sql'
    else:
        return dbname +'.sql'

