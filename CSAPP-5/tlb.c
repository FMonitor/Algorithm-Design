#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>

#define PAGE_SIZE 4096
#define MAX_PAGES 8192 // 最大页数（32MB）
#define REPEAT 1000

char *array;

double get_time_diff(struct timespec start, struct timespec end) {
    return (end.tv_sec - start.tv_sec) * 1e9 + (end.tv_nsec - start.tv_nsec);
}

int main() {
    array = malloc(MAX_PAGES * PAGE_SIZE);
    if (!array) {
        perror("malloc failed");
        return 1;
    }

    struct timespec start, end;

    printf("Pages\tAvg Time per Access (ns)\n");
    for (int num_pages = 1; num_pages <= MAX_PAGES; num_pages *= 2) {
        clock_gettime(CLOCK_MONOTONIC, &start);

        for (int r = 0; r < REPEAT; r++) {
            for (int i = 0; i < num_pages * PAGE_SIZE; i += PAGE_SIZE) {
                array[i]++;
            }
        }

        clock_gettime(CLOCK_MONOTONIC, &end);
        double time_ns = get_time_diff(start, end);
        double avg_access_time = time_ns / (num_pages * REPEAT);
        printf("%5d\t%.2f\n", num_pages, avg_access_time);
    }

    free(array);
    return 0;
}
