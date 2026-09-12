#include<iostream>

using namespace std;

int main(){
	int n;
	long long answer = 0, temp;
	cin>>n;
	for (int i=0;i<n;i++){
		cin>>temp;
		answer ^= temp;
	}
	cout<<answer<<' '<<(answer ^ answer);
	
	return 0;
}
