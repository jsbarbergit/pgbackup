from time import strftime, localtime
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
    parser.add_argument('-d', '--driver',
            help=f'How and Where to Store the Backup.\nSupported Drivers: {VALID_DRIVERS}',
            required=True,
            nargs=2,
            metavar=('DRIVER', 'DESTINATION'),
            action=DriverAction)

    return parser

def main():
    import boto3
    from pgbackup import pgdump, storage

    args = create_parser().parse_args()
    timestamp = strftime('%Y-%m-%dT%H_%M_%S',localtime())
    dump = pgdump.dump(args.url)
    # driver validation done as part of the args parser already
    if args.driver == 's3':
        # Need a unique file name for S3 type- create timestamp
        timestamp = strftime('%Y-%m-%dT%H_%M_%S',localtime())
        # Call function to combine outfile name
        outfile = pgdump.dump_file_name(args.url, timestamp)
        client = boto3.client('s3')
        storage.s3(client, dump.stdout, args.destination, outfile)
        print(f'Successfully uploaded backup file to s3://{args.destination}/{outfile}')
    else:
        # For local storage Destination includes a filename
        outfile = open(args.destination, 'wb')
        storage.local(dump.stdout, outfile)
        print(f'Successfully wrote backup file to {args.destination}')
