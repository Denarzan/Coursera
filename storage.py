import os
import tempfile
import argparse
import json

"""key-values storage with --key and --val arguments"""
def print_data(path, key):
    data = read_data(path) #reading data from the file
    if data == {}:
        print(None)
    else:
        try:
            print(*data[key], sep=", ") #printing data
        except KeyError:
            print(None)

def read_data(path):
    if os.path.getsize(path) > 0: #checking if the file is not empty
        with open(path, "r") as file:
            data = json.load(file) #loading from the file
            return data
    else:
        return {}


def write_data(path, key, value):
    if os.path.exists(path): # checking if the file exist
        data = read_data(path)
        if key in data and value not in data.values(): #if we write new value to data
            data[key].append(value)
            with open(path, 'w') as file:
                json.dump(data, file)
        if key in data and value in data.values(): # if we write key and value that are in the file
            return
        if key not in data: # if we write new key and new value
            data[key] = [value]
            with open(path, 'w') as file:
                json.dump(data, file)

    else:
        with open(path, 'w') as file: # if new file
            data = {key: [value]}
            json.dump(data, file)


def arguments():
    parser = argparse.ArgumentParser() #adding arguments
    parser.add_argument("--key", help="enter key")
    parser.add_argument("--val", help="enter value")
    args = parser.parse_args()
    return args


def main(path):
    args = arguments()
    try:
        if args.key and args.val: #checking if we take key and value to write data
            write_data(path, args.key, args.val)
        elif args.key: #checking if we take key to read data
            print_data(path, args.key)
        else:
            print()
    except FileNotFoundError:
        print(None)

if __name__ == '__main__':
    storage_path = os.path.join(tempfile.gettempdir(), 'storage.data') #the file in which we will store the data
    main(storage_path)
