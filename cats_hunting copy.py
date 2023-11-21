from main import Point
from proper_tchebychew import distance_euclid as distance

HUNT_TIME = {
    "fieldmouse": 180,
    "house mouse": 120,
    "snail": 90,
    "leaf": 60,
    "pebble": 30,
    "START": 0
}


class Hunt:
    def __init__(self, cat):
        self.distance = 0
        self.time = 0
        self.points_list = []
        self.score = 0
        self.cat = cat

    def append(self, prey):
        new_distance = distance(self.points_list[len(self.points_list) - 1], prey)
        self.points_list.append(prey)
        self.score += self.cat.preferences[prey.type]
        self.distance += distance
        self.time += (new_distance/self.speed + HUNT_TIME[prey.type])


class Cat:
    def __init__(self, name, preferences):
        self.name = name
        self.preferences = preferences
        self.speed = 10


class Prey(Point):
    def __init__(self, type, x=0, y=0, coordinates_tuple=None):
        super().__init__(x, y, coordinates_tuple)
        self.type = type


def can_return(current_point, end_point, time_left):
    print('...')
    # checks if cat can return to start point in left time


def time_to_return(point):
    print('...')
    # returns time which cat needs to return to start point from given point


def value_ratio(current_point, end_point, cat):
    print('...')
    # returns value to time and distance ratio for given point and cat


def no_interesting_objects(cat, points):
    print('...')
    # returns true if there are interesting objects for given cat in given area, else return false


def check_if_crossing_paths(start_point, end_point, paths):
    print('...')
    # return true if section crosses another cats path, else returns false


#  Returns cat to the starting point
def return_to_start(start_point, current_point, current_hunt, time):
    current_hunt.points_list.append(start_point)
    time -= time_to_return(current_point)
    return current_hunt, time


def updated_paths(cat_paths, cat_hunts):
    print('...')
    # adds hunt paths to global paths of all cats and returns updated value (add every path in cat_hunts to cat_paths)


def cat_hunting(cat, points, start_point, cats_paths):
    MIN_TIME = 60
    MAX_CAT_CAPACITY = 5
    POINT_RANGE = 5
    time = 7200
    total_score = 0
    cats_hunts = []
    while (time > MIN_TIME):
        current_point = start_point
        current_hunt = Hunt(cat=cat)
        current_hunt.points_list.append(start_point)
        points_in_range = []
        hunt_count = 0
        while (hunt_count < MAX_CAT_CAPACITY):
            next_point = None
            for point in points:
                if distance(point=point, destination_point=current_point) <= POINT_RANGE:
                    points_in_range.append(point)
            if not no_interesting_objects(cat=cat, points=points_in_range):
                for point in points_in_range:
                    if can_return(start_point=current_point, end_point=point, time_left=time) and not check_if_crossing_paths(start_point=current_point, end_point=point, paths=cats_paths):
                        if value_ratio(current_point=current_point, end_point=point, cat=cat) > value_ratio(current_point=current_point, end_point=next_point, cat=cat):
                            next_point = point
            # tutaj else i zwiększanie zasięgu poszukiwań jeżeli nic nie znalazł
            if next_point:
                current_hunt.append(next_point)
                time -= time_to_return(next_point)
                hunt_count += 1
                points.remove(next_point)
            else:
                if len(current_hunt.points_list) > 1:
                    current_hunt, time = return_to_start(start_point=start_point, current_point=current_point, current_hunt=current_hunt, time=time)

        if len(current_hunt.points_list) > 1:
            cats_hunts.append(current_hunt)
            total_score += current_hunt.score
    return total_score, points, updated_paths(cat_paths=cats_paths, cat_hunts=cats_hunts)

# Generate points as Prey objects, starting objects has type value of START
