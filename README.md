# message_sender

This is message sender script, was written as code challenge

Script runs on Python3 and uses 1 external library `requests` for sending http requests

To download all necessary libraries you need to run pip install:

```pip3 install requirements.txt```


To launch script you need to run the command:

```bash ./run.sh <path_to_commservice_executable_file>```

for example

```bash ./run.sh ./commservice.mac```


It will launch your commservice in background, will run script that will
parse and send all messages and after the script finishes
it will stop commservice and all logs will be shown