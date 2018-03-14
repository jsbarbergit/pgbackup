import pytest


#import our module that we want to test
from pgbackup import cli

URL = 'postgres://bob@example.com:5432/db_on'


# Maerk the following function as a pytest fixture func
# doesn't start with test_ so won't be run as a test
# tests can then be called with a function as a param to 
# instantiate the cli.create_parser() object
@pytest.fixture
def parser():
    # Instantiate an instance of the cli module create_parser function
    return cli.create_parser()

#Failing Path Tests
def test_parser_without_driver(parser):
    """
    Without a specified driver the parser will exit
    """
    # Instantiate an instance of the cli module create_parser function
    # !Not needed now using decorator function as a param to this func
    # parser = cli.create_parser()
    # Test will succeed if a System Exit is received from cli module
    with pytest.raises(SystemExit):
        # Pass it just a URL(db connection string) - should fail
        parser.parse_args([URL])

def test_parser_with_driver(parser):
    """
    The parser will exit if it receives a driver w/out a destination
    """
    # Test will succeed if a System Exit is received from cli module
    with pytest.raises(SystemExit):
        # Pass URL and driver but without 3rd opt of a dest path
        parser.parse_args([URL, '--driver', 'local'])

def test_parser_valid_driver(parser):
    """
    The parser will exit if driver is not local or s3
    """
    # Pass args with inavlid driver
    with pytest.raises(SystemExit) as err:
        args = parser.parse_args([URL, '--driver', 'invalid', '/some/test/path'])

#Happy Path Tests
def test_parser_with_driver_and_destination(parser):
    """
    The parser will not exit if it receives a driver and destination
    """
    # Pass args - function will return all args received
    args = parser.parse_args([URL, '--driver', 'local', '/some/test/path'])
    # Check/Assert that they are what we expect
    assert args.url == URL
    assert args.driver == 'local'
    assert args.destination == '/some/test/path'

def test_parser_with_valid_driver_types(parser):
    """
    Ensure parser accepts known valid drivers
    """
    valid_drivers = ['s3', 'local']
    for driver in valid_drivers:
        # Check for Truthy return
        assert parser.parse_args([URL, '--driver', driver, '/some/test/path'])
