// Exhaustive deterministic 1-bit/star cut-recognition search on K_4.
// Standard C++17. Independent of the prior MILP and of any numerical solver.
#include <array>
#include <chrono>
#include <cstdint>
#include <iostream>
#include <vector>
using Mask=std::array<uint64_t,7>;
static std::array<std::array<Mask,128>,4> miss;
static std::array<Mask,5> forced;
static uint64_t visited[5]={};
static int answer[4];
bool nonempty_intersection(const Mask& a,const Mask& b){
 for(int k=0;k<7;k++) if(a[k]&b[k])return true;
 return false;
}
bool search(int v, const Mask& uncovered){
 visited[v]++;
 if(nonempty_intersection(uncovered,forced[v])) return false;
 if(v==4)return true;
 for(int f=0;f<128;f++){
  Mask next{};for(int k=0;k<7;k++)next[k]=uncovered[k]&miss[v][f][k];
  answer[v]=f<<1;if(search(v+1,next))return true;
 }
 return false;
}
int main(){
 const int n=4;std::vector<std::pair<int,int>> edges;
 for(int u=0;u<n;u++)for(int v=u+1;v<n;v++)edges.push_back({u,v});
 int local[64][4]={}; bool cut[64]={};
 for(int g=0;g<64;g++){
  for(int v=0;v<n;v++){
   int k=0;for(int j=0;j<6;j++)if(edges[j].first==v||edges[j].second==v){
    local[g][v]|=((g>>j)&1)<<k;k++;
   }
  }
  int mat[4][4]={};for(int j=0;j<6;j++){
   auto[u,v]=edges[j];mat[u][v]=mat[v][u]=(g>>j)&1;
  }
  cut[g]=true;for(int u=1;u<n;u++)for(int v=u+1;v<n;v++)
   if(mat[u][v]!=(mat[0][u]^mat[0][v]))cut[g]=false;
 }
 int c=0;Mask initial{};
 for(int good=0;good<64;good++)if(cut[good])
 for(int bad=0;bad<64;bad++)if(!cut[bad]){
  int w=c/64,b=c%64;initial[w]|=1ULL<<b;
  int highest=-1;for(int v=0;v<4;v++)if(local[good][v]!=local[bad][v])highest=v;
  for(int depth=highest+1;depth<=4;depth++)forced[depth][w]|=1ULL<<b;
  for(int v=0;v<4;v++)for(int f=0;f<128;f++){
   int table=f<<1;
   if(((table>>local[good][v])&1)==((table>>local[bad][v])&1))
    miss[v][f][w]|=1ULL<<b;
  }
  c++;
 }
 auto start=std::chrono::steady_clock::now();bool exists=search(0,initial);
 auto seconds=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
 std::cout<<"{\"m\":4,\"bits_per_vertex\":1,\"output_complement_normalized\":true,\"normalized_protocols\":268435456,\"constraints\":"<<c<<",\"exists\":"<<(exists?"true":"false")<<",\"search_nodes_by_depth\":[";
 for(int k=0;k<5;k++){if(k)std::cout<<",";std::cout<<visited[k];}
 std::cout<<"],\"elapsed_seconds\":"<<seconds;
 if(exists){std::cout<<",\"truth_tables\":[";for(int k=0;k<4;k++){if(k)std::cout<<",";std::cout<<answer[k];}std::cout<<"]";}
 std::cout<<"}\n";
}
