#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define MAX_ARRAY_SIZE (64 * 1024 * 1024) // 最大测试到 64MB
#define STRIDE 64                         // 固定步长 = 64 字节
#define REPEAT 10               
double get_time_diff(struct timespec start, struct timespec end) {
    return (end.tv_sec - start.tv_sec) * 1e9 + (end.tv_nsec - start.tv_nsec); // ns
}

int main() {
    int STEP_SIZE = 64 * 1024; // 步长 = 4KB
    struct timespec start, end;
    printf("Array Size (KB)\tAvg Access Time (ns)\n");
    for (int size = 4 * 1024; size <= MAX_ARRAY_SIZE; size += STEP_SIZE) {
        if(size > 1024*1024) {
            STEP_SIZE = 1024 * 1024; // 步长 = 1MB
        }
        int num_ints = size / sizeof(int);
        int stride_ints = STRIDE / sizeof(int);
        int *array = (int *)malloc(size);
        if (!array) {
            perror("malloc");
            exit(1);
        }
        for (int i = 0; i < num_ints; ++i) {        // 初始化数组
            array[i] = i;
        }
        clock_gettime(CLOCK_MONOTONIC, &start);     // 测试访问延迟
        for (int r = 0; r < REPEAT; ++r) {
            for (int i = 0; i < num_ints; i += stride_ints) {
                array[i]++;
            }
        }
        clock_gettime(CLOCK_MONOTONIC, &end);
        int num_accesses = (num_ints / stride_ints) * REPEAT;
        double total_time = get_time_diff(start, end);
        double avg_time = total_time / num_accesses;
        printf("%16d\t%.2f\n", size / 1024, avg_time);
        free(array);
    }
    return 0;
}
