#include <iostream>
using namespace std;

int main() {
	int n;
	cin >> n;
	int cnt = 0;
	for (int num = 1; num <= n; num++) {
		int tmp = num;
		int d = tmp % 10;
		bool ok = true;
		while (tmp > 0) {
			if (tmp % 10 != d) {
				ok = false;
				break;
			}
			tmp /= 10;
		}
		if (ok) {
			cnt++;
		}
	}
	cout << cnt << endl;
	return 0;
}
