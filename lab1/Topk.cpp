#include <bits/stdc++.h>
using namespace std;

void optimizedTopk(vector<int>& arr, int k) {
    priority_queue<int, vector<int>, greater<int>> pq;
    for (int i = 0; i < k; i++) {
        pq.push(arr[i]);
    }
    for (int i = k; i < arr.size(); i++) {
        if (arr[i] > pq.top()) {
            pq.pop();
            pq.push(arr[i]);
        }
    }
    while (priority_queue.size() != 0) {
        cout << pq.top() << " ";
        pq.pop();
    }
}

void simpleTopk(vector<int>& arr, int k) {
    for(int i = 0; i < 10; i++) {
        int max = 0;
        int maxindex = 0;
        for (int j = 0; j < arr.size(); j++) {
            if (arr[j] > max) {
                max = arr[j];
                maxindex = j;
            }
        }
        cout << max << " ";
        arr[maxindex] = 0;
    }
}

int main(int argc, char* argv[]) {

    string algorithm = argv[1];
    int size = atoi(argv[2]);

    // 生成随机数组
    vector<int> arr(size);
    for (int i = 0; i < size; i++) {
        arr[i] = rand();
    }

    // 计时
    auto start = high_resolution_clock::now();

    if (algorithm == "simple") {
        simpleTopk(arr, 10);
    } else if (algorithm == "optimized") {
        optimizedTopk(arr, 10);
    } else {
        cerr << "Invalid algorithm: " << algorithm << endl;
        return 1;
    }

    auto end = high_resolution_clock::now();
    auto duration = duration_cast<milliseconds>(end - start);

    cout << duration.count() << endl;
    return 0;
}