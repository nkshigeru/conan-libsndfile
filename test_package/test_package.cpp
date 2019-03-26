#include <iostream>
#include <sndfile.h>

int main() {
    std::cout << "libsndfile version: " << sf_version_string() << std::endl;
}
