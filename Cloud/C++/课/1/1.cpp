#include <iostream>
#include <algorithm>
#include <iomanip>

using namespace std;

int main() {
	double V, G, M, N;
	cin >> V >> G >> M >> N;
	double vol_cost = 0.5 * V;
	double wei_cost;
	if (G < 300) {
		wei_cost = M;
	} else {
		wei_cost = N;
	}
	double ans = min(vol_cost, wei_cost);
	cout << fixed << setprecision(1) << ans << endl;
	return 0;
}
