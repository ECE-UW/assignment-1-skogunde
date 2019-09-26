import re
import sys

from vertices_edges import StreetDataBase
from point import Point


def validate_street_name(name_input):
    name = name_input.lower()
    # Allow only alphabets (lower/upper case) including 0 or more space
    # At least one letter must be be present
    letters = re.compile("^[a-zA-Z ]+$")
    if not letters.match(name):
        raise Exception("Error: " + name_input + "street is not valid")

    if not name.replace(" ", "").__len__():
        raise Exception("Error: street name is empty")
    return name


def parse_coordinates(coordinates):
    r = re.compile("^[(]\s*-?\d+\.?\d*\s*[,]\s*-?\d+\.?\d*\s*[)]")
    split = r.findall(coordinates)

    if not split:
        raise Exception("Error: Invalid format " + coordinates)


def reform_coordinate(coordinate):
    string1 = coordinate.replace(" ", "")
    string2 = string1.replace(")(", ") (")
    parts = string2.split()

    if len(parts) <= 1:
        raise Exception("Error: Not sufficient coordinates")

    for part in parts:
        parse_coordinates(part)

    return parts


def parse_command(input_line):
    valid_cmd = re.findall(r'^[a|c|r|g]', input_line[:1])
    if not valid_cmd:
        raise Exception(input_line[0] + " is not a valid command.\n"
                                        "Available commands are:\n"
                                        "a: add a street\n"
                                        "c: change a street\n"
                                        "r: remove a street\n"
                                        "g: generate graph\n")
    return valid_cmd[0].replace(" ", "")


def parse_street_name(input_line):
    # street_name = input_line[2:]
    start_index, end_index = input_line.find('"'), input_line.rfind('"')

    # Check to make sure street name is enclosed in double quotes.
    if start_index == end_index:
        raise Exception('Error: street name is not enclosed in double quotes')

    name_input = input_line[start_index + 1: end_index]
    return validate_street_name(name_input), end_index + 1


def generate_point_objects_from_coordinates(coordinates):
    points_array = []
    for coordinate in coordinates:
        coord = coordinate.replace("(", "").replace(")", "").split(',')
        point = Point(float(coord[0]), float(coord[1]))
        points_array.append(point)

    return points_array


def main():
    street_db = StreetDataBase()

    while True:
        input_line = sys.stdin.readline()
        if input_line:
            input_line = input_line.replace('\n', '').strip().rstrip()
            if not input_line:
                print("Do you want to terminate the program ? Issue ctrl+D to terminate.")
                continue

            try:
                cmd = parse_command(input_line)

                if cmd == 'a' or cmd == 'c':
                    street_name, coordinate_begin_index = parse_street_name(input_line)
                    coordinates = reform_coordinate(input_line[coordinate_begin_index:])
                    coordinate_points = generate_point_objects_from_coordinates(coordinates)
                    if cmd == 'a':
                        street_db.add(street_name, coordinate_points)
                    elif cmd == 'c':
                        street_db.change(street_name, coordinate_points)

                if cmd == 'r':
                    street_name, index = parse_street_name(input_line)
                    street_db.remove(street_name)

                if cmd == 'g':
                    street_db.output_graph()

            except Exception as err_msg:
                print(err_msg)
        else:
            sys.exit()  # Handle ctrl+D


if __name__ == '__main__':
    main()
