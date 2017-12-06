#!/usr/bin/env python3

import argparse
import csv
from datetime import datetime
import time
import requests
import logging

class ScheduledMessage:
    def __init__(self, email: str, message: str, timing: int):
        self.email = email
        self.message = message
        self.timing = timing

    def __str__(self):
        return "%s '%s' %d %d"%(self.email, self.message, self.timing)


def getParsedMessages(inputfile):
    messages = list()

    spamreader = csv.DictReader(inputfile, delimiter=',', quotechar='"')
    for row in spamreader:
        for s in row["schedule"].split('-'):
            schedule_timing = int(s.replace('s', ''))
            message = ScheduledMessage(email=row["email"], message=row["text"], timing=schedule_timing)
            messages.append(message)
    messages = sorted(messages, key=lambda x: x.timing)
    return messages


def __main__():
    # At first we need to parse cmd arguments
    parser = argparse.ArgumentParser(description='Process customers messages csv file.')
    parser.add_argument('--input', help='input csv file', type=argparse.FileType('r'))
    parser.add_argument('--send_url', help='url to send messages', type=str)
    args = parser.parse_args()

    #put messages from file to sorted list
    messages = getParsedMessages(args.input)
    args.input.close()


    #Init variables that we need in message loop
    previous_timing = 0 #Schedule time of previous message
    cumulative_time_delta = 0 #Time that we spent in sending message
    start_time = None #Variable that is used to store time in processing and sending messages


    #iterating throw list as it was queue with possibility to delete undemanded items
    while messages:
        f = messages.pop(0)

        #if it is not first iteration -  we measure timing of previous iteration and remove it from sleeptime
        if start_time:
            cumulative_time_delta += (datetime.now() - start_time).total_seconds()

        # Wait for needed time minus time spent for posting previous message.
        # But if somehow we spent in posting message more time that we need to wait for next message, we don't wait
        # and post the next message immediately
        if (f.timing - previous_timing - cumulative_time_delta)>0:
            time.sleep(f.timing - previous_timing - cumulative_time_delta)
            cumulative_time_delta = 0

        # Start to measure time spent in processing and sending message
        start_time = datetime.now()

        response = requests.post(args.send_url+"/messages", json={
            "email": f.email,
            "text": f.message
        })

        if response.status_code == 201:
            # Check if customer already paid the invoice, we don't disturb him anymore
            # And remove message to him from the queue
            if response.json().get("paid") == True:
                messages = [m for m in messages if m.email != f.email]
        else:
            #I am not sure what to do in this case so we just write error to log and do nothing
            logging.warning(response.status_code, response.text)

        previous_timing = f.timing


if __name__ == '__main__':
    __main__()