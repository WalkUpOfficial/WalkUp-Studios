#include <iostream>

using namespace std;

int main() {
	int T;
	cin >> T;
	while (T--) {
		int P;
		cin >> P;
		if (P <= 10) {
			cout << "R\n";
		} else if (P <= 20) {
			cout << "L\n";
		} else {
			cout << P << "\n";
		}
	}
	return 0;
}
