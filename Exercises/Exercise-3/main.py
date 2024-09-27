import boto3
import gzip
import io

def download_s3_file_in_memory(bucket_name, key):
    """Download a file from S3 and return it in-memory."""
    s3_client = boto3.client('s3')
    s3_object = s3_client.get_object(Bucket=bucket_name, Key=key)
    return io.BytesIO(s3_object['Body'].read())  # Read the S3 object into a BytesIO stream.

def extract_first_line_from_gz(gz_data):
    """Extract and return the first line from a .gz file in memory."""
    with gzip.GzipFile(fileobj=gz_data, mode='rb') as gz_file:
        for line in gz_file:
            return line.decode('utf-8').strip()  # Return the first line as a decoded string.

def stream_and_print_s3_file(bucket_name, key):
    """Download a file from S3 and stream each line to stdout."""
    s3_client = boto3.client('s3')
    s3_object = s3_client.get_object(Bucket=bucket_name, Key=key)
    
    # Stream the file directly from S3 without loading it fully into memory
    for line in s3_object['Body'].iter_lines():
        print(line.decode('utf-8'))

def main():
    # Step 1: Download the gz file in-memory from the S3 bucket.
    bucket_name = 'commoncrawl'
    gz_key = 'crawl-data/CC-MAIN-2022-05/wet.paths.gz'
    gz_file_data = download_s3_file_in_memory(bucket_name, gz_key)

    # Step 2: Extract the gz file in memory and get the first line (file URI).
    first_file_uri = extract_first_line_from_gz(gz_file_data)
    print(f"First URI: {first_file_uri}")

    # Step 3: Download and stream the file from the first URI.
    # The first_file_uri will be something like: 'crawl-data/CC-MAIN-2022-05/segments/...'
    stream_and_print_s3_file(bucket_name, first_file_uri)

if __name__ == "__main__":
    main()