#include <stdio.h>
#include <math.h>

// �����W�����v�Z����֐�
double deriv(double (*f)(double), double x, double dx) {
    return (f(x + dx / 2) - f(x - dx / 2)) / dx;
}

// ���C���֐�
int main() {
    double x = 2.0; // ��Ƃ��Ċw���ԍ��̉�3����200�̏ꍇ
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
    
    printf("���Ό덷�́C%1.1e �ŋɏ��ƂȂ�C���̒l�� %e �ł�\n", min_dx, min_error);
    printf("���Ό덷�́C%1.1e �ōő�ƂȂ�C���̒l�� %e �ł�\n", max_dx, max_error);

    return 0;
}
