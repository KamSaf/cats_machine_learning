import random
import ast

random.seed(10)


class Point:
    def __init__(self, x=0, y=0, coordinates_tuple=None):
        if coordinates_tuple:
            self.x = coordinates_tuple[0]
            self.y = coordinates_tuple[1]
        else:
            self.x = x
            self.y = y

    def __str__(self):
        return f'({self.x}, {self.y})'

    def save_to_file(points_list=[], path_list=[], output_file_path=None):
        file_path = output_file_path if output_file_path else 'coordinates.cf'
        file = open(file_path, 'w')

        file.write(f'{len(points_list)}\n')
        for point in points_list:
            file.write(str(point) + '\n')

        file.write(f'\n{len(path_list)}\n')
        for path in path_list:
            file.write(str(path))
        file.close()

    def read_from_file(input_path):
        file = open(input_path)
        data = {
            'points_number': 0,
            'paths_number': 0,
            'points': [],
            'paths': [],
        }

        lines = file.readlines()
        file.close()
        data['points_number'] = int(lines[0])
        for i in range(1, data['points_number']+1):
            data['points'].append(ast.literal_eval(lines[i]))

        data['paths_number'] = int(lines[data['points_number']+2])
        for i in range(data['points_number']+3, len(lines)):
            path = lines[i]
            data['paths'].append(Path.string_to_list(path_scheme=path[:path.index(':')], path_length=float(path[path.index(':')+1:])))
        return data

    def generate_coordinates(points_number=0):
        points = [Point(x=round(random.uniform(1.0, 50.0), 2), y=round(random.uniform(0.0, 50.0), 2)) for i in range(points_number)]
        return points


class Path:
    def __init__(self, steps=[], path_length=None):
        self.steps = steps
        self.path_length = path_length

    def __str__(self):
        output = ''
        for index, step in enumerate(self.steps):
            if index != 0:
                output += '>'
            output += str(step)
        output += f':{self.path_length}\n'
        return output

    def add(self, step):
        self.steps.append(step)

    def string_to_list(path_scheme, path_length):
        steps = path_scheme.split('>')
        return Path(list(map(ast.literal_eval, steps)), path_length)


# while (True):
#     user_input = input('Type SAVE to save data to a file, type LOAD to load data from a file\n')

#     if user_input == "SAVE":
#         points_list = Point.generate_coordinates(25)
#         available_points = [x for x in range(25)]
#         paths_list = []

#         for i in range(5):
#             steps_list = []
#             for j in range(5):
#                 index = random.choice(available_points)
#                 steps_list.append(points_list[index])
#                 available_points.remove(index)
#             paths_list.append(Path(steps=steps_list, path_length=16.10)) # currently path_length has a placeholder value

#         Point.save_to_file(points_list=points_list, path_list=paths_list)
#         print("Coordinates saved to a file")
#     else:
#         data = Point.read_from_file(input_path='coordinates.cf')
#         print('POINTS NUMBER:' + str(data['points_number']) + '\n' + 'PATHS NUMBER:' + str(data['paths_number']) + '\n' + '\n\nPOINTS:')
#         for p in data['points']:
#             print(p)
#         print('\n\nPATHS:')
#         for p in data['paths']:
#             print(p)
