Homework 5

1) First of all run file 'create_lambda_handler.py' it will make aws configuration for  lambda function
and upload zip file with following file 'lambda_proces.py' (this file contains logic for lambda function)
in more details it will monitor that after uploading picture to s3 bucket lambda will invoke service which will
create metadata for this picture)
2) Then run file 'create_s3_triggers',it will check if we  have related bucket and policy , if we don't have it will create them
automatically, then create s3 trigger and give it a permission to invoke relate service to process data.
3) Then we  should run file 'upload_file_to_bucket.py' which will upload jpg file to s3 bucket.
4) Then by running file 'get_metadata.py' we can test if metadata file is really generated and if we can download it.