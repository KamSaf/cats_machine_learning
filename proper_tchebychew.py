import math
from main import Point, Path


def distance_tschebyshev(A, B):
    dx = abs(B.x - A.x)
    dy = abs(B.y - A.y)
    return max(dx, dy)


def distance_euclid(A, B):
    d = math.sqrt(((A.x - B.x)**2) + ((A.x - B.y)**2))
    return d


def find_closest_point(given_point, path_length, points):
    min_distance = float('inf')
    closest_point = None
    for point in points:
        if given_point != point:
            distance = distance_tschebyshev(given_point, point)
            # distance = distance_euclid(given_point, point)
            if distance < min_distance:
                min_distance = distance
                closest_point = point
    path_length += min_distance
    return closest_point, path_length, points


def create_path(points, start_point, end_point, steps_number):
    path_length = 0
    steps = [start_point]
    next_step = start_point
    while steps_number > 1:
        closest_point, path_length, points = find_closest_point(next_step, path_length, points)
        steps.append(closest_point)
        steps_number = steps_number - 1
        points.remove(next_step)
        next_step = closest_point
    steps.append(end_point)
    path_length += distance_tschebyshev(steps[len(steps)-1], end_point)
    # path_length += distance_euclid(steps[len(steps)-1], end_point)
    return Path(steps, round(path_length, 3))


# A = Point(12.02, 0.02)
# B = Point(34.02, 12.02)
# C = Point(20.53, 82.51)
# D = Point(53.12, 17.62)
# E = Point(11.34, 4.51)
# F = Point(31.63, 64.19)

# points = [A, B, C, D, E, F]

points = Point.generate_coordinates(15)

start_point = points[0]

end_point = points[2]

steps_number = 4

print(create_path(points, start_point, end_point, steps_number))
