#include <iostream>
#include <string>
#include <yaml-cpp/yaml.h>

int main(int argc, char** argv) {
    // default config file
    std::string fname = "config.yaml";
    if(argc > 1) fname = argv[1];  // allow overriding from CLI

    // load YAML
    YAML::Node config = YAML::LoadFile(fname);

    // read values
    int nx = config["problem"]["nx"].as<int>();
    double final_time = config["problem"]["final_time"].as<double>();
    std::string scheme = config["scheme"]["name"].as<std::string>();
    double cfl = config["scheme"]["cfl"].as<double>();

    // print out what we read
    std::cout << "Running simulation with:" << std::endl;
    std::cout << "  nx          = " << nx << std::endl;
    std::cout << "  final_time  = " << final_time << std::endl;
    std::cout << "  scheme      = " << scheme << std::endl;
    std::cout << "  CFL         = " << cfl << std::endl;

    // pretend we run a simulation
    double dt = cfl * (1.0 / nx); // fake CFL condition
    int steps = static_cast<int>(final_time / dt);

    std::cout << "Computed dt = " << dt << ", steps = " << steps << std::endl;
    for(int n=0; n<steps; ++n) {
        std::cout << "Step " << n+1 << "/" << steps << " running with scheme " << scheme << std::endl;
    }

    return 0;
}
