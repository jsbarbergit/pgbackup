from argparse import ArgumentParser, Action, ArgumentTypeError

VALID_DRIVERS=['s3', 'local']

# Custom class for parsing --driver args
class DriverAction(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        driver, destination = values
        if driver.lower() in VALID_DRIVERS:
            namespace.driver = driver.lower()
            namespace.destination = destination
        else:
            parser.error(f'Inavlid Driver. Valid Drivers are {VALID_DRIVERS}')

def create_parser():
    parser = ArgumentParser()
    parser.add_argument('url', help='URL of PostgreSQL DB to Backup')
    # --driver flag must pass 2 args and is required
    # custom subclass used for action to parse the 2 args into sep vars
    parser.add_argument('--driver',
            help='How and Where to Store the Backup',
            required=True,
            nargs=2,
            action=DriverAction)

    return parser

