#include<stack>
#include<iostream>
#include<vector>

using namespace std;

int main(){
    int a;
    stack<int> sztosy[200000];
    int stos_indx = 0;
    cin >> a;
    char curr;
    int liczba;

    for(int i=0; i<a; i++){
        cin >> curr;
        stos_indx++;
        if(curr=='+'){
            cin >> liczba;
            sztosy[stos_indx] = sztosy[stos_indx-1];
            sztosy[stos_indx].push(liczba);
            if(~sztosy[stos_indx].empty()){
                cout<<sztosy[stos_indx].top();
            }
            else{
                cout<<-1;
            }
        }
        else if(curr=='-'){
            sztosy[]
        }    
    }
}