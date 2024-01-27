#include <iostream>
#include <sstream>
#include <fstream>
#include <vector>
#include <string>
#include <list>
#include <array>

class Matrix{
    public:
        std::vector<std::vector<float> > matrix;

    Matrix(float x, float y, float z) : matrix(3, std::vector<float>(3,0)){
        matrix[0][0] = x;
        matrix[1][1] = y;
        matrix[2][2] = z;
    }
    void set_Position(float row, float column, float value){
        matrix[row][column] = value;
    }
};

class Sphere{
   public:
        std::vector<float> position;
        Matrix scale;
        std::vector<float> color;
        std::vector<float> coefficients;
        std::vector<float> shine;

        Sphere(float x, float y, float z, float scalex, float scaley, float scalez,
                float r, float g, float b, float Ka, float Kd, float Ks, float Kr,float shine_value) :
                position({x,y,z}), scale({scalex,scaley,scalez}), color({r,g,b}),
                coefficients({Ka,Kd,Ks,Kr}), shine({shine_value}){}
};

class Light{
    public:
        std::vector<float> position;
        std::vector<float> color;

        Light(float x, float y, float z, float r, float g, float b):
                position({x,y,z}), color({r,g,b}){}
};

class Ray{
    public:
        std::vector<float> eye;
        std::vector<float> direction;
        int depth;

        Ray(float x, float y, float z, float directionx, float directiony, float directionz, float starting_depth) :
            eye({x,y,z}), direction({directionx,directiony,directionz}), depth(starting_depth){}
};

std::array<float,14> store_line(std::string);

void parse_text_file(std::string input_file, std::list<Sphere>& spheres, std::list<Light>& lights){
/*
Function takes the name of an text file, opens it and reads each line. The values of the lines are stored in objects
TODO: Also have it take arrays for the background color, ambient color, and output filename
*/
    std::string name;
    std::fstream input;

    input.open(input_file, std::ios::in);
    if(input.is_open()){
        std::string line;
        while(std::getline(input, line)){
            std::array<float,14> curr_line;
            curr_line = store_line(line);
            if(curr_line[0]==1.0){
                spheres.push_back(Sphere(curr_line[1], curr_line[2], curr_line[3],curr_line[4],curr_line[5],curr_line[6],curr_line[7],
                curr_line[8],curr_line[9],curr_line[10],curr_line[11],curr_line[12],curr_line[13],curr_line[14]));
            }else if(curr_line[0]==2.0){
                lights.push_back(Light(curr_line[1],curr_line[2],curr_line[3],curr_line[4],curr_line[5],curr_line[6]));
            }
        }
    }
    input.close();
}

std::array<float,14> store_line(std::string line){
/*
Function takes a string as input and returns an array of every word in the string.
TODO: have it return the background color, ambient lighting, and output name
*/
    std::istringstream iss(line);
    std::array<float,14> curr_line;
    std::string cur_word;
    float cur_num;
    int index=1;

    iss>>cur_word;
    // Determining if line stores info for a sphere or a light
    // TODO: CHECK FOR BACKGROUND COLOR AND AMBIENT COLOR
    if (cur_word == "SPHERE"){
        curr_line[0] = 1.0;
    }else if (cur_word == "LIGHT"){
        curr_line[0] = 2.0;
    }else{
        curr_line[0] = -1.0;
    }
    while(iss>>cur_word){
        if((curr_line[0]==1||curr_line[0]==2)&&index!=1){
            curr_line[index-1] = std::stof(cur_word);
        }
        index++;
    }
    return curr_line;
}

int main(int argc, char* argv[]){
/*
Will serve as the main function for the raytracer
TODO: have the intitial for loop for the raytracer in this function

OVERALL TODOS: split up classes and functions into seperate files, it'd be a good way to practice not having everything in one file
*/
    std::string input_file = argv[1];
    std::list<Sphere> spheres;
    std::list<Light> lights;
    parse_text_file(input_file, spheres, lights);
    return 0;
}