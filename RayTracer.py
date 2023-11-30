import sys
import numpy as np
import matplotlib.pyplot as plt

near = None
left = None
right = None
bottom = None
top = None

resolution = []
background_color = np.array([])
ambient = []
spheres = []
lights = []
output_name = None

class Sphere:
    def __init__(self, name: str, position: list, scale: list, color: list, coefficients: list, shine: float):
        self.name = name
        self.position = np.array(position)
        self.scale = np.array([[scale[0], 0, 0],
                              [0, scale[1], 0],
                              [0, 0, scale[2]]])
        self.color = np.array(color)
        self.coefficients = np.array(coefficients)
        self.shine = shine

class Light:
    def __init__(self, name: str, position: list, color: list):
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
            spheres.append(Sphere(str(values[1]), [float(values[2]), float(values[3]), float(values[4])], [float(values[5]), float(values[6]), float(values[7])],[float(values[8]), float(values[9]), float(values[10])], [float(values[11]), float(values[12]), float(values[13]), float(values[14])], float(values[15])))
        elif (values[0] == "LIGHT"):
            lights.append(Light(str(values[1]), [float(values[2]), float(values[3]), float(values[4])], [float(values[5]), float(values[6]), float(values[7])]))
        elif (values[0] == "BACK"):
            background_color = np.array([float(values[1]), float(values[2]), float(values[3])])
        elif (values[0] == "AMBIENT"):
            ambient = [float(values[1]), float(values[2]), float(values[3])]
        elif (values[0] == "OUTPUT"):
            output_name = str(values[1])


def normalize(vector):
    return vector / np.linalg.norm(vector)

def inverse_by_scale(vector, scale):
    inverse_scale =  np.linalg.inv(scale)
    return np.dot(vector, inverse_scale)

def raytrace(currentRay: Ray):
    # If we've reached max depth, return black
    if (currentRay.depth > 3):
        return np.array([0,0,0])
    # Search for whether there is a closest object to intersect with
    closest_object, closest_distance = find_closest_intersection(currentRay)
    # If no object, return background color
    if (closest_object is None):
        return background_color
    # Calculates intersect point of minimum distance object
    P = currentRay.eye - closest_distance*currentRay.direction


    return closest_object.color
    
def find_closest_intersection(curr_ray):
    # Keep track of closest object and the distance to it
    closest_object = None
    closest_distance = np.inf
    for curr_sphere in spheres:
        eye_minus_center = curr_ray.eye - curr_sphere.position

        curr_ray_inverse = inverse_by_scale(curr_ray.direction, curr_sphere.scale)
        eye_center_inverse = inverse_by_scale(eye_minus_center, curr_sphere.scale)

        a = np.dot(curr_ray_inverse, curr_ray_inverse)
        b = 2 * np.dot(curr_ray_inverse, eye_center_inverse)
        c = np.linalg.norm(eye_center_inverse)**2 - 1

        discriminant = b**2 - 4*a*c
        if(discriminant>0):
            discriminant = np.sqrt(discriminant)
            t1 = (-b + discriminant) / (a*2)
            t2 = (-b - discriminant) / (a*2)
            if (t1>0 and t2>0):
                t = min(t1, t2)
            if (t1>0):
                t = t1
            else:
                t = t2
        else:
            t = None
        if (t and t<closest_distance):
            closest_distance = t
            closest_object = curr_sphere
    return closest_object, closest_distance


def main():
    parse_info()
    # For image plane settup
    eye = np.array([0,0,near])
    image = np.zeros((resolution[1], resolution[0], 3))

    for pixel_column in range(resolution[1]):
        for pixel_row in range(resolution[0]):
            uc = left + (right*(2*pixel_column)/(resolution[1]))
            vr = top + (bottom*(2*pixel_row)/(resolution[0]))

            pixel = np.array([uc,vr,0])
            direction = normalize(pixel - eye)

            color = raytrace(Ray(eye, direction, 1))
            image[pixel_row, pixel_column] = np.clip(color, 0, 1)
    plt.imsave(output_name, image)


if __name__ == "__main__":
    main()