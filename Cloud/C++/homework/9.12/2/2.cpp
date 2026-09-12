#include <iostream>
using namespace std;

int main() {
	int n, k, sum = 0;
	cin >> n >> k;
	for (int i = 0; i < n; i++) {
		int x;
		cin >> x;
		if (x % 10 == k) {
			sum += x;
		}
	}
	cout << sum << endl;
	return 0;
}
