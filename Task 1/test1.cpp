
#include <bits/stdc++.h>
#include <iostream>

using namespace std;

const int sizen = 268;

long long costMatrixA[sizen][sizen];
long long costMatrixB[sizen][sizen];
long long productMat[sizen][sizen];
long long minmat[sizen][sizen];
long long maxmat[sizen][sizen];

//Simple recursion  which returns the minimum cost of going from i,j to n,n

long long FindMinCostA(int i, int j, int n)
{
    //going out of bounds
    if (i >= n)
        return 1000000;
    //going out of bounds
    if (j >= n)
        return 1000000;
    //reaching the last cell
    if (i == n - 1 && j == n - 1)
        return costMatrixA[i][j];
    //going down or right
    long long int a,b;
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
    long long int x = costMatrixA[i][j] + min(a,b);
    minmat[i][j] = x;
    return x;
}


//Simple recursion which returns the maximum cost of going from i,j to n,n
long long FindMaxCostB(int i, int j, int n)
{
    //going out of bounds
    if (i >= n)
        return 0;
    //going out of bounds
    if (j >= n)
        return 0;
    //reaching the last cell
    if (i == n - 1 && j == n - 1)
        return costMatrixB[i][j];
    //going down or right
    long long int a,b;
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
    long long int y= costMatrixB[i][j] + max(a,b);
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
            minmat[i][j] = 0;
            maxmat[i][j] = 0;
        }
    }
    //creating productMat as explained in the beginning
    
    for (i = 0; i < sizen; i++)
    {
        for (j = 0; j < sizen; j++)
        {
            for (k = 0; k < sizen; k++)
            if(i ==0 && j==0 & k==0){
                productMat[i][j] += FindMinCostA(i, k, sizen) * FindMaxCostB(k, j, sizen);
            }else{
                productMat[i][j] += minmat[i][k]*maxmat[k][j];
            }
        }
    }
    
   /*
    printf("%lld\n",FindMinCostA(0,0,sizen));
    printf("%lld\n",FindMaxCostB(0,0,sizen));
    for(int i =0;i<sizen;i++){
        for (int j =0;j< sizen; j++){
            printf("%lld ",minmat[i][j]);
        }
        printf("\n");
    }
    */

    return 0;
}