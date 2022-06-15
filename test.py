from datetime import datetime
import time

labels = []

for i in range(100):
    now = datetime.now()
    current_time = now.strftime("%d-%m-%y %H:%M:%S")
    labels.append(current_time)
    if len(labels) > 11:
        labels.pop(0)
    print(labels)
    time.sleep(1)

