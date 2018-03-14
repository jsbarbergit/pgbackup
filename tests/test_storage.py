import pytest
import tempfile

from pgbackup import storage


@pytest.fixture
def infile():
    # by default TemporaryFile opens in w+b - write and byte mode
    # Temp file will be deleted when done
    f = tempfile.TemporaryFile()
    # Write a byte sequence to the tempfile
    f.write(b'Testing')
    # Return pointer to start of file after writing
    f.seek(0)
    return f

# Use infile as a decortator function to aid reuse
def test_storing_file_locallyin(infile):
    """
    Write content from 1 file-like to another
    file-like as opposed to file as we're working with subprocess.Popen PIPE object
    which is file-like as is the tempfile used in these tests
    """
    # Create a non deleted temp file with a name for future reference
    outfile = tempfile.NamedTemporaryFile(delete=False)
    # Invoke our function with a file-like object and make sure it gets written
    # Testing that the stdout.PIPE dump object can be written to a file-like object
    storage.local(infile, outfile)
    with open(outfile.name, 'rb') as f:
        assert f.read() == b'Testing'


def test_s3_storage(mocker, infile):
    """
    Write content to S3
    """
    # Create a new mocked object
    client = mocker.Mock()

    storage.s3(client, infile, 'bucket_name', 'file_name')
    # upload_fileobj is the boto3 s3 upload_fileobj method we are mocking
    # upload_fileobj() is used for file-like objects. upload_file() is used for actual files
    # note that there is no dependency on boto3 though in our test :-)
    client.upload_fileobj.assert_called_with(infile, 'bucket_name', 'file_name')
    
