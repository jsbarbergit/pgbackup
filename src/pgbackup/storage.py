def local(infile, outfile):
    outfile.write(infile.read())
    outfile.close()
    infile.close()

def s3(client, infile, bucket, outfile):
    client.upload_fileobj(infile, bucket, outfile)
