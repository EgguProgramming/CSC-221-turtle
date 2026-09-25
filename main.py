# Name: Melody
# Status: Complete
# This program uses the turtle library to draw a set of points onto a window.
# The program is configured to draw the python snakes and their eyes.
import turtle
import math

# main will act as the init function. This starts the drawing sequence and will
# keep the program running when it's done drawing
def main():
    #show the window
    turtle.showturtle()

    draw_snakes()

    # keep the window open when the art is done
    while True:
        # Show the turtle
        turtle.showturtle()

# These are the points of each object drawn
python_blue_snake_point_array = [[-4.55,0.5],[-4.4,1.6],[-4.,2.4],[-3.2,2.7],[-0.2,2.7],[-0.2,3],[-2.3,3],[-2.3,4],[-2,4.6],[-1,4.95],[-0.2,5],[0.7,4.95],[1.6,4.6],[1.95,4],[1.95,2],[1.9,1.5],[1.65,1],[1,0.7],[-1.2,0.7],[-2,0.4],[-2.55,-0.6],[-2.55,-1.6],[-3.4,-1.6],[-3.9,-1.4],[-4.3,-0.8],[-4.475,-0.2]] # coordinates for the points of the blue snake
python_yellow_snake_point_array = [[4, -0.7], [4.2,0.5],[4, 1.8],[3.6, 2.5],[3,2.7],[2.2, 2.7],[2.2,1.4],[1.7,0.7],[1,0.4],[-1,0.4],[-1.9,0.2],[-2.3,-0.6],[-2.3,-3],[-1.8,-3.5],[-1.15, -3.75],[0,-4],[1,-3.75],[1.5, -3.5],[2,-3],[2, -1.9],[-0.2,-1.9], [-0.2, -1.6],[3, -1.6],[3.6,-1.4]] # coordinates for the points of the yellow snake
python_snake_eyes = [[1.04, -2.8], [-1.35, 3.94]] # coordinates for the eyes of the snakes

multiply_size = 50 # this will shrink and grow the size of the art

current_art_to_trace = None # this is a tracker so that some functions don't need an extra argument


# this function will merely control the sequence of events in which the
# snakes are drawn.
def draw_snakes():
    # draw the bodies
    move_turtle_to_new_image(python_blue_snake_point_array)
    move_turtle_to_new_image(python_yellow_snake_point_array)

    # draw the eyes
    draw_snake_eyes(0)
    draw_snake_eyes(1)

    # move_turtle_to_new_image(square)

# this will draw a snake's eye based on a passed index.
def draw_snake_eyes(eye_index : int):
    global current_art_to_trace

    turtle.penup()
    current_art_to_trace = python_snake_eyes
    move_turtle_to_point(eye_index)

    turtle.pendown()
    turtle.circle(0.28*multiply_size)

# This will make the turtle move to draw a new image.
def move_turtle_to_new_image(image_to_draw : list):
    global current_art_to_trace

    current_art_to_trace = image_to_draw
    # Get it ready to draw by moving it to the first point
    first_move_turtle_to_new_image()
    # draw the rest of the points
    for point_index in range(1, len(image_to_draw)):
        move_turtle_to_point(point_index)
    # move it back to the first point so that it closes
    move_turtle_to_point(0)

# merely lift the pen, move, drop the pen.
def first_move_turtle_to_new_image():
    turtle.penup()
    move_turtle_to_point(0)
    turtle.pendown()

# from a passed index, use functions to move the turtle to a point
def move_turtle_to_point(point_index : int):
    next_angle = get_angle_between_turtle_and_point(point_index) # the angle between the next point and the turtle

    # decide if the turtle will move left or right, based on which is faster
    if next_angle > 180:
        turtle.left(360-next_angle)
    else:
        turtle.right(next_angle)
    turtle.forward(get_distance_to_point(point_index))

# from a passed index, get the angle between the turtle and a next point
def get_angle_between_turtle_and_point(next_point_index : int):
    # getting the Arctangent of a line's slope will give you the angle the
    # line is rotated by. math.atan2 allows you to do this with the x and y of 2 points
    # subtracting the turtle's position via (b.y - a.y), (b.x - a.x) normalizes it
    turtle_point = [turtle.pos()[0], turtle.pos()[1]] # position of the turtle, normalized against scaling
    next_point = [current_art_to_trace[next_point_index][0] * multiply_size,current_art_to_trace[next_point_index][1] * multiply_size] # the position of the next point
    rise = next_point[0] - turtle_point[0] # delta y
    run = next_point[1] - turtle_point[1] # delta x
    # math.atan has a default output of the radians unit. Turtle uses degrees so
    # we must convert.
    global_angle = math.degrees(math.atan2(rise, run)) # angle between turtle and the next point

    #arctangent is designed for unit circle angles, while turtle uses cartesian angles.
    # additionally, the turtle needs to know how much to turn - now where to turn to.
    return  unit_angle_to_cartesian_angle(turtle.heading()+global_angle)

# this function, given a passed angle, will translate from unit to cartesian
def unit_angle_to_cartesian_angle(angle : float):
    # cartesian angles are offset by 90 degrees
    return_angle = (angle-90) # the angle that will be returned
    if return_angle < 0:
        # if the angle is below zero, make it above zero by adding 360 as many
        # times as needed
        return_angle += (360*math.floor(1+(return_angle/-360)))
    if return_angle > 360:
        # if the angle is above 360, make it below 360 by subtracting as many times as
        # needed
        return_angle -= (360*math.floor(return_angle/360))
    return return_angle

# given an index, find the distance between the turtle and a point
def get_distance_to_point(next_point_index : int):
    turtle_point = [turtle.pos()[0], turtle.pos()[1]] # the position of the turtle, normalized against scaling
    next_point = [current_art_to_trace[next_point_index][0] * multiply_size,current_art_to_trace[next_point_index][1] * multiply_size] # position of the next point

    # the formula for getting distance between points is
    # sqrt(((b.x-a.x)^2) + ((bturtle_left_turn_angle.y - a.y)^2))
    # We'll define this as relative_x, and relative_y, then do the math
    relative_x = (next_point[0] - turtle_point[0])**2 # relative position of the next point's x
    relative_y = (next_point[1] - turtle_point[1])**2 # relative position of the next point's y

    return math.sqrt(relative_x + relative_y)

# This line will run the initialization function only if the script is being run
# as the main program.
if __name__ == '__main__':
    main()
