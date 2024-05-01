import matplotlib.pyplot as plt
import numpy as np

show_graph = False
save_graph = True
graph_time_range = False
line_graph = False

# fileName = 'test.txt' 
# fileName = 'one_second_kernel_make_tiny400thread.txt'
fileName = 'one_second_none.txt'
logs = open('./data/'+fileName, 'r')
# logs = open('./data/one_second_kernel_make_tiny_5thread.txt', 'r')

class Log_Item:
    def __init__(self, ts, thread_name, pid, message):
        self.ts = ts
        self.thread_name = thread_name
        self.pid = pid
        self.message = message
    # print the log item
    def __str__(self):
        return str(self.ts) + "\t" + self.thread_name + "\t" + self.pid + "\t" + self.message

def between_time_range(time_range, ts):
    return True
    if ts >= time_range[0] and ts <= time_range[1]:
        return True
    return False

log_items = []

isHeader = True
for line in logs:
    if isHeader:
        isHeader = False
        continue
    line = line.strip()
    line = line.split("\t")
    ts = line[0]
    thread_name = line[1]
    pid = line[2]
    message = line[3]
    # print(ts)
    log_item = Log_Item(float(ts), thread_name, pid, message)
    log_items.append(log_item)


points_x_cpu0 = []
points_y_cpu0 = []
points_x_cpu1 = []
points_y_cpu1 = []
points_x_cpu2 = []
points_y_cpu2 = []
points_x_cpu3 = []
points_y_cpu3 = []

time_range = [521628396392.0, 521644130442.0]


load_balance_interval = 0.015

next_time0 = False
save_log0 = None
next_time1 = False
save_log1 = None
next_time2 = False
save_log2 = None
next_time3 = False
save_log3 = None

interval_map0 = {}
interval_map1 = {}
interval_map2 = {}
interval_map3 = {}

interval_maps = [interval_map0, interval_map1, interval_map2, interval_map3]

too_big_deltas = {
    0: [],
    1: [],
    2: [],
    3: []
}

all_idle_times = [[], [], [], []]

# sort according to ts
log_items.sort(key=lambda x: x.ts)
for item in log_items:
    # print(item)
    message = item.message
    if "CPU 0 with" in message and between_time_range(time_range, float(item.ts)):
        points_x_cpu0.append(float(item.ts))
        points_y_cpu0.append(int(message.split(" ")[-1]))
    if "CPU 1 with" in message and between_time_range(time_range, float(item.ts)):
        points_x_cpu1.append(float(item.ts))
        points_y_cpu1.append(int(message.split(" ")[-1]))
    if "CPU 2 with" in message and between_time_range(time_range, float(item.ts)):
        points_x_cpu2.append(float(item.ts))
        points_y_cpu2.append(int(message.split(" ")[-1]))
    if "CPU 3 with" in message and between_time_range(time_range, float(item.ts)):
        points_x_cpu3.append(float(item.ts))
        points_y_cpu3.append(int(message.split(" ")[-1]))

    if "CPU 0 with 0" in message or "CPU 1 with 0" in message or "CPU 2 with 0" in message or "CPU 3 with 0" in message:
        # find the next time it is not 0
        if not next_time0 and "CPU 0 with 0" in message:
            # print(item)
            next_time0 = True
            save_log0 = item
        if not next_time1 and "CPU 1 with 0" in message:
            # print(item)
            next_time1 = True
            save_log1 = item
        if not next_time2 and "CPU 2 with 0" in message:
            # print(item)
            next_time2 = True
            save_log2 = item
        if not next_time3 and "CPU 3 with 0" in message:
            # print(item)
            next_time3 = True
            save_log3 = item

    if "CPU 0 with" in message and next_time0 and "CPU 0 with 0" not in message:
        # print(item)
        next_time0 = False
        if save_log0 == None:
            # throw error
            print("ERROR")
            continue
        time_delta = float(item.ts) - float(save_log0.ts)
        time_delta = time_delta / 1000000000
        all_idle_times[0].append(time_delta)
        if time_delta > load_balance_interval:
            # pass
            # print(save_log0)
            # print(item)
            # print("time delta is: ", time_delta)
            too_big_deltas[0].append((save_log0, item, time_delta))
        save_log0 = None
    if "CPU 1 with" in message and next_time1 and "CPU 1 with 0" not in message:
        # print(item)
        next_time1 = False
        if save_log1 == None:
            # throw error
            print("ERROR")
            continue
        time_delta = float(item.ts) - float(save_log1.ts)
        time_delta = time_delta / 1000000000
        all_idle_times[1].append(time_delta)
        if time_delta > load_balance_interval:
            # print(save_log1)
            # print(item)
            # print("time delta is: ", time_delta)
            too_big_deltas[1].append((save_log1, item, time_delta))
            # pass
        save_time1 = None
    if "CPU 2 with" in message and next_time2 and "CPU 2 with 0" not in message:
        # print(item)
        next_time2 = False
        if save_log2 == None:
            # throw error
            print("ERROR")
            continue
        time_delta = float(item.ts) - float(save_log2.ts)
        time_delta = time_delta / 1000000000
        all_idle_times[2].append(time_delta)
        if time_delta > load_balance_interval:
            # print(save_log2)
            # print(item)
            # print("time delta is: ", time_delta)
            too_big_deltas[2].append((save_log2, item, time_delta))
            pass
        save_time2 = None
    if "CPU 3 with" in message and next_time3 and "CPU 3 with 0" not in message:
        # print(item)
        next_time3 = False
        if save_log3 == None:
            # throw error
            print("ERROR")
            continue
        time_delta = float(item.ts) - float(save_log3.ts)
        time_delta = time_delta / 1000000000
        all_idle_times[3].append(time_delta)
        if time_delta > load_balance_interval:
            # print(save_log3)
            # print(item)
            # print("time delta is: ", time_delta)
            too_big_deltas[3].append((save_log3, item, time_delta))
        save_time3 = None

