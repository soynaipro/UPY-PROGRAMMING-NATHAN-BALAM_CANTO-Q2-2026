import pygame

#config
config = {}
with open ('config.txt','r') as file:
    for line in file:
        parameter, value = line.strip().split('=')
        if ',' in value:
            config[parameter] = tuple(int(c.strip()) for c in value.split(','))
        elif '.' in value:
            config[parameter] = float(value)
        else:
            config[parameter] = int(value)

vanishing_point =(config['width'] *0.5, config['height'] * 0.25)

#launcher
pygame.init()
screen = pygame.display.set_mode((config['width'],config['height']))

def calculate_x_position(surface, vertical_lines, space):
    x_positions = []
    width = surface.get_width()
    spacing = space * width
    central_line = width / 2
    offset = -int(vertical_lines / 2)

    for _ in range(vertical_lines):
        x_positions.append(central_line + offset * spacing)
        offset += 1

    return x_positions

def calculate_y_position(surface, horizontal_lines):
    y_positions = []
    height = surface.get_height()
    spacing = height / (horizontal_lines + 1)

    for _ in range(1, horizontal_lines + 1):
        y_positions.append( _ * spacing)

    return y_positions

def draw_vertical_lines(surface, x_positions, color, width = 2):
    height = surface.get_height()

    for x in x_positions:
        pygame.draw.line(surface, color, (x,0),(x,height),width)

def draw_horizontal_lines(surface, x_positions, y_positions, color, width = 2):
    for y in y_positions:
        start_point = (x_positions[0],y)
        end_point = (x_positions[-1],y)
        pygame.draw.line(surface, color, start_point, end_point, width)


def draw_perspective_vertical_lines(surface, x_positions, vanishing_point, color, width = 2):
    for x in x_positions:
        pygame.draw.line(surface, color, vanishing_point,(x,surface.get_height()), width)


def draw_perspective_horizontal_lines(surface, x_positions, y_positions, vanishing_point, color, width = 2):
    height = surface.get_height()
    start_point = vanishing_point

    diagonal_1 = (start_point, (x_positions[0], height))
    diagonal_2 = (start_point, (x_positions[-1],height))

    for y in y_positions:
        if y > vanishing_point[1]:
            point_1 = (x_positions[0],y)
            point_2 = (x_positions[-1],y)

            h_line = (point_1, point_2)

            intersection_1 = find_intersection(diagonal_1,h_line)
            intersection_2 = find_intersection(diagonal_2,h_line)

            pygame.draw.line(surface, color, intersection_1, intersection_2, width)

def find_intersection(line_1, line_2):

#find intersections between 2 lines

    star_point_line_1, end_point_line_1 = line_1
    star_point_line_2, end_point_line_2 = line_2
    x1, y1 = star_point_line_1
    x2, y2 = end_point_line_1
    x3, y3 = star_point_line_2
    x4, y4 = end_point_line_2

    dominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    common_factor_a = x1 * y2 - y1 * x2
    common_factor_b = x3 * y4 - y3 * x4

    if dominator == 0:
        return  None

    intersection_x = (common_factor_a * (x3-x4)-(x1-x2)*common_factor_b)/dominator
    intersection_y = (common_factor_a * (y3-y4)-(y1-y2)*common_factor_b)/dominator

    return (intersection_x, intersection_y)

def non_linear_spacing(surface, y_positions, vanishing_point, power=2.0):
    height = surface.get_height()
    v_y = vanishing_point[1]
    available_height = height - v_y
    y_curved = []

    for  y in y_positions:
        t = (y - v_y)/available_height
        new_y = v_y + available_height * t **power
        y_curved.append(new_y)

    return y_curved

#main loop

x_positions = calculate_x_position(
    surface = screen,
    vertical_lines = config['vertical_lines'],
    space = config ['space']
)

print(x_positions)

y_positions = calculate_y_position(
    surface = screen,
    horizontal_lines = config['horizontal_lines']
)

y_curved = non_linear_spacing(
    surface = screen,
    y_positions = y_positions,
    vanishing_point = vanishing_point
)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(config['bg_color'])
    # draw_vertical_lines(screen, x_positions, config['line_color'])
    # draw_horizontal_lines(screen, x_positions, y_positions, config['line_color'], width=2)
    draw_perspective_vertical_lines(screen, x_positions, vanishing_point, config['line_color'])
    # draw_perspective_horizontal_lines(screen, x_positions, y_positions, vanishing_point, config['line_color'], width = 2)
    draw_perspective_horizontal_lines(screen, x_positions, y_curved, vanishing_point, config['line_color'], width=2)
    pygame.display.flip()

pygame.quit()