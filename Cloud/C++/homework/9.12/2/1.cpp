#include <iostream>
using namespace std;

bool IsMagic(int x) {
	if (x % 7 == 0) return true;
	while (x > 0) {
		if (x % 10 == 7) return true;
		x /= 10;
	}
	return false;
}

int main() {
	int n, sum = 0;
	cin >> n;
	for (int i = 1; i <= n; i++) {
		if (IsMagic(i)) {
			sum += i;
		}
	}
	cout << sum << endl;
	return 0;
}