# make intervals from list points_x_cpu
for i in range(len(points_x_cpu0)):
    if i == len(points_x_cpu0) - 1:
        break
    interval_map0[(points_x_cpu0[i], points_x_cpu0[i+1])] = points_y_cpu0[i]
for i in range(len(points_x_cpu1)):
    if i == len(points_x_cpu1) - 1:
        break
    interval_map1[(points_x_cpu1[i], points_x_cpu1[i+1])] = points_y_cpu1[i]
for i in range(len(points_x_cpu2)):
    if i == len(points_x_cpu2) - 1:
        break
    interval_map2[(points_x_cpu2[i], points_x_cpu2[i+1])] = points_y_cpu2[i]
for i in range(len(points_x_cpu3)):
    if i == len(points_x_cpu3) - 1:
        break
    interval_map3[(points_x_cpu3[i], points_x_cpu3[i+1])] = points_y_cpu3[i]


def see_interval_overlap(interval, cpu):
    # see which other cpu's interval overlaps with this interval
    for i in range(4):
        if i == cpu:
            continue
        for key in interval_maps[i]:
            if key[0] < interval[1] and key[1] > interval[0]:
               print("CPU", i, "has this many threads during this interval: ", interval_maps[i][key])

# print all too big deltas
for i in range(4):
    for delta in too_big_deltas[i]:
        print(delta[0])
        print(delta[1])
        print("time delta is: ", delta[2])
        # see_interval_overlap((delta[0].ts, delta[1].ts), i)
        print()


mean_of_idle_times = []
for i in range(4):
    sum_time = 0
    num_time = 0
    for time in all_idle_times[i]:
        sum_time += time
        num_time += 1
    if num_time != 0:
        mean_of_idle_times.append(sum_time / num_time)
    else:
        mean_of_idle_times.append(0)
print("mean of idle times: ", mean_of_idle_times)

# (1935541293901.0, 1935551023820.0)
# see_interval_overlap((330378152656.0, 330388488316.0), 0)


if line_graph:
    plt.step(points_x_cpu0, points_y_cpu0, label="CPU 0", where='post')
    plt.step(points_x_cpu1, points_y_cpu1, label="CPU 1", where='post')
    plt.step(points_x_cpu2, points_y_cpu2, label="CPU 2", where='post')
    plt.step(points_x_cpu3, points_y_cpu3, label="CPU 3", where='post')
    if graph_time_range:
        plt.axvline(x = time_range[0], color= 'purple')
        plt.axvline(x = time_range[1], color = 'purple') 
    # limit the x axis
    # plt.xlim(time_range[0] - 1000, time_range[1] + 1000)
    plt.legend() 

    fig = plt.gcf()
    if save_graph:
        fig.savefig('./graphs/'+fileName+'_graph.png', dpi=300)
    if show_graph:
        plt.show()
else:
    plt.bar(["0", "1", "2", "3"], mean_of_idle_times)
    # plt.legend()
    plt.ylabel("Mean of idle times (seconds)")
    plt.xlabel("CPU")
    plt.title("Mean of idle times for each CPU")
    fig = plt.gcf()
    if save_graph:
        fig.savefig('./graphs/'+fileName+'_graph_bar.png', dpi=300)
    if show_graph:
        plt.show()


