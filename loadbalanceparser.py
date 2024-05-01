logs = open('./loadbalancelog.txt', 'r')

times = []

isHeader = True
for line in logs:
    if isHeader:
        isHeader = False
        continue
    line = line.strip()
    line = line.split("\t")
    ts = line[0]
    times.append(float(ts))

# sort times
times.sort()

# find the average difference between times
diffs = []
for i in range(1, len(times)):
    diffs.append(times[i] - times[i-1])
# find average
average = sum(diffs) / len(diffs)
print("Average time between load balance: " + str(average))

