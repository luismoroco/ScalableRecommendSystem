/**
 * DS using in program
*/

#include <iostream>
#include <vector>
#include <functional>
#include <cmath>
#include <utility>
#include <limits>
#include <map>
#include <queue>
#include <set>

using std::priority_queue;
using std::numeric_limits;
using std::vector;
using std::function;
using std::pair;
using std::map;
using std::set;
using std::string;

const float INF = numeric_limits<float>::max();

template <typename T>
struct ObjectEngine {
  private:
    set<pair<int, T>> bEng;
  
  public:
    T search(int src) {
      auto it = bEng.lower_bound({src, T()});
      if (it != bEng.end()) 
        return it->second;
      return T();
    }

    void add(int id, T w) {
      bEng.insert({id, w});
    }
};

