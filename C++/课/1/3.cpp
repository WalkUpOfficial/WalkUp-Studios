#include <iostream>
#include <algorithm>
#include <iomanip>

using namespace std;

int main() {
	int x, y, n, p;
	cin >> x >> y >> n >> p;
	double opt1;
	if (p >= x) {
		opt1 = p - y;
	} else {
		opt1 = p;
	}
	double opt2 = p * n / 10.0;
	double ans = min(opt1, opt2);
	cout << fixed << setprecision(2) << ans << endl;
	return 0;
}
