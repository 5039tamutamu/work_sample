#include <stdio.h>
#include <math.h>

// 微分係数を計算する関数
double deriv(double (*f)(double), double x, double dx) {
    return (f(x + dx / 2) - f(x - dx / 2)) / dx;
}

// メイン関数
int main() {
    double x = 2.0; // 例として学生番号の下3桁が200の場合
    double dx, approx, exact, rel_error;
    double min_error = 1e10, max_error = -1e10;
    double min_dx, max_dx;
    
    printf("x = %f, f(x) = %f\n", x, cos(x));
    printf("dx          approx        exact         rel_error\n");

    for (int i = 1; i <= 12; i++) {
        dx = pow(10, -i);
        approx = deriv(cos, x, dx);
        exact = -sin(x);
        rel_error = fabs((approx - exact) / exact);
        printf("%1.1e   %f   %f   %e\n", dx, approx, exact, rel_error);
        
        if (rel_error < min_error) {
            min_error = rel_error;
            min_dx = dx;
        }
        if (rel_error > max_error) {
            max_error = rel_error;
            max_dx = dx;
        }
    }
    
    printf("相対誤差は，%1.1e で極小となり，その値は %e です\n", min_dx, min_error);
    printf("相対誤差は，%1.1e で最大となり，その値は %e です\n", max_dx, max_error);

    return 0;
}
