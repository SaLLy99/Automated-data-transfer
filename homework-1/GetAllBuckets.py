import boto3

session = boto3.Session( 
         aws_access_key_id='access_key_id', 
         aws_secret_access_key='access_secret_accsess_key')
         
session = boto3.resource('s3')
def getAllBuckets():
    print ("Bucket names: ")
    for bucket in session.buckets.all():
       print (bucket.name+"\n")

def getCertainBuckets():
    for bucket in session.buckets.all():
        if bucket.name.startswith('prod'):
            print("Get prod bucket names:")   
            print(bucket.name);
          
        
def main():
    getAllBuckets()
    getCertainBuckets()


if __name__ == "__main__":
    main()