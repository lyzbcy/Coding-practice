/**
 * 二维最接近点对问题
 * 
 * 使用分治算法求解
 * 时间复杂度：O(n log² n)
 * 空间复杂度：O(n)
 */

#include <iostream>
#include <vector>
#include <algorithm>
#include <cmath>
#include <iomanip>
#include <climits>

using namespace std;

// 定义点结构体
struct Point {
    int x, y;
    
    Point(int x = 0, int y = 0) : x(x), y(y) {}
};

// 计算两点间距离
double distance(const Point &p1, const Point &p2) {
    int dx = p1.x - p2.x;
    int dy = p1.y - p2.y;
    return sqrt((double)dx * dx + (double)dy * dy);
}

// 暴力枚举计算n≤3时的最短距离
double bruteForce(const vector<Point> &points, int left, int right) {
    double min_dist = 1e20;
    for (int i = left; i < right; i++) {
        for (int j = i + 1; j < right; j++) {
            double dist = distance(points[i], points[j]);
            if (dist < min_dist) {
                min_dist = dist;
            }
        }
    }
    return min_dist;
}

// 计算条带区域内的最短距离
double stripClosest(vector<Point> &strip, double d) {
    double min_dist = d;
    
    // 按y坐标排序条带中的点
    sort(strip.begin(), strip.end(), 
         [](const Point &a, const Point &b) {
             if (a.y != b.y) return a.y < b.y;
             return a.x < b.x;
         });
    
    // 对于每个点，只需检查其后的最多6个点
    for (int i = 0; i < strip.size(); i++) {
        for (int j = i + 1; j < strip.size() && 
             (strip[j].y - strip[i].y) < min_dist; j++) {
            double dist = distance(strip[i], strip[j]);
            if (dist < min_dist) {
                min_dist = dist;
            }
        }
    }
    
    return min_dist;
}

// 分治算法主函数
double closestUtil(vector<Point> &points, int left, int right) {
    // 递归终止条件：点数≤3时使用暴力法
    if (right - left <= 3) {
        return bruteForce(points, left, right);
    }
    
    // 找到中点
    int mid = left + (right - left) / 2;
    Point midPoint = points[mid];
    
    // 递归求解左右两部分
    double dl = closestUtil(points, left, mid);
    double dr = closestUtil(points, mid, right);
    
    // 取左右两部分的最小距离
    double d = min(dl, dr);
    
    // 构建条带：距离中线d范围内的点
    vector<Point> strip;
    for (int i = left; i < right; i++) {
        if (abs(points[i].x - midPoint.x) < d) {
            strip.push_back(points[i]);
        }
    }
    
    // 计算条带内的最短距离
    double stripMin = stripClosest(strip, d);
    
    // 返回全局最小距离
    return min(d, stripMin);
}

// 主函数：计算最近点对距离
double closest(vector<Point> &points) {
    int n = points.size();
    
    // 按x坐标排序
    sort(points.begin(), points.end(), 
         [](const Point &a, const Point &b) {
             if (a.x != b.x) return a.x < b.x;
             return a.y < b.y;
         });
    
    // 调用分治算法
    return closestUtil(points, 0, n);
}

int main() {
    int n;
    cin >> n;
    
    vector<Point> points(n);
    for (int i = 0; i < n; i++) {
        cin >> points[i].x >> points[i].y;
    }
    
    double result = closest(points);
    cout << fixed << setprecision(2) << result << endl;
    
    return 0;
}

