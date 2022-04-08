import boto3


session = boto3.resource('s3')


def get_all_buckets():
    print("Bucket names: ")
    for bucket in session.buckets.all():
        print(bucket.name + "\n")


def get_certain_buckets():
    for bucket in session.buckets.all():
        if bucket.name.startswith('prod'):
            print("Get prod bucket names:")
            print(bucket.name);


def main():
    get_all_buckets()
    get_certain_buckets()


if __name__ == "__main__":
    main()
