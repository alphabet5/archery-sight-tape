from jinja2 import Template
from yamlarg import parse

class line:
    def __init__(self, value, y, color):
        self.value = value
        self.y = y
        self.id = value
        self.texty = y + 7
        self.color = color


if __name__ == '__main__':
    template = Template(open('svg.template', 'r').read())

    args = parse('arguments.yaml')

    sight_settings = dict()
    with open('sight-settings.csv', 'r') as f:
        for row in f.readlines():
            distance, sight = row.split(',')
            sight_settings[int(distance)] = float(sight)

    height = round(args['height'] * args['ppi'])
    width = round(args['width'] * args['ppi'])

    numbers = list()
    small = list()
    medium = list()

    start_offset = args['start'] * args['ppi']

    for k, v in sight_settings.items():
        y = (v * args['ppi']) + start_offset
        if y < height:
            if k % 10 == 0:
                numbers.append(line(k, y, args['large_color']))
            elif k % 5 == 0:
                medium.append(line(k, y, args['medium_color']))
            else:
                small.append(line(k, y, args['small_color']))

    print(sight_settings)

    output = template.render(height=height, width=width, numbers=numbers, small=small, medium=medium)
    with open(args['output'], 'w') as f:
        f.write(output)