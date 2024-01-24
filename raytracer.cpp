#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <cmath>

void read_file(std::string input_file);

int main(int argc, char* argv[]){
    std::string input_file = argv[1];
    read_file(input_file);

    return 0;
}

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