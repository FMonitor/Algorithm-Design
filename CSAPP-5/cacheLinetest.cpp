#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define ARRAY_SIZE (8 * 1024 * 1024)  
#define REPEAT 100                    // 重复次数，用于平滑时间波动
int array[ARRAY_SIZE];
double get_time_diff(struct timespec start, struct timespec end) {
    return (end.tv_sec - start.tv_sec) * 1e9 + (end.tv_nsec - start.tv_nsec); // ns
}
int main() {
    struct timespec start, end;
    int stride
    printf("Stride (Bytes)\tAvg Access Time (ns)\n");
    for (stride = 1; stride <= 1024; stride *= 2) {
        for (int i = 0; i < ARRAY_SIZE; ++i) array[i] = i;

        clock_gettime(CLOCK_MONOTONIC, &start);
        for (int r = 0; r < REPEAT; ++r) {
            for (int i = 0; i < ARRAY_SIZE; i += stride) {
                array[i]++;
            }
        }
        clock_gettime(CLOCK_MONOTONIC, &end);
        int num_accesses = (ARRAY_SIZE / stride) * REPEAT;
        double total_time_ns = get_time_diff(start, end);
        double avg_time = total_time_ns / num_accesses;
        printf("%14d\t%.2f\n", stride * sizeof(int), avg_time);
    }
    return 0;
}
