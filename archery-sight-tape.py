from jinja2 import Template
from yamlarg import parse
from rich.traceback import install
install(show_locals=True)

class line:
    def __init__(self, value, x, y, color, offset, line_width):
        self.value = value
        self.y = y
        self.id = value
        self.texty = y + offset
        self.color = color
        self.x = x
        self.line_width = line_width


if __name__ == '__main__':
    template = Template(open('svg.template', 'r').read())

    args = parse('arguments.yaml')

    sight_settings = dict()
    with open(args['input'], 'r') as f:
        for row in f.readlines():
            distance, sight = row.split(',')
            sight_settings[int(distance)] = float(sight)

    height = round(args['height'] * args['ppi'])
    width = round(args['width'] * args['ppi'])

    numbers = list()
    small = list()
    medium = list()

    ppi = args['ppi']

    large_width_pct, medium_width_pct, small_width_pct = args['line_width'].split(',')
    large_width = (100 - int(large_width_pct))/100 * width
    medium_width = (100 - int(medium_width_pct))/100 * width
    small_width = (100 - int(small_width_pct))/100 * width

    large_color, medium_color, small_color = args['color'].split(',')

    large_weight, medium_weight, small_weight = args['line_weight'].split(',')

    start_offset = args['start'] * args['ppi']

    for k, v in sight_settings.items():
        y = (v * ppi) + start_offset

        if y < height:
            if k % 10 == 0:
                numbers.append(line(k, large_width, y, large_color, args['font_y_offset'], large_weight))
            elif k % 5 == 0:
                medium.append(line(k, medium_width, y, medium_color, args['font_y_offset'], medium_weight))
            else:
                small.append(line(k, small_width, y, small_color, args['font_y_offset'], small_weight))

    print(sight_settings)

    output = template.render(height=height, width=width, numbers=numbers, small=small, medium=medium, font_size=args['font_size'])
    with open(args['output'], 'w') as f:
        f.write(output)