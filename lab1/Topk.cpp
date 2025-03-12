#include <bits/stdc++.h>
using namespace std;
using namespace std::chrono;

vector<int> heapTopk(vector<int>& arr, int k) {
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
    vector<int> result;
    while (!pq.empty()) {
        result.push_back(pq.top());
        pq.pop();
    }
    return result;
}

vector<int> simpleTopk(vector<int>& arr, int k) {
    vector<int> result;
    for (int i = 0; i < 10; i++) {
        int max = 0;
        int maxindex = 0;
        for (int j = 0; j < arr.size(); j++) {
            if (arr[j] > max) {
                max = arr[j];
                maxindex = j;
            }
        }
        result.push_back(max);
        arr[maxindex] = 0;
    }
    return result;
}


vector<int> quickTopk(vector<int>& nums, int k) {
    if (nums.size() <= k) {
        return nums;
    }

    // 随机选择基准元素
    srand(time(0));
    int pivot = nums[rand() % nums.size()];

    // 分区
    vector<int> greater, equal, less;
    for (int num : nums) {
        if (num > pivot) {
            greater.push_back(num);
        } else if (num == pivot) {
            equal.push_back(num);
        } else {
            less.push_back(num);
        }
    }

    // 递归处理
    if (greater.size() >= k) {
        return quickTopk(greater, k);
    } else if (greater.size() + equal.size() >= k) {
        vector<int> result = greater;
        result.insert(result.end(), equal.begin(), equal.end());
        return vector<int>(result.begin(), result.begin() + k);
    } else {
        vector<int> result = greater;
        result.insert(result.end(), equal.begin(), equal.end());
        vector<int> lessResult = quickTopk(less, k - greater.size() - equal.size());
        result.insert(result.end(), lessResult.begin(), lessResult.end());
        return result;
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
    vector<int> result;
    if (algorithm == "simpleTopk") {
        result = simpleTopk(arr, 10);
    } else if (algorithm == "heapTopk") {
        result = heapTopk(arr, 10); 
    } else if (algorithm == "quickTopk") {
        result = quickTopk(arr, 10);
    } else {
        cerr << "Invalid algorithm: " << algorithm << endl;
        return 1;
    }

    auto end = high_resolution_clock::now();
    auto duration = duration_cast<milliseconds>(end - start);

    cout << duration.count() << endl;
    return 0;
}