
#include <bits/stdc++.h>
#include <iostream>

using namespace std;

const int sizen = 1000;

int costMatrixA[sizen][sizen];
int costMatrixB[sizen][sizen];
int productMat[sizen][sizen];
int minmat[sizen][sizen];
int maxmat[sizen][sizen];
int maxmat_1[sizen][sizen];                //transpose of maxmat
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
    printf("Initialization complete");
    //creating productMat as explained in the beginning
    FindMinCostA(0,0,sizen);
    FindMaxCostB(0,0,sizen);

    for (i = 0; i < sizen; i++)
    {
        for (j = 0; j < sizen; j++)
        {
            maxmat_1[i][j] = maxmat[j][i];
        }
    }
    for (i = 0; i < sizen; i++)
    {
        for (j = 0; j < sizen; j++)
        {
            for (k = 0; k < sizen; k++)
            {
                productMat[i][j] += minmat[i][k]*maxmat_1[j][k];
            }
        }
    }
    
   /*
    printf("%lld\n",FindMinCostA(0,0,sizen));
    printf("%lld\n",FindMaxCostB(0,0,sizen));
    *
    for(int i =0;i<100;i++){
        for (int j =0;j< 100; j++){
            printf("%d ",maxmat[i][j]);
        }
        printf("\n");
    }
    */

    return 0;
}