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
        self.eye = np.array(eye)
        self.direction = np.array(direction)
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

def raytrace(currentRay: Ray):
    # if (currentRay.depth > 3):
    #     return np.array([0,0,0])
    intersect = closest_intersect(currentRay, spheres)
    if intersect is not None:
        return intersect.color
        print("intersect made, setting color to current sphere color")
    else:
        return background_color

def closest_intersect(currentRay: Ray, spheres_list):
    # closest_intersect = float("inf")
    # closest_sphere: Ray
    count = 1
    for sphere in spheres_list:
        # print("printing sphere " + str(count))
        eye_minus_center = currentRay.eye - sphere.position

        # Calculate A,B,C values
        A = np.dot(currentRay.direction, currentRay.direction)
        B = 2.0 * np.dot(currentRay.direction, eye_minus_center)
        C = np.dot(eye_minus_center, eye_minus_center) - 1

        # Solve for the discriminant, 
        discriminant = B**2 - (A*C)
        if (discriminant < 0 or discriminant == 0):
            return None
        discriminant = np.sqrt(B**2 - (A*C))

        t1 = (-B/A) + (discriminant/A)
        t2 = (-B/A) - (discriminant/A)

        if (t1>0):
            return sphere
        if (t2>0):
            return sphere
        count=+1
    return None
    

def main():
    parse_info()

    # For image plane settup
    W = resolution[1]/2
    H = resolution[0]/2

    eye = np.array([0,0,-5])
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
            uc = -W + (W * (2*pixel_column)/(resolution[0]))
            vr = -H + (H * (2*pixel_row)/(resolution[1]))

            # Pixel in image plane relative to camera coordinate system
            pixel_in_camera = eye - near*n + uc*u + vr*v

            # Create current ray
            curr_ray = Ray(eye, pixel_in_camera - eye, 0)
            curr_ray.set_depth(1)

            # curr_pixel_color = raytrace()
            colorCR = raytrace(curr_ray)
            color = colorCR * 255
            image[pixel_row, pixel_column] = color  # Set current pixel color

    output_ppm(output_name, image)


if __name__ == "__main__":
    main()