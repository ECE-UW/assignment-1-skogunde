from point import Point


def find_intersection(line1, line2):
    # a1 = y2 - y1
    a1 = line1.end.y - line1.begin.y  # a1 = point2[1] - point1[1]
    b1 = line1.begin.x - line1.end.x  # b1 = x1-x2
    c1 = a1 * line1.begin.x + b1 * line1.begin.y  # c1 = (a1 * x1) + (b1 * y1)

    a2 = line2.end.y - line2.begin.y
    b2 = line2.begin.x - line2.end.x
    c2 = a2 * line2.begin.x + b2 * line2.begin.y

    denominator = a1 * b2 - a2 * b1
    if denominator == 0:
        # Parallel lines detected.
        return None
    else:
        x = (b2 * c1 - b1 * c2) / denominator
        y = (a1 * c2 - a2 * c1) / denominator
        # Check the boundary to find intersection
        # Note: Potential intersections are not intersections
        if (((min(line1.begin.x, line1.end.x) <= x) and (x <= max(line1.begin.x, line1.end.x))
             and (min(line1.begin.y, line1.end.y) <= y) and (y <= max(line1.begin.y, line1.end.y)))
                and ((min(line2.begin.x, line2.end.x) <= x) and (x <= max(line2.begin.x, line2.end.x))
                     and (min(line2.begin.y, line2.end.y) <= y) and (y <= max(line2.begin.y, line2.end.y)))):
            return Point(x, y)
        else:
            return None
