import matplotlib.pyplot as plt
import numpy as np
import splunklib
import splunklib.client as client
import splunklib.results as results
from datetime import datetime

HOST = "ip address"
PORT = 8089
USERNAME = "admin"
PASSWORD = "password!"

service = client.connect(host=HOST, port=PORT, username=USERNAME, password=PASSWORD)
rr = splunklib.results.ResultsReader(
    service.jobs.export("search * earliest=-6d@d | eval megabytes = bytes/1024/1024 | timechart sum(megabytes)"))

dates = []
values = []

startPrint = False

for result in rr:
    if isinstance(result, results.Message):
        if result.message == "Your timerange was substituted based on your search string":
            startPrint = True
    elif isinstance(result, dict):
        parsedDate = str(list(result.values())[0]).replace(' 00:00:00.000 EDT', '')
        dt: datetime = datetime.strptime(parsedDate, '%Y-%m-%d')
        splunk_date = dt.strftime("%a, %b %d %Y")
        splunk_value = list(result.values())[1]
        if startPrint:
            dates.append(splunk_date)
            values.append(round(float(splunk_value), 2))
            print(splunk_date + " - " + splunk_value)

bar_width = 0.5
plt.grid(color='grey',alpha=0.2)
plt.title('Joe0.com - Bandwidth Usage by Date (past week)', color='red')
plt.ylabel('MegaBytes', color='green')
bar = plt.bar(np.arange(len(values)) + bar_width, values, bar_width, align='center', alpha=0.5, color='green')
plt.xticks(range(len(values)), dates, rotation=45)

i = 0
for rect in bar:
    height = rect.get_height()
    plt.text(rect.get_x() + rect.get_width() / 2.0, height, values[i], ha='center', va='bottom')
    i = i + 1

plt.show()
