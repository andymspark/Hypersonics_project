#include <vector>
#include <iostream>
#include <cmath>

void main() {
    // initial conditions
    int L = 4;
    int N = 160;            
    int num_points = N + 1;
    double dx = static_cast<double>(L) / static_cast<double>(N); // dx=1/40

    double c = 0.8;     //CFL number(0<c<1)
    double T = 2.4;
    double dt = c * dx;     //dt=0.02
    int num_steps = static_cast<int>(std::round(T / dt)) + 1;       //num_steps=121/ std::round! if not num_steps=120

    std::vector<std::vector<double>> u(num_steps, std::vector<double>(num_points, 0));     //first row is initial condtition
    int row_count = u.size();
    int col_count = u[0].size();

    

    //initial condition verification
    // std::cout << "dx = " << dx << std::endl;
    // std::cout << "dt = " << dt << std::endl;
    // std::cout << "num_steps = " << num_steps << std::endl;
    // std::cout << "num_row = " << row_count << std::endl;
    // std::cout << "num_col = " << col_count << std::endl;

    // for (int i = 0; i < num_steps; i++) {
    //     for (int j = 0; j < num_points; j++) {
    //         std::cout << u[i][j] << " ";
    //     }
    //     std::cout << "\n";
    // }



}