import pytest
import subprocess
from pgbackup import pgdump


URL = "postgres://bob:password@example.com:5432/db_one"

def test_dump_calls_pgdump(mocker):
    """
    Utilize pg_dump with database url
    """
    # Stub a subprocess.Popen call - nonblocking sub process
    # Our test should not be concerned with Popen - just our code
    mocker.patch('subprocess.Popen')
    # Test for a truthy value
    assert pgdump.dump(URL)
    subprocess.Popen.assert_called_with(['pg_dump', URL], stdout=subprocess.PIPE)

def test_dump_handles_os_error(mocker):
    """
    pgdump.dump resturns a reasonable error if pg_dump not installed
    """
    mocker.patch('subprocess.Popen', side_effect=OSError('no such file'))
    with pytest.raises(SystemExit):
        pgdump.dump(URL)
