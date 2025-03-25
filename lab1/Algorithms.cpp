#include <iostream>
#include <vector>
#include <cstdlib>
#include <chrono>

using namespace std;
using namespace std::chrono;

void swap(int& a, int& b) {
    a ^= b;
    b ^= a;
    a ^= b;
}

void selectionSort(vector<int>& arr) {
    int n = arr.size();
    for (int i = 0; i < n / 2; i++) {
        int minIndex = i;
        int maxIndex = i;
        for (int j = i + 1; j < n - i; j++) {
            if (arr[j] < arr[minIndex]) {
                minIndex = j;
            }
            if (arr[j] > arr[maxIndex]) {
                maxIndex = j;
            }
        }
        if (minIndex != i) {
            swap(arr[i], arr[minIndex]);
        }
        // Adjust maxIndex if it was swapped with minIndex
        if (maxIndex == i) {
            maxIndex = minIndex;
        }
        if (maxIndex != n - i - 1) {
            swap(arr[n - i - 1], arr[maxIndex]);
        }
    }
}

void bubbleSort(vector<int>& arr) {
    int n = arr.size();
    for (int i = 0; i < n - 1; i++) {
        bool swapped = false;
        for (int j = 0; j < n - 1 - i; j++) {
            if (arr[j] > arr[j + 1]) {
                swap(arr[j], arr[j + 1]);
                swapped = true;
            }
        }
        if (!swapped) break;
    }
}

void insertionSort(vector<int>& arr) {
    int n = arr.size();
    for (int i = 1; i < n; i++) {
        int key = arr[i];
        int j = i - 1;
        while (j >= 0 && arr[j] > key) {
            arr[j + 1] = arr[j];
            j--;
        }
        arr[j + 1] = key;
    }
}




void merge(vector<int>& arr, int left, int mid, int right) {
    vector<int> temp(right - left + 1);
    int i = left, j = mid + 1, k = 0;
    while (i <= mid && j <= right) {
        if (arr[i] <= arr[j]) {
            temp[k++] = arr[i++];
        } else {
            temp[k++] = arr[j++];
        }
    }
    while (i <= mid) temp[k++] = arr[i++];
    while (j <= right) temp[k++] = arr[j++];
    for (i = left, k = 0; i <= right; i++, k++) {
        arr[i] = temp[k];
    }
}

void mergeSort(vector<int>& arr, int left, int right) {
    if (left < right) {
        int mid = left + (right - left) / 2;
        mergeSort(arr, left, mid);
        mergeSort(arr, mid + 1, right);
        merge(arr, left, mid, right);
    }
}




int split(vector<int>& arr, int low, int high) {
    int pivot = arr[high];
    int i = low - 1;
    for (int j = low; j < high; j++) {
        if (arr[j] < pivot) {
            i++;
            swap(arr[i], arr[j]);
        }
    }
    swap(arr[i + 1], arr[high]);
    return i + 1;
}


void quickSort(vector<int>& arr, int low, int high) {
    if (low < high) {
        int pivotIndex = split(arr, low, high);
        quickSort(arr, low, pivotIndex - 1);
        quickSort(arr, pivotIndex + 1, high);
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

    if (algorithm == "selection") {
        selectionSort(arr);
    } else if (algorithm == "bubble") {
        bubbleSort(arr);
    } else if (algorithm == "insertion") {
        insertionSort(arr);
    } else if (algorithm == "merge") {
        mergeSort(arr, 0, size - 1);
    } else if (algorithm == "quick") {
        quickSort(arr, 0, size - 1);
    } else {
        cerr << "Invalid algorithm!" << endl;
        return 1;
    }

    auto end = high_resolution_clock::now();
    auto duration = duration_cast<milliseconds>(end - start);

    cout << duration.count() << endl;
    return 0;
}