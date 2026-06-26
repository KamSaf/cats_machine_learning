from main import Point, Path
from proper_tchebychew import distance_euclid as distance
from shapely.geometry import LineString

HUNT_TIME = {
    "fieldmouse": 180,
    "house mouse": 120,
    "snail": 90,
    "leaf": 60,
    "pebble": 30,
    "START": 0
}

CAT_SPEED = 10


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
        self.time += (new_distance/CAT_SPEED + HUNT_TIME[prey.type])


class Cat:
    def __init__(self, name, preferences):
        self.name = name
        self.preferences = preferences


# Basically Point class but with additional value of 'type'
class Prey(Point):
    def __init__(self, type, x=0, y=0, coordinates_tuple=None):
        super().__init__(x, y, coordinates_tuple)
        self.type = type


# Returns time required to get to prey and hunt it
def time_to_hunt(prey_type, start_point, end_point):
    return HUNT_TIME[prey_type] + time_to_move(start_point=start_point, target_point=end_point)


# Checks if cat can return to start point in left time
def can_return(start_point, current_point, end_point, time_left):
    required_time = time_to_hunt(prey_type=end_point.type, start_point=current_point, end_point=end_point) + time_to_move(start_point=end_point, target_point=start_point)
    if required_time <= time_left:
        return True
    return False


# Returns time which cat needs to move from start point to target point
def time_to_move(start_point, target_point):
    required_time = distance(target_point, start_point)/CAT_SPEED
    return required_time


# Returns ratio of how profitable given point is
def value_ratio(current_point, end_point, cat):
    standardized_distance = distance(current_point, end_point)/10
    standardized_time = time_to_hunt(prey_type=end_point.type, start_point=current_point, end_point=end_point)/(7200)
    value_ratio = 0.5*(1 - standardized_distance) + 0.5*(1 - standardized_time)
    return value_ratio


# Returns true if there are no interesting objects for given cat in given area, else return false
def no_interesting_objects(cat, points):
    for point in points:
        if cat.preferences[point.type] > 0:
            return False
    return True


# Returns True if path crosses another cats path, else returns False
def check_if_crossing_paths(start_point, end_point, cats_paths, cat_name):
    path_to_check = LineString([(start_point.x, start_point.y), (end_point.x, end_point.y)])
    for cat_key, paths_list in cats_paths.values():
        if cat_key != cat_name:
            for path in paths_list:
                existing_path = LineString([(point.x, point.y) for point in path.steps])
                if path_to_check.intersects(existing_path):
                    return True
    return False


#  Returns cat to the starting point
def return_to_start(start_point, current_point, current_hunt, time):
    current_hunt.points_list.append(start_point)
    time -= time_to_move(start_point=current_point, end_point=start_point)
    return current_hunt, time


# Adds hunt paths to global paths of all cats and returns updated value (add every path in cat_hunts to cats_paths)
def update_paths(cats_paths, cat_hunts):
    for hunt in cat_hunts:
        cats_paths[hunt.cat.name].append(Path(hunt.points_list))
    return cats_paths


# cat - Cat class object
# points - list of points (Prey class objects)
# start_point - point, from which cat will begin hunting
# cats_paths - dictionary with key value of cat name and value of Path containing points visited (hunted) by cat

def cat_hunting(cat, points, start_point, cats_paths):
    MIN_TIME = 60
    MAX_CAT_CAPACITY = 5
    POINT_RANGE = 5
    time = 7200
    total_score = 0
    cat_hunts = []
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
                    if can_return(start_point=start_point, current_point=current_point, end_point=point, time_left=time) and not check_if_crossing_paths(start_point=current_point, end_point=point, paths=cats_paths, cat_name = cat.name):
                        if value_ratio(current_point=current_point, end_point=point, cat=cat) > value_ratio(current_point=current_point, end_point=next_point, cat=cat):
                            next_point = point
            # tutaj else i zwiększanie zasięgu poszukiwań jeżeli nic nie znalazł
            if next_point:
                current_hunt.append(next_point)
                time -= time_to_hunt(prey_type=next_point.type, start_point=current_point, end_point=next_point)
                hunt_count += 1
                points.remove(next_point)
            else:
                if len(current_hunt.points_list) > 1:
                    current_hunt, time = return_to_start(start_point=start_point, current_point=current_point, current_hunt=current_hunt, time=time)

        if len(current_hunt.points_list) > 1:
            cat_hunts.append(current_hunt)
            total_score += current_hunt.score
    return total_score, points, update_paths(cats_paths=cats_paths, cat_hunts=cat_hunts)

# Generate points as Prey objects, starting objects has type value of START
