import subprocess
import sys

def dump(url):
    try:
        return subprocess.Popen(['pg_dump', url], stdout=subprocess.PIPE)
    # Catch OSError which will catch pg_dump not being installed
    except OSError as err:
        print(f'Error: {err}')
        sys.exit(1)
