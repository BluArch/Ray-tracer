import sys
import numpy as np

near = None
left = None
right = None
bottom = None
top = None
resolution = []
background_color = np.array([])
ambient = np.array([])
spheres = []
lights = []
output_name = None


class Sphere:
    def __init__(self, name, position, scale, color, coefficients, shine):
        self.name = name
        self.position = np.array(position)
        self.scale = np.array(scale)
        self.color = np.array(color)
        self.coefficients = np.array(coefficients)
        self.shine = shine

class Light:
    def __init__(self, name, position, color):
        self.name = name
        self.position = np.array(position)
        self.color = np.array(color)

class Ray:
    def __init__(self, eye, direction, depth):
        self.eye = eye
        self.direction = direction
        self.depth = depth
    
    def set_depth(self, new_depth):
        self.depth = new_depth


def parse_info():
    # Takes input from command line for the variables of the scene
    # Will create objects for Lights and Spheres
    global near, left, right, bottom, top, resolution, spheres, lights, background_color, ambient, output_name

    testcaseFile = sys.argv[1]  
    file = open(testcaseFile, 'r')
    
    for line in file:
        values = line.split()

        # If current line is empty, skip it
        if not values:
            continue
        
        # Continue parsing
        if (values[0] == "NEAR"):
            near = float(values[1])
        elif (values[0] == "LEFT"):
            left = float(values[1])
        elif (values[0] == "RIGHT"):
            right = float(values[1])
        elif (values[0] == "BOTTOM"):
            bottom = float(values[1])
        elif (values[0] == "TOP"):
            top = float(values[1])
        elif (values[0] == "RES"):
            resolution = [int(values[1]), int(values[2])]
        elif (values[0] == "SPHERE"):
            spheres.append(Sphere(str(values[1]), 
                                (float(values[2]), float(values[3]), float(values[4])), 
                                (float(values[5]), float(values[6]), float(values[7])),
                                (float(values[8]), float(values[9]), float(values[10])),
                                (float(values[11]), float(values[12]), float(values[13]), float(values[14])),
                                 float(values[15])))
        elif (values[0] == "LIGHT"):
            lights.append(Light(str(values[1]),
                        (float(values[2]), float(values[3]), float(values[4])), 
                        (float(values[5]), float(values[6]), float(values[7]))))
        elif (values[0] == "BACK"):
            background_color = np.array([float(values[1]), float(values[2]), float(values[3])])
        elif (values[0] == "AMBIENT"):
            ambient = np.array([float(values[1]), float(values[2]), float(values[3])])
        elif (values[0] == "OUTPUT"):
            output_name = str(values[1])

def output_ppm(filename, image):
    with open(filename, 'w') as output:

        output.write(f'P3\n{resolution[0]} {resolution[1]}\n255\n')
        # Write the pixel values in text format
        for column in range(resolution[0]):
            for row in range(resolution[1]):
                pixel = image[row, column]
                output.write(f'{pixel[0]} {pixel[1]} {pixel[2]} ')

            # Add a newline after each row
            output.write('\n')


def main():
    parse_info()

    eye = np.array([0,0,5])
    lookat = np.array([0,0,0])
    up = np.array([0,1,0])

    # Basis vector n
    N = eye - lookat
    n = eye / np.linalg.norm(N)
    # Basis vector u
    U = np.cross(up, n)
    u = U / np.linalg.norm(U)
    # Basis vector v
    v = np.cross(n, u)

    image = np.zeros((resolution[1], resolution[0], 3), dtype=np.uint8)

    for pixel_column in range(resolution[0]):
        for pixel_row in range(resolution[1]):
            # Finding lower left uc and vr values in camera coordinate system
            uc = -left + (left * (2*pixel_column)/(resolution[0]))
            vr = -right + (right * (2*pixel_row)/(resolution[1]))

            # Pixel in image plane relative to camera coordinate system
            pixel_in_camera = eye - near*n + uc*u + vr*v

            # Create current ray
            curr_ray = Ray(eye, pixel_in_camera - eye, 0)

            # curr_pixel_color = raytrace()
            backgroundcolor = background_color * 255
            image[pixel_row, pixel_column] = backgroundcolor  # Set current pixel color

    output_ppm(output_name, image)


if __name__ == "__main__":
    main()