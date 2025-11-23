#include <vector>
#include <unordered_map>
#include <cstdlib>
#include <ctime>

using namespace std;

class RandomizedSet {
private:
    vector<int> nums;                    // 存储所有元素
    unordered_map<int, int> valToIndex;  // 值 -> 数组索引的映射

public:
    RandomizedSet() {
        // 构造函数，初始化随机数种子
        srand(time(nullptr));
    }
    
    bool insert(int val) {
        // 如果已存在，返回 false
        if (valToIndex.find(val) != valToIndex.end()) {
            return false;
        }
        
        // 添加到数组末尾
        nums.push_back(val);
        // 记录索引
        valToIndex[val] = nums.size() - 1;
        return true;
    }
    
    bool remove(int val) {
        // 如果不存在，返回 false
        if (valToIndex.find(val) == valToIndex.end()) {
            return false;
        }
        
        // 获取要删除元素的索引
        int idx = valToIndex[val];
        // 获取最后一个元素
        int lastVal = nums.back();
        
        // 将最后一个元素移动到 idx 位置
        nums[idx] = lastVal;
        // 更新最后一个元素的索引映射
        valToIndex[lastVal] = idx;
        
        // 删除数组最后一个元素
        nums.pop_back();
        // 删除哈希表中的映射
        valToIndex.erase(val);
        
        return true;
    }
    
    int getRandom() {
        // 生成随机索引
        int randomIndex = rand() % nums.size();
        return nums[randomIndex];
    }
};

/**
 * Your RandomizedSet object will be instantiated and called as such:
 * RandomizedSet* obj = new RandomizedSet();
 * bool param_1 = obj->insert(val);
 * bool param_2 = obj->remove(val);
 * int param_3 = obj->getRandom();
 */

