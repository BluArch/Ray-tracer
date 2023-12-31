import sys
import numpy as np

near = None
left = None
right = None
bottom = None
top = None
output_name = None

class Sphere:
    """
    Class stores the values of a sphere in the scene
    """
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
    """
    Class stores the values of a light in the scene
    """
    def __init__(self, name: str, position: list, color: list):
        self.name = name
        self.position = np.array(position)
        self.color = np.array(color)

class Ray:
    """
    Class stores the values of a ray in the scene. Depth of the ray can be updated with set_depth
    """
    def __init__(self, eye, direction, depth):
        self.eye = np.array(eye)
        self.direction = np.array(direction)
        self.depth = depth
    
    def set_depth(self, new_depth):
        self.depth = new_depth

def parse_info():
    """
    Takes input from command line and stores values in variables and objects of the scene
    """
    global near, left, right, bottom, top, output_name

    spheres = []
    lights = []
    ambient = None
    background_color = None
    resolution = None

    testcaseFile = sys.argv[1]  
    
    with open(testcaseFile, 'r') as file:
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
        return spheres, lights, ambient, background_color, resolution


def normalize(vector: np.array):
    """
    Function normalizes a given vector and returns the normalized vector
    """
    return vector / np.linalg.norm(vector)

def inverse_by_scale(vector: np.array, scale: np.array):
    """
    Function computes the dot product of a vector and a matrix, scales the vector by the inverse of the scaling matrix
    """
    inverse_scale =  np.linalg.inv(scale)
    return np.dot(vector, inverse_scale)

def inverse_transpose(vector: np.array, scale: np.array):
    """
    Function computes the inverse transpose of a vector by a given scale
    """
    inverse = np.linalg.inv(scale)
    inverseTranspose = np.linalg.inv(scale).T

    result = np.dot(inverseTranspose, np.dot(inverse, vector))
    return result


def raytrace(currentRay: Ray, objects: list, light_sources: list, ambient_light: list, background: np.array):
    """
    Function goes through the raytracing process for a given pixel, maximum 3 bounces
    """
    # If we've reached max depth, return black
    if (currentRay.depth > 3):
        return np.array([0,0,0])
    
    # Search for whether there is a closest object to intersect with
    closest_object, closest_distance, t_inside = find_closest_intersection(currentRay, objects)

    # If no object, return background color
    if (closest_object is None):
        return background
    
    P = currentRay.eye + closest_distance*currentRay.direction
    p_normal = P-closest_object.position
    p_normal = inverse_transpose(p_normal, closest_object.scale)
    p_normal = normalize(p_normal)
    P = P + 0.00001 * p_normal
    if (t_inside == 1):
        p_normal = -p_normal
    
    # Compute ambient lighting + lighting from lights
    clocal = color_from_lights(currentRay.eye, P, p_normal, closest_object, objects, ambient_light, light_sources, t_inside)

    reflected_direction = -2 * np.dot(p_normal, currentRay.direction)*p_normal + currentRay.direction
    reflected_ray = Ray(P, reflected_direction, currentRay.depth + 1)

    colorRE = raytrace(reflected_ray, objects, light_sources, ambient_light, background)
    if np.allclose(colorRE, background):
        colorRE = np.array([0.0,0.0,0.0])
    pixel_color = clocal + colorRE*closest_object.coefficients[3]
    return pixel_color
    

def color_from_lights(eye: np.array, point: np.array, normal: np.array, object: Sphere, objects: list, Ka, light_sources: list, tnum):
    """
    Function returns the sum of all lighting from lights using ADS model
    """
    # Get vector from eye to point
    point_to_eye = normalize(eye - point)
    clocal = Ka * object.color * object.coefficients[0]

    for light in light_sources:
        # Get vector to current light from point
        point_to_light = normalize(light.position - point)
        # Convert light ray to Ray object to run find_closest_intersection on it
        light_ray = Ray(point, point_to_light, 0)

        _, closest_distance, _ = find_closest_intersection(light_ray, objects)
        distance_to_light = np.linalg.norm(light.position - point)

        if (distance_to_light > closest_distance or (tnum == 1 and light.position[2] <-near)):
            continue
        # Calculate diffuse value
        diffuse = object.coefficients[1] * light.color * np.dot(normal, point_to_light) * object.color
        # Calculate specular value
        R = 2.0*np.dot(normal, point_to_light)*normal - point_to_light
        specular = object.coefficients[2] * light.color * np.dot(R, point_to_eye)**object.shine

        clocal += diffuse + specular
    return clocal


def find_closest_intersection(curr_ray: Ray, objects: list):
    """
    Computes all intersections of a given ray with the objects in the scene.
    Return the closest object with the distance to the object
    """
    closest_object = None
    closest_distance = np.inf
    t_inside = None
    # Find intersection if it exists for each sphere, update closest_object/distance is closer than current values
    for curr_sphere in objects:
        t, inside = getDistance(curr_ray, curr_sphere)
        # Update values if closer
        if (t and t<closest_distance):
            closest_distance = t
            closest_object = curr_sphere
            t_inside = inside
    return closest_object, closest_distance, t_inside

def getDistance(ray, sphere):
    """
    Function returns the distance to an intersect point if an intersect exists
    """
    eye_minus_center = ray.eye - sphere.position
    # Get the scaled value of the ray and vector from eye to circle center
    curr_ray_inverse = inverse_by_scale(ray.direction, sphere.scale)
    eye_center_inverse = inverse_by_scale(eye_minus_center, sphere.scale)
    # Solve for a, b, and c values
    a = np.dot(curr_ray_inverse, curr_ray_inverse)
    b = 2 * np.dot(curr_ray_inverse, eye_center_inverse)
    c = np.linalg.norm(eye_center_inverse)**2 - 1
    # Find the number of intersections
    discriminant = b**2 - 4*a*c
    if(discriminant>0):
        discriminant = np.sqrt(discriminant)
        t1 = (-b + discriminant) / (a*2)
        t2 = (-b - discriminant) / (a*2)
        if (t1>0 and t2>0):
            if (t1<=near or t2<=near):
                return max(t1,t2), 1
            return min(t1,t2), 0
    return None, None

def main():
    """
    Stores variables from .txt file and generates rays to iterate through every pixel of the image plane, writing pixel colors to .ppm file
    """
    objects, light_sources, ambient_lights, backgroundC, resolution = parse_info()

    eye = np.array([0,0,0])

    with open(output_name, 'w') as ppm_file:
        ppm_file.write("P3\n")
        ppm_file.write(f"{resolution[1]} {resolution[0]}\n")
        ppm_file.write("255\n")
        for pixel_row in range(resolution[1]):
            for pixel_column in range(resolution[0]):
            
                uc = left + (right*(2*pixel_column)/(resolution[1]))
                vr = top + (bottom*(2*pixel_row)/(resolution[0]))
                
                pixel = np.array([uc,vr,-near])
                direction = normalize(pixel - eye)
                
                color = raytrace(Ray(eye, direction, 1), objects, light_sources, ambient_lights, backgroundC)
                scaled_pixel = (color * 255).astype(int)
                ppm_file.write(f"{scaled_pixel[0]} {scaled_pixel[1]} {scaled_pixel[2]} ")
            ppm_file.write("\n")

if __name__ == "__main__":
    main()