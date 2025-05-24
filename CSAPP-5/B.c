#include <sys/time.h> 
#include <unistd.h> 
#include <stdlib.h>
#include <stdio.h> 
#define BLOCK_SIZE 32
int main(int argc, char* argv[])
{
    float *a,*b,*c, temp;
    long int i, j, k, size, m;
    struct timeval time1,time2; 
    
    if(argc<2) { 
        printf("\n\tUsage:%s <Row of square matrix>\n",argv[0]); 
        exit(-1); 
    } //if

    size = atoi(argv[1]);
    m = size*size;
    a = (float*)malloc(sizeof(float)*m); 
    b = (float*)malloc(sizeof(float)*m); 
    c = (float*)malloc(sizeof(float)*m); 

    for(i=0;i<size;i++) { 
        for(j=0;j<size;j++) { 
            a[i*size+j] = (float)(rand()%1000/100.0); 
            b[i*size+j] = (float)(rand()%1000/100.0); 
        } 
    }
    
    gettimeofday(&time1,NULL);
    // 分块矩阵乘法
for (i = 0; i < size; i += BLOCK_SIZE) {
    for (j = 0; j < size; j += BLOCK_SIZE) {
        for (k = 0; k < size; k += BLOCK_SIZE) {
            // 处理块内元素
            for (int i1 = i; i1 < i + BLOCK_SIZE && i1 < size; i1++) {
                for (int j1 = j; j1 < j + BLOCK_SIZE && j1 < size; j1++) {
                    float sum = (k == 0) ? 0 : c[i1*size+j1];
                    for (int k1 = k; k1 < k + BLOCK_SIZE && k1 < size; k1++) {
                        sum += a[i1*size+k1] * b[k1*size+j1];
                    }
                    c[i1*size+j1] = sum;
                }
            }
        }
    }
}
    gettimeofday(&time2,NULL);     
    
time2.tv_sec-=time1.tv_sec; 
    time2.tv_usec-=time1.tv_usec; 
    if (time2.tv_usec<0L) { 
        time2.tv_usec+=1000000L; 
        time2.tv_sec-=1; 
    } 
   
    printf("Executiontime=%ld.%06ld seconds\n",time2.tv_sec,time2.tv_usec); 
        return(0); 
}//main
