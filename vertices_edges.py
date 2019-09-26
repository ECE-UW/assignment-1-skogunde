from intersection_code import find_intersection


class StreetDataBase(object):
    def __init__(self):
        self.vertices = {}
        self.edges = {}
        self.intersections = []  # will contain array of Intersection objects
        self.street_names = []
        self.street_lines = []

    # param: street_name, name of street
    # param: street_points, is a array of points
    def add(self, street_name, street_points):
        # Check if street already exists.
        if street_name in self.street_names:
            print("Error: ", street_name, " already exists")
            return
        self.street_names.append(street_name)
        self.street_lines.append(Street(street_points))

    def change(self, street_name, street_points):
        # check for the existence of the street name
        if street_name in self.street_names:
            st_index = self.street_names.index(street_name)
            self.street_lines[st_index] = Street(street_points)
        else:
            print("Error: ", street_name, " does not exist")

    def remove(self, street_name):
        if street_name in self.street_names:
            index = self.street_names.index(street_name)
            self.street_names.pop(index)
            self.street_lines.pop(index)
        else:
            print("Error: ", street_name, " does not exist")

    def output_graph(self):
        self.vertices.clear()
        self.edges.clear()
        del self.intersections[:]  # python2 does not support clear() on list

        # Clear line intersections cache.
        for ind in range(len(self.street_lines)):
            for line in self.street_lines[ind].line_segments:
                del line.intersections[:]

        for cur_street_index in range(len(self.street_lines) - 1):
            for next_street_index in range(cur_street_index + 1, len(self.street_lines)):
                self.street_lines[cur_street_index].compare_and_store_results(self.street_lines[next_street_index],
                                                                              self.intersections, self.vertices,
                                                                              self.edges)

        for inter_point in self.intersections:  # for each intersection point
            for lineX in inter_point.lines:
                sort_vertices(lineX, self.edges)

        # Print vertices
        print("V = {")
        for point in self.vertices:
            print("  ", point + 1, ": ", self.vertices[point])
        print("}")

        # Print edges
        print("E = {")
        for edge in self.edges:
            line = self.edges[edge]
            # print(line)
            print("<", (list(self.vertices.keys())[list(self.vertices.values()).index(line.begin)] + 1), ",",
                  (list(self.vertices.keys())[list(self.vertices.values()).index(line.end)] + 1), ">")
        print("}")


def add_unique_edges(edges_dict, new_edge):
    for index in edges_dict:
        line = edges_dict[index]
        if (line.begin == new_edge.begin and line.end == new_edge.end) or \
                (line.begin == new_edge.end and line.end == new_edge.begin) or \
                (new_edge.begin == new_edge.end):
            return

    edge_len = len(edges_dict)
    edges_dict[edge_len] = new_edge


def sort_vertices(line, edges):
    vertices_in_line = []
    for inter_point in line.intersections:
        vertices_in_line.append(inter_point)

    vertices_in_line.append(line.begin)
    vertices_in_line.append(line.end)

    sorted_points = []

    for vertex in sorted(vertices_in_line):
        sorted_points.append(vertex)

    for point_index in range(len(sorted_points) - 1):
        add_unique_edges(edges, Line(sorted_points[point_index], sorted_points[point_index + 1]))


class Line(object):
    def __init__(self, begin, end):
        self.begin = begin
        self.end = end
        self.intersections = []  # to keep track of number of intersection points in the current line segment

    def __str__(self):
        return str(self.begin) + '-->' + str(self.end)

    def add_unique_intersection(self, new_inter_point):
        for point in self.intersections:
            # Do not add duplicate point.
            if point == new_inter_point:
                return

        # Check for T-intersection, if found, then don't consider to add
        # intersection point to the current line.
        if self.begin == new_inter_point or self.end == new_inter_point:
            return

        self.intersections.append(new_inter_point)


# This static method is defined to avoid duplicate vertices
# Check before adding item into vertices array
def add_unique_vertices(vertices, point):
    flag = 0
    for vertex in vertices.values():  # loop through points
        if vertex == point:
            flag = 1

    if flag == 0:
        # Add each vertex/point in a order starting from 0 indexed.
        new_index = len(vertices)
        vertices[new_index] = point


class Intersections(object):
    def __init__(self, point):
        self.point = point
        self.lines = []  # to keep track of number of lines that intersect.

    def add(self, line):
        if line not in self.lines:
            self.lines.append(line)


def add_unique_intersection_objects(intersections, new_intersection_point, line1, line2):
    # Check if intersections list is empty,
    # then add the very first Intersections object unconditionally
    if not len(intersections):
        new_inter_object1 = Intersections(new_intersection_point)
        new_inter_object1.add(line1)
        new_inter_object1.add(line2)
        intersections.append(new_inter_object1)
    else:
        found = 0
        for old_inter_object in intersections:
            if old_inter_object.point == new_intersection_point:
                found = 1
                old_inter_object.add(line1)
                old_inter_object.add(line2)
                break  # break the loop, already found an existing intersection point

        if not found:
            new_inter_object2 = Intersections(new_intersection_point)
            new_inter_object2.add(line1)
            new_inter_object2.add(line2)
            intersections.append(new_inter_object2)


class Street(object):
    # A street can have 2 or more points (can have more than one line)
    def __init__(self, points):
        self.line_segments = []

        # make sure to check at least 2 points in a street
        if len(points) > 1:
            for i in range(len(points) - 1):
                self.line_segments.append(Line(points[i], points[i + 1]))

    def compare_and_store_results(self, next_street, intersections, vertices, edges):
        for current_line in self.line_segments:
            for next_line in next_street.line_segments:
                new_intersection_point = find_intersection(current_line, next_line)
                if new_intersection_point is not None:
                    add_unique_intersection_objects(intersections, new_intersection_point, current_line, next_line)

                    add_unique_vertices(vertices, new_intersection_point)  # intersection is also a point
                    add_unique_vertices(vertices, current_line.begin)  # begin and end are points of line
                    add_unique_vertices(vertices, current_line.end)
                    add_unique_vertices(vertices, next_line.begin)
                    add_unique_vertices(vertices, next_line.end)

                    # Add intersection point to each intersecting lines
                    current_line.add_unique_intersection(new_intersection_point)
                    next_line.add_unique_intersection(new_intersection_point)
