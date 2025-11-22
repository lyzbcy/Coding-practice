"""
LeetCode 45. 跳跃游戏 II - 错误代码演示
展示常见错误和正确解法的对比
"""

def jump_wrong1(nums):
    """
    错误示例 1：每次都跳最远（贪心策略错误）
    问题：局部最优不一定导致全局最优
    """
    n = len(nums)
    if n <= 1:
        return 0
    
    jumps = 0
    i = 0
    
    while i < n - 1:
        jumps += 1
        # 每次都跳最远
        max_jump = nums[i]
        i = i + max_jump
    
    return jumps


def jump_wrong2(nums):
    """
    错误示例 2：遍历到最后一个位置导致错误计数
    问题：最后一个位置是终点，不需要再跳
    """
    n = len(nums)
    jumps = 0
    end = 0
    maxReach = 0
    
    # 错误：遍历到 n，而不是 n - 1
    for i in range(n):  # ❌ 应该只遍历到 n - 1
        maxReach = max(maxReach, i + nums[i])
        if i == end:
            jumps += 1
            end = maxReach
    
    return jumps


def jump_wrong3(nums):
    """
    错误示例 3：使用动态规划，时间复杂度 O(n²)
    问题：虽然正确，但时间复杂度不是最优
    """
    n = len(nums)
    if n <= 1:
        return 0
    
    # dp[i] 表示到达位置 i 的最小跳跃次数
    dp = [float('inf')] * n
    dp[0] = 0
    
    for i in range(1, n):
        for j in range(i):
            if j + nums[j] >= i:
                dp[i] = min(dp[i], dp[j] + 1)
    
    return dp[n - 1]


def jump_correct(nums):
    """
    正确解法：边界跳跃法（贪心算法）
    时间复杂度：O(n)
    空间复杂度：O(1)
    """
    n = len(nums)
    jumps = 0
    end = 0          # 上一次跳跃能到达的最远位置（边界）
    maxReach = 0     # 当前能到达的最远位置
    
    # 注意：只需要遍历到 n - 1（最后一个位置不需要再跳）
    for i in range(n - 1):
        # 更新当前能到达的最远位置
        maxReach = max(maxReach, i + nums[i])
        
        # 如果到达边界，需要再跳一次
        if i == end:
            jumps += 1
            end = maxReach
    
    return jumps


def compare_solutions():
    """对比错误解法和正确解法"""
    test_cases = [
        ([2, 3, 1, 1, 4], 2),
        ([2, 3, 0, 1, 4], 2),
        ([1, 1, 1, 1], 3),
        ([1], 0),
        ([1, 2, 3, 4, 5], 3),
    ]
    
    print("=" * 60)
    print("LeetCode 45. 跳跃游戏 II - 错误代码演示")
    print("=" * 60)
    print()
    
    for nums, expected in test_cases:
        print(f"测试用例: nums = {nums}")
        print(f"预期结果: {expected}")
        print()
        
        # 错误示例 1
        try:
            result1 = jump_wrong1(nums)
            status1 = "✓" if result1 == expected else "✗"
            print(f"错误示例 1（每次都跳最远）: {result1} {status1}")
            if result1 != expected:
                print(f"  问题：局部最优不一定导致全局最优")
        except Exception as e:
            print(f"错误示例 1: 运行时错误 - {e}")
        print()
        
        # 错误示例 2
        try:
            result2 = jump_wrong2(nums)
            status2 = "✓" if result2 == expected else "✗"
            print(f"错误示例 2（遍历到最后一个位置）: {result2} {status2}")
            if result2 != expected:
                print(f"  问题：最后一个位置是终点，不需要再跳")
        except Exception as e:
            print(f"错误示例 2: 运行时错误 - {e}")
        print()
        
        # 错误示例 3（动态规划，虽然正确但时间复杂度不是最优）
        try:
            result3 = jump_wrong3(nums)
            status3 = "✓" if result3 == expected else "✗"
            print(f"错误示例 3（动态规划 O(n²)）: {result3} {status3}")
            if result3 == expected:
                print(f"  说明：虽然结果正确，但时间复杂度 O(n²) 不是最优")
            else:
                print(f"  问题：结果错误")
        except Exception as e:
            print(f"错误示例 3: 运行时错误 - {e}")
        print()
        
        # 正确解法
        result_correct = jump_correct(nums)
        status_correct = "✓" if result_correct == expected else "✗"
        print(f"正确解法（边界跳跃法 O(n)）: {result_correct} {status_correct}")
        print()
        print("-" * 60)
        print()


if __name__ == '__main__':
    compare_solutions()

