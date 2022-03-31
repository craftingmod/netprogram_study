from socket import *
import argparse

s = socket(AF_INET, SOCK_STREAM)

parser = argparse.ArgumentParser()

parser.add_argument("-s", default="localhost")
parser.add_argument