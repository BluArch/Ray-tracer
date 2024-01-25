#include <iostream>
#include <sstream>
#include <fstream>
#include <vector>
#include <string>

class Matrix{
    public:
        std::vector<std::vector<int> > matrix;

    Matrix(int x, int y, int z) : matrix(3, std::vector<int>(3,0)){
        matrix[0][0] = x;
        matrix[1][1] = y;
        matrix[2][2] = z;
    }
    void set_Position(int row, int column, int value){
        matrix[row][column] = value;
    }
};

class Sphere{
   public:
        std::string name;
        std::vector<int> position;
        Matrix scale;
        std::vector<int> color;
        std::vector<int> coefficients;
        std::vector<int> shine;

        Sphere(std::string new_name, int x, int y, int z, int scalex, int scaley, int scalez,
                int r, int g, int b, int rA, int rD, int rS, int shine_value) :
                name(new_name), position({x,y,z}), scale({scalex,scaley,scalez}), color({r,g,b}),
                coefficients({rA,rD,rS}), shine({shine_value}){}
};

class Light{
    public:
        std::string name;
        std::vector<int> position;
        std::vector<int> color;

        Light(std::string new_name, int x, int y, int z, int r, int g, int b):
                name(new_name), position({x,y,z}), color({r,g,b}){}
};

class Ray{
    public:
        std::vector<int> eye;
        std::vector<int> direction;
        int depth;

        Ray(int x, int y, int z, int directionx, int directiony, int directionz, int starting_depth) :
            eye({x,y,z}), direction({directionx,directiony,directionz}), depth(starting_depth){}
};

void read_file(std::string input_file){

    std::fstream input;
    input.open(input_file, std::ios::in);
    if(input.is_open()){
        std::string line;
        while(std::getline(input, line)){
            std::cout << line << "\n";
        }
    }
    input.close();
}   

std::vector<Sphere> get_Spheres(std::string input_file){
    std::vector<Sphere> spheres;
    std::fstream input;
    input.open(input_file, std::ios::in);
    if(input.is_open()){
        std::string line;
        while(std::getline(input, line)){
            std::istringstream iss(line);
            std::string cur_word;
            while(iss>>cur_word){
                std::cout<<cur_word<<"\n";
            }
        }
    }
    input.close();
    return spheres;
}

int main(int argc, char* argv[]){
    std::string input_file = argv[1];
    get_Spheres(input_file);

    return 0;
}