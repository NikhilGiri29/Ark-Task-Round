
#include <bits/stdc++.h>
#include <iostream>
#include<pthread.h>
using namespace std;

const int sizen = 1000;
int maxThread = 20;

int costMatrixA[sizen][sizen];
int costMatrixB[sizen][sizen];
int productMat[sizen][sizen];
int minmat[sizen][sizen];
int maxmat[sizen][sizen];
int maxmat_1[sizen][sizen];                //transpose of maxmat

int thread_num =1;
int task_per_thread = sizen/maxThread;
//Simple recursion  which returns the minimum cost of going from i,j to n,n
int FindMinCostA(int i, int j, int n)
{
    //going out of bounds
    if (i >= n)
        return 1000000;
    //going out of bounds
    if (j >= n)
        return 1000000;
    //reaching the last cell
    if (i == n - 1 && j == n - 1){
    int x = costMatrixA[i][j];
    minmat[i][j] = x;
    return x;
    }
    //going down or right
   int a,b;
    if(minmat[i+1][j] ==0){
    a = FindMinCostA(i + 1, j, n);
    }else{
    a = minmat[i+1][j];
    }
    if(minmat[i][j+1] ==0){
    b = FindMinCostA(i, j + 1, n);
    }else{
    b = minmat[i][j+1] ;
    }
    int x = costMatrixA[i][j] + min(a,b);
    minmat[i][j] = x;
    return x;
}


//Simple recursion which returns the maximum cost of going from i,j to n,n
int FindMaxCostB(int i, int j, int n)
{
    //going out of bounds
    if (i >= n)
        return 0;
    //going out of bounds
    if (j >= n)
        return 0;
    //reaching the last cell
    if (i == n - 1 && j == n - 1){
        int y= costMatrixB[i][j] ;
        maxmat[i][j] = y;
        return y;
    }
        
    //going down or right
    int a,b;
    if(maxmat[i+1][j] ==0){
    a = FindMaxCostB(i + 1, j, n);
    }else{
    a = maxmat[i+1][j];
    }
    if(maxmat[i][j+1] ==0){
    b = FindMaxCostB(i, j + 1, n);
    }else{
    b = maxmat[i][j+1] ;
    }
    int y= costMatrixB[i][j] + max(a,b);
    maxmat[i][j] = y;
    return y;
}

void* funct(void* arg){
    int start  = (task_per_thread-1)*thread_num; 
    
   for (int i = start; i < (start+task_per_thread); i++) {
            for (int j = 0; j < sizen; j++) {
                for (int k = 0; k < sizen; k++)
                {
                    productMat[i][j] += minmat[i][k] * maxmat_1[j][k];
                }
        }
   }
   thread_num += 1;

   return arg;
                
}


int main()
{
    int i, j, k;
    srand(time(0));
    // initialisation
    for (i = 0; i < sizen; i++)
    {
        for (j = 0; j < sizen; j++)
        {
            costMatrixA[i][j] = 1 + rand() % 10;
            costMatrixB[i][j] = 1 + rand() % 10;
            productMat[i][j] = 0;

        }
    }
    //printf("Initialization complete");
    //creating productMat as explained in the beginning
    FindMinCostA(0,0,sizen);
    FindMaxCostB(0,0,sizen);

    for (i = 0; i < sizen; i++)
    {
        for (j = 0; j < sizen; j++)
        {
            maxmat_1[j][i] = maxmat[i][j];
        }
    }
   
    pthread_t threads[maxThread];
  
    // Creating four threads, each evaluating its own part
    for (int i = 0; i < maxThread; i++) {
        int* p;
        pthread_create(&threads[i], NULL, funct, (void*)(p));
    }
  
    // joining and waiting for all threads to complete
    for (int i = 0; i < maxThread; i++) 
        pthread_join(threads[i], NULL);    

    //filter of size 4 x n
    int filterArray[4][sizen];

    for (i = 0; i < 4; i++)
    {
        for (j = 0; j < sizen; j++)
            filterArray[i][j] = rand() % 2;
    }

    // matrix of dimension (sizen/c) x 1 where c = 4
   int finalMat[sizen / 4];
    // applying the filter
    for (i = 0; i < sizen - 4; i += 4)
    {
        int sum = 0;
        // dot product of 4xn portion of productMat
        for (j = 0; j < sizen; j++)
        {
            for (int filterRow = 0; filterRow < 4; filterRow++)
            {
                sum += productMat[i + filterRow][j] * filterArray[filterRow][j];
            }
        }
        finalMat[i / 4] = sum;
        
    }
        
    return 0;
} 


//console --> g++ -pthread ArkOptimisation.cpp