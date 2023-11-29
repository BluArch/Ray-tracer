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
        self.scale = np.array(scale)
        
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


def raytrace(currentRay: Ray):
    if (currentRay.depth > 3):
        return np.array([0,0,0])
    closest_object, closest_distance = find_closest_intersection(currentRay)
    if (closest_object is None):
        return background_color
    return closest_object.color
    
def find_closest_intersection(curr_ray):
    # Keep track of closest object and the distance to it
    closest_object = None
    closest_distince = np.inf
    for curr_sphere in spheres:
        t = find_intersection(curr_ray, curr_sphere)
        if (t and t<closest_distince):
            closest_distince = t
            closest_object = curr_sphere
    return closest_object, closest_distince

def find_intersection(curr_ray: Ray, sphere: Sphere):
    eye_minus_center = curr_ray.eye - sphere.position

    a = np.dot(curr_ray.direction, curr_ray.direction)
    b = 2 * np.dot(curr_ray.direction, eye_minus_center)
    c = np.linalg.norm(eye_minus_center)**2 - 1

    discriminant = b**2 - 4*a*c
    print(discriminant)
    if(discriminant>0):
        t1 = (-b + np.sqrt(discriminant)) / (a*2)
        t2 = (-b - np.sqrt(discriminant)) / (a*2)
        if (t1>0 and t2>0):
            return min(t1, t2)
    else:
        return None


def main():
    parse_info()
    # For image plane settup
    eye = np.array([0,0,near])
    ratio = float(resolution[0])/resolution[1]
    screen = (left, top/ratio, right, bottom/ratio)

    W = resolution[1]/2
    H = resolution[0]/2

    # Fill out an empty canvas
    image = np.zeros((resolution[1], resolution[0], 3))
    for pixel_column in range(resolution[0]):
        for pixel_row in range(resolution[1]):
            # # Finding lower left uc and vr values in camera coordinate system
            uc = -W + (W * (2*pixel_column)/(resolution[0]))
            vr = -H + (H * (2*pixel_row)/(resolution[1]))
            # Pixel in image plane relative to camera coordinate system
            pixel = np.array([uc,vr,0])
            ray_shot = normalize(pixel-eye)
            # Create current ray
            curr_ray = Ray(eye, ray_shot,0)
            curr_ray.set_depth(1)
            # curr_pixel_color = raytrace()
            colorCR = raytrace(curr_ray)
            # clamp between 0 and 1
            # scale by 255
            color = colorCR * 255
            # Set current pixel color
            image[pixel_row, pixel_column] = np.clip(color,0,1)
    plt.imsave(output_name, image)


if __name__ == "__main__":
    main()