## Copyright 2022 Salem Inc. All rights reserved
## Use of this code is subject to the terms of the MIT license 

import json
import sys
import csv
import getopt
from azure.eventhub import EventHubProducerClient, EventData

def main():
    argv = sys.argv[1:]
    opts, args = getopt.getopt(argv,'c:s:n:f:',['connection_string=','source=','alert_name=','file='])
    source = 'default'
    file_path = None
    alert_name = None
    event_hub_connection_str = None
    for k,v in opts:
        if k in ('-c','--connection_string'):
            event_hub_connection_str = v.strip('"\'')
        elif k in ('-s','--source'):
            source = v.strip('"\'')
        elif k in ('-n','--alert_name'):
            alert_name = v.strip('"\'')
        elif k in ('-f','--file'):
            file_path = v.strip('"\'')

    if file_path:
        file_extension = file_path.split('.')[-1]
        if file_extension in ('json','txt'):
            with open(file_path) as f:
                if file_extension == 'json':
                    file = f.read()
                    alerts = json.loads(file)
                else:
                    alerts = (l.strip() for l in f)
        elif file_extension == 'csv':
            with open(file_path,newline='') as f:
                alerts = csv.DictReader(f)
        else:
            raise ValueError(f'unsupported file type: {file_extension}')
    else:
        raise ValueError('No file path provided')
            

    producer = EventHubProducerClient.from_connection_string(
        conn_str=event_hub_connection_str,
        eventhub_name='alerts'
    )
    try:
        event_data_batch = producer.create_batch()
        count = 0
        for alert in alerts:
            msg = {
                "source": source
            }
            if alert_name:
                msg['alert_name'] = alert_name
            if type(alert) is str:
                msg['alert'] = alert
            else:
                msg['alert'] = json.dumps(alert)
            try:
                event_data_batch.add(EventData(json.dumps(msg).encode('utf-8')))
            except ValueError:
                # EventDataBatch object reaches max_size.
                producer.send_batch(event_data_batch)
                event_data_batch = producer.create_batch()
                event_data_batch.add(EventData(msg.encode('utf-8')))
            count += 1

        producer.send_batch(event_data_batch)
    finally:
        # Close down the producer handler.
        if count == 0:
            print('No alerts found')
        elif count == 1:
            print('Sent 1 alert to Salem')
        else:
            print(f'Sent {count} alerts to Salem')
        producer.close()

if __name__ == '__main__':
    main()