#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <time.h>

#define MAX_SIZE 200000

typedef struct {
    int* nums;              // 数组存储元素
    int size;               // 当前元素个数
    int capacity;           // 数组容量
    int* valToIndex;        // 值到索引的映射（使用数组模拟哈希表）
    int mapSize;            // 映射表大小
} RandomizedSet;

RandomizedSet* randomizedSetCreate() {
    RandomizedSet* obj = (RandomizedSet*)malloc(sizeof(RandomizedSet));
    obj->capacity = 16;
    obj->size = 0;
    obj->nums = (int*)malloc(sizeof(int) * obj->capacity);
    obj->mapSize = 200001;  // 值范围：-2^31 到 2^31-1，需要偏移处理
    obj->valToIndex = (int*)malloc(sizeof(int) * obj->mapSize);
    // 初始化为 -1 表示不存在
    memset(obj->valToIndex, -1, sizeof(int) * obj->mapSize);
    srand(time(NULL));
    return obj;
}

bool randomizedSetInsert(RandomizedSet* obj, int val) {
    // 将 val 映射到非负索引（偏移 100000）
    int key = val + 100000;
    if (key < 0 || key >= obj->mapSize) return false;
    
    // 检查是否已存在
    if (obj->valToIndex[key] != -1) {
        return false;
    }
    
    // 扩容检查
    if (obj->size >= obj->capacity) {
        obj->capacity *= 2;
        obj->nums = (int*)realloc(obj->nums, sizeof(int) * obj->capacity);
    }
    
    // 添加到数组末尾
    obj->nums[obj->size] = val;
    obj->valToIndex[key] = obj->size;
    obj->size++;
    return true;
}

bool randomizedSetRemove(RandomizedSet* obj, int val) {
    int key = val + 100000;
    if (key < 0 || key >= obj->mapSize) return false;
    
    // 检查是否存在
    int idx = obj->valToIndex[key];
    if (idx == -1) {
        return false;
    }
    
    // 将最后一个元素移动到 idx 位置
    int lastVal = obj->nums[obj->size - 1];
    obj->nums[idx] = lastVal;
    
    // 更新最后一个元素的索引映射
    int lastKey = lastVal + 100000;
    obj->valToIndex[lastKey] = idx;
    
    // 删除 val 的映射
    obj->valToIndex[key] = -1;
    
    // 删除数组最后一个元素
    obj->size--;
    return true;
}

int randomizedSetGetRandom(RandomizedSet* obj) {
    int randomIndex = rand() % obj->size;
    return obj->nums[randomIndex];
}

void randomizedSetFree(RandomizedSet* obj) {
    if (obj) {
        free(obj->nums);
        free(obj->valToIndex);
        free(obj);
    }
}

