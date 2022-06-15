# import datetime module from datetime
from datetime import datetime
current_time = datetime.now()
date = current_time.strftime("%d-%m-%y %H:%M:%S")
print(date)