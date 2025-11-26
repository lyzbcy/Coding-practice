#include <stddef.h>

/**
 * 一次遍历的贪心法：
 * total 记录总体盈余判断是否存在解；
 * tank 记录当前起点能否坚持到下一个站点；
 * 当 tank < 0 时，说明当前起点失败，直接从下一站重试。
 */
int canCompleteCircuit(int* gas, int gasSize, int* cost, int costSize) {
    if (gas == NULL || cost == NULL || gasSize <= 0 || gasSize != costSize) {
        return -1;
    }

    int total = 0;  // 全局净油量
    int tank = 0;   // 当前起点的油箱余量
    int start = 0;  // 候选起点

    for (int i = 0; i < gasSize; i++) {
        int gain = gas[i] - cost[i];
        total += gain;
        tank += gain;

        if (tank < 0) {
            start = i + 1;  // 当前起点无法到达 i+1，改用下一站
            tank = 0;       // 重置油箱，重新累计
        }
    }

    if (total < 0) {
        return -1;
    }

    return start % gasSize;
}


