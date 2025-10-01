#include <vector>
#include <iostream>
#include <cmath>

int main() {

    int N = 10;
    int num_points = N + 1;
    double h = 1.0/static_cast<double>(N);

    double u_0 = 1.0;

    std::vector<double> u(num_points, 0.0);
    std::vector<double> x(num_points, 0.0);
    
    u[0] = u_0;
    x[0] = 0.0;
    for (int i = 1; i < num_points; i++) {
        u[i] = (1.0 + h) * u[i-1];
        x[i] = h * i;
        std::cout << "current x =" << x[i] << std::endl;
    }

    std::cout << "u(x=1) = " << u[num_points-1] << std::endl;
    std::cout << "exact u(x=1) = " << std::exp(1.0) << std::endl;
    return 0;
}