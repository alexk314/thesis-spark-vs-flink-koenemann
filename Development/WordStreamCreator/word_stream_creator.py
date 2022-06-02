#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This application is creating input data for Stream processing
# Features:
# 1. Open Socket and establish connection to Cluster
# 2. After connecting, data is created (random words) and send to server.
import socket
import sys
import time
import urllib.request  # for retrieving a dictionary for random words
import random  # for selecting random words


class WordStreamCreator:
    dictionary = list()


def main():
    import_dictionary()

    # Establish connection with client/cluster:
    port = 9000
    host = '192.168.178.56'
    addr, connection = create_socket_and_connection(host, port)
    print('Got connection from cluster: ', addr)

    initiate_experiment(connection)
    return 0


def import_dictionary():
    word_input_url = "https://www.mit.edu/~ecprice/wordlist.100000"  # 100.000 words
    response = urllib.request.urlopen(word_input_url)
    WordStreamCreator.dictionary = response.read().decode().splitlines()
    print(f"Imported dictionary from MIT with {format(len(WordStreamCreator.dictionary), ',d')} words")


def initiate_experiment(connection):
    print("Type 'wps' for sending words per second or 'p' for maximum penetration of the cluster")
    # chosen_mode = input() #TODO: einkommentieren
    chosen_mode = 'p'
    if chosen_mode == 'wps':
        # Ask for velocity of new words per second:
        word_velocity_per_second = set_velocity()
        duration_experiment = set_experiment_duration()
        send_random_words_stream_per_second(connection, int(duration_experiment), int(word_velocity_per_second))
    elif chosen_mode == 'p':
        # duration_experiment = set_experiment_duration() #TODO: einkommentieren
        duration_experiment = 10
        send_max_stream(connection, int(duration_experiment))
    close_connection(connection)


def set_experiment_duration():
    print("How long do you want to penetrate the cluster [sec]?")
    return input()


def set_velocity():
    print("How many words do you want to send to the cluster per second?")
    return input()


def send_random_words_stream_per_second(connection, duration_experiment_sec, words_per_second):
    print(f"Starting experiment for {duration_experiment_sec} seconds with {words_per_second} words per second")
    t_start = time.time()
    t_end = t_start + float(duration_experiment_sec)
    # TODO: Check assumption, that TCP Packages will be distributed roughly even over time
    while time.time() < t_end:
        t_current_round_start = time.time()
        random_words = create_random_words(words_per_second)
        connection.sendall(random_words.encode())  # utf-8 encoding
        t_current_round = time.time() - t_current_round_start
        required_sleep = 1.0 - min(t_current_round, 1.0)  # upper bound 1 sec
        print(f"required sleep for current round: {round(required_sleep, 2)} sec.")
        time.sleep(required_sleep)  # accounting for time to create and send data
    t_finish = time.time() - t_start
    number_of_words = duration_experiment_sec * words_per_second
    print(f"Experiment finished after {round(t_finish, 2)} sec. number of words: {format(number_of_words, ',d')}")


def send_max_stream(connection, duration_experiment_sec):
    print(f"Starting experiment for {duration_experiment_sec} seconds with max velocity")
    t_start = time.time()
    t_end = t_start + float(duration_experiment_sec)
    word_counter = 0
    # data_counter = 0
    while time.time() < t_end:
        words_per_packet = 1
        random_words_line = create_random_words(words_per_packet)
        word_counter += words_per_packet
        # data_counter += sys.getsizeof(random_words_line)
        connection.sendall(random_words_line.encode())  # utf-8 encoding
    t_finish = time.time() - t_start
    print(
        f"Experiment finished after {round(t_finish, 2)} sec. number of words: {format(word_counter, ',d').replace(',', '.')}")


def create_random_words(words_per_second):
    # Note: Random words will be retrieved every second, if performance problems arise could be optimized.
    random_words = ' '.join(random.sample(WordStreamCreator.dictionary, words_per_second)) + "\n"
    return random_words


def create_socket_and_connection(host, port):
    # Create a socket object
    stream_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    stream_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("Socket successfully created")

    # Bind socket to the port
    stream_socket.bind((host, port))
    print("Socket bind to %s" % port)

    # 2.1 Put the socket into listening mode and wait for cluster
    stream_socket.listen(5)
    print("Socket is listening")
    connection, addr = stream_socket.accept()
    return addr, connection


def close_connection(connection):
    connection.shutdown(socket.SHUT_RDWR)  # No reads and writes allowed afterwards
    connection.close()
    print("Connection closed")
    pass


if __name__ == "__main__":
    main()
