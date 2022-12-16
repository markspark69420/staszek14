#include<iostream>
#include<map>

using namespace std;

int litery[26]; 

int main(){
    string a;
    int max;
    int count=0;
    cin >> a >> max;
    int end = 0;
    int ei = 1000001,bi = -1;
    for(int i=0; i<a.length();i++){
        while(count<max && end<a.length()){
            if(litery[(int) a[end] - 97] == 0){
                count++;
            }
            litery[(int) a[end] - 97]++;
            end++;
        }
        if(count==max and (ei-bi)>(end-i)){
            ei = end;
            bi = i;
        }
        litery[(int) a[i] - 97]--;
        if(litery[(int) a[i] - 97]==0){
            count--;
        }
    }
    if(bi==-1){
        cout<<"BRAK";
    }
    else{
        cout<<bi+1<<' '<<ei;
    }
}
