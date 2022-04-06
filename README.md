# homeworks
This is for homework only

First homework:
  
1)Prints existed bucketlist and also the  bucket which starts with 'Prod',
run following file 'get_all_buckets.py'  to see result.

Second homework:
  
1)it creates new bucket if we already have similar bucket then it will print
  'bucket already exists', please run 'create_bucket.py' to see result.

2)Checks if we have policy on certain bucket and if we don't have then it will 
create new one for it,please run 'create_policy.py' to see result/

3)Checks if we have certain bucket and if we have, it will delete it,
otherwise it will print that bucket doesn't exist, please see 'check_bucket.py' to see result.


Third homework:

1)Uploads file into certain bucket , in order to see result please run 'upload_file_to_bucket.py' file

2)Deletes file from certain bucket, in order to see result, please run 'delete_file_from_bucket.py' file

3)Download's certain file from bucket to the local directory, please run 'download_file.py' to see result

4)Lists extension of files and their amount order from certain bucket, please run 'list_bucket_by_file_type.py' file to see result

5)Replaces last version of file with previous version, please run 'determine_file_version.py' to see result


Fourth homework:

1)Create new bucket, in order to see result , please run 'create_bucket.py' from terminal in this way:
python create_bucket.py --bucket=demo2.test.com

2)Attach new policy to our bucket, in order to see result , please run 'attach_policy py' from terminal in this way:
python attach_policy.py --bucket=demo2.test.com

3)Make configuration for public static website and prints website url, in order to see result , please run 'set_website_config.py' from terminal
in this way:python set_website_config.py --bucket=demo2.test.com

4)Upload content to our bucket, in order to see result, please run 'upload_website.py' from terminal in this way:
python upload_website.py --bucket=demo2.test.com --dir=website