import sys
import numpy

near = None
left = None
right = None
bottom = None
top = None
resolution = [None, None]
background_color = [None, None, None]
ambient = [None, None, None]
output_name = None
spheres = [None]
lights = [None]


class Sphere:
    def __init__(self, name, position, scale, color, coefficients, shine):
        self.name = name
        self.position = position
        self.scale = scale
        self.color = color
        self.coefficients = coefficients
        self.shine = shine

class Light:
    def __init__(self, name, position, color):
        self.name = name
        self.position = position
        self.color = color

def parse_info():
    global near, left, right, bottom, top, resolution, spheres, lights, background_color, ambient, output_name
    
    testcaseFile = sys.argv[1]  
    file = open(testcaseFile, 'r')

    for line in file:
        values = line.split()
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
            background_color = [float(values[1]), float(values[2]), float(values[3])]
        elif (values[0] == "AMBIENT"):
            ambient = [float(values[1]), float(values[2]), float(values[3])]
        elif (values[0] == "OUTPUT"):
            output_name = str(values[1])

def main():
    parse_info()
    print(resolution)

if __name__ == "__main__":
    main()