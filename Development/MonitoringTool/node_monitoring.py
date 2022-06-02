
# -*- coding: utf-8 -*-

# This application is monitoring CPU, RAM usage and writes it to a .csv file
from datetime import datetime
import time

import psutil as psutil


class WordFileCreator:
    dictionary = list()


# TODO: Plot network usage
def main():
    node_name = set_node_name()
    write_interval = 1
    print(f"Hardware monitoring started, will write every {write_interval} sec to file.")

    # create files to write to:
    current_date = datetime.now().strftime("%d-%b-%Y_%H-%M-%S")
    file_name_cpu = node_name + "_cpu_utilization_" + current_date + ".csv"
    file_name_mem = node_name + "_mem_utilization_" + current_date + ".csv"
    file_name_net = node_name + "_net_utilization_" + current_date + ".csv"
    file_cpu = open(file_name_cpu, 'w+')  # existing file will be overwritten
    file_mem = open(file_name_mem, 'w+')  # existing file will be overwritten
    file_net = open(file_name_net, 'w+')  # existing file will be overwritten

    # Plot data to file as long as required:
    file_cpu.write("ts, cpu util[%] \n")
    file_mem.write("ts, mem util[%] \n")
    file_net.write("ts, net io[mBit/sec] \n")
    # initialize cpu_counter and net counter:
    psutil.cpu_percent()
    network_counter = psutil.net_io_counters()
    bandwidth_bytes_old = network_counter.bytes_sent + network_counter.bytes_recv
    while True:
        # Track network:
        network_counter = psutil.net_io_counters()
        bandwidth_bytes_new = network_counter.bytes_sent + network_counter.bytes_recv
        bandwidth_bytes_diff = bandwidth_bytes_new - bandwidth_bytes_old
        bandwidth_bytes_old = bandwidth_bytes_new
        bandwidth_mbit_per_sec = (bandwidth_bytes_diff / (1024 * 1024)) * 8  # *8 due to byte to bit conversion

        # Track cpu and mem:
        now_str = datetime.now().strftime("%H:%M:%S")
        file_cpu.write(f"{now_str},{psutil.cpu_percent(interval=None)} \n")
        file_mem.write(f"{now_str},{psutil.virtual_memory().percent} \n")
        file_net.write(f"{now_str},{bandwidth_mbit_per_sec} \n")
        time.sleep(write_interval)  # write interval
    return 0


def set_node_name():
    print("What is the name of your node? (Will be prefix to filename)")
    return input()


if __name__ == "__main__":
    main()
