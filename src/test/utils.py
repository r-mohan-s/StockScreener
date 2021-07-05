import csv


def write_to_file(symbol_name, file_name):
    with open(file_name, 'a') as file:
        file.write(symbol_name)
        file.write("\n")


def read_from_file(file_name):
    with open(file_name, 'r') as file_to_read:
        csv_reader = csv.reader(file_to_read)
        next(csv_reader)
        stocks_to_check = []
        for symbol in csv_reader:
            stocks_to_check.append(symbol[0])
        return stocks_to_check
