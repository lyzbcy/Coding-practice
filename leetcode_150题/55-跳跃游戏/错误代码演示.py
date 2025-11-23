"""
LeetCode 55. 跳跃游戏 - 错误代码演示
演示学生提交的错误代码的执行过程，帮助理解问题所在
"""

def canJump_wrong(nums):
    """
    学生提交的错误代码（Python版本）
    问题：
    1. if((i+m)>=numsSize) return false; 应该返回 true
    2. 判断条件 nums[i+m]>=(nums[i]-m) 不够准确
    3. 算法思路不够标准
    """
    numsSize = len(nums)
    i = 0
    m = 1
    
    print(f"初始状态：i={i}, m={m}, numsSize={numsSize}")
    print(f"数组：{nums}")
    print("-" * 60)
    
    step_count = 0
    max_steps = 100  # 防止无限循环
    
    while i < numsSize and step_count < max_steps:
        step_count += 1
        print(f"\n【步骤 {step_count}】当前位置：i={i}, 尝试跳跃步数：m={m}")
        print(f"  检查条件：i+m={i+m} >= numsSize={numsSize}? {i+m >= numsSize}")
        
        # 问题1：这里应该返回 true，但错误地返回了 false
        if (i + m) >= numsSize:
            print(f"  ❌ 错误判断：i+m={i+m} >= numsSize={numsSize}，错误地返回 false")
            print(f"  💡 正确做法：此时应该返回 true（已到达或超过终点）")
            return False
        
        if i + m < numsSize:
            print(f"  检查：nums[{i+m}]={nums[i+m]} >= (nums[{i}]-{m})={nums[i]-m}? {nums[i+m] >= (nums[i]-m)}")
            
            # 问题2：判断条件不够准确
            if nums[i + m] >= (nums[i] - m):
                print(f"  ✅ 条件满足，跳跃到位置 {i+m}")
                i = i + m
                m = 1
                print(f"  更新后：i={i}, m={m}")
                if i >= numsSize - 1:
                    print(f"  ✓ 到达终点！应该返回 true")
                    return True
                continue
            else:
                print(f"  ❌ 条件不满足，尝试增加跳跃步数")
                m += 1
        
        print(f"  检查：m={m} > nums[{i}]={nums[i]}? {m > nums[i]}")
        if m > nums[i]:
            print(f"  ❌ 跳跃步数超过当前位置的最大跳跃能力，返回 false")
            return False
    
    if step_count >= max_steps:
        print(f"\n⚠️ 达到最大步数限制，可能存在无限循环")
    
    print(f"\n循环结束，返回 true")
    return True


def canJump_correct(nums):
    """
    正确的贪心算法实现
    """
    maxReach = 0  # 当前能到达的最远位置
    
    print(f"\n【正确算法】")
    print(f"数组：{nums}")
    print("-" * 60)
    
    for i in range(len(nums)):
        print(f"\n位置 i={i}, nums[{i}]={nums[i]}")
        print(f"  当前 maxReach={maxReach}")
        
        if i > maxReach:
            print(f"  ❌ i={i} > maxReach={maxReach}，无法到达，返回 false")
            return False
        
        newReach = i + nums[i]
        maxReach = max(maxReach, newReach)
        print(f"  从位置 {i} 最多能到 {newReach}，更新 maxReach={maxReach}")
        
        if maxReach >= len(nums) - 1:
            print(f"  ✓ maxReach={maxReach} >= {len(nums)-1}，可以到达终点，返回 true")
            return True
    
    return True


def compare_solutions():
    """
    对比错误代码和正确代码的执行结果
    """
    test_cases = [
        ([2, 3, 1, 1, 4], True, "示例1：应该能到达"),
        ([3, 2, 1, 0, 4], False, "示例2：无法到达"),
        ([0], True, "边界：只有一个元素"),
        ([1, 0], True, "边界：能到达"),
        ([0, 1], False, "边界：无法到达"),
    ]
    
    print("=" * 80)
    print("错误代码 vs 正确代码 对比测试")
    print("=" * 80)
    
    for nums, expected, description in test_cases:
        print(f"\n{'='*80}")
        print(f"测试用例：{nums}")
        print(f"预期结果：{expected}")
        print(f"说明：{description}")
        print(f"{'='*80}")
        
        # 测试错误代码
        print("\n【错误代码执行】")
        try:
            result_wrong = canJump_wrong(nums.copy())
            print(f"错误代码结果：{result_wrong}")
        except Exception as e:
            print(f"错误代码异常：{e}")
            result_wrong = None
        
        # 测试正确代码
        print("\n【正确代码执行】")
        result_correct = canJump_correct(nums.copy())
        print(f"正确代码结果：{result_correct}")
        
        # 对比
        print(f"\n【对比结果】")
        if result_wrong == expected:
            print(f"  ✓ 错误代码意外正确（可能是巧合）")
        else:
            print(f"  ❌ 错误代码结果：{result_wrong}，预期：{expected}")
        
        if result_correct == expected:
            print(f"  ✓ 正确代码结果正确")
        else:
            print(f"  ❌ 正确代码结果：{result_correct}，预期：{expected}")
        
        print("\n" + "="*80 + "\n")


def demonstrate_specific_case():
    """
    详细演示一个特定测试用例的错误执行过程
    """
    print("=" * 80)
    print("详细演示：nums = [2, 3, 1, 1, 4]")
    print("=" * 80)
    
    nums = [2, 3, 1, 1, 4]
    print(f"\n数组：{nums}")
    print(f"数组长度：{len(nums)}")
    print(f"最后一个位置索引：{len(nums) - 1}")
    print(f"预期结果：True（应该能到达）")
    
    print("\n" + "="*80)
    print("【错误代码执行过程】")
    print("="*80)
    result_wrong = canJump_wrong(nums.copy())
    
    print("\n" + "="*80)
    print("【正确代码执行过程】")
    print("="*80)
    result_correct = canJump_correct(nums.copy())
    
    print("\n" + "="*80)
    print("【总结】")
    print("="*80)
    print(f"错误代码结果：{result_wrong}")
    print(f"正确代码结果：{result_correct}")
    print(f"预期结果：True")
    print(f"\n错误代码的主要问题：")
    print(f"  1. if((i+m)>=numsSize) return false; 应该返回 true")
    print(f"  2. 判断条件 nums[i+m]>=(nums[i]-m) 不够准确")
    print(f"  3. 算法思路不够标准，应该使用贪心算法维护 maxReach")


if __name__ == "__main__":
    print("=" * 80)
    print("LeetCode 55. 跳跃游戏 - 错误代码演示")
    print("=" * 80)
    print("\n本演示将展示学生提交的错误代码的执行过程，")
    print("帮助理解代码中的逻辑错误。")
    print("\n按 Enter 键开始演示...")
    input()
    
    # 详细演示一个特定用例
    demonstrate_specific_case()
    
    print("\n\n" + "=" * 80)
    print("是否继续查看所有测试用例的对比？(y/n)")
    print("=" * 80)
    choice = input().strip().lower()
    
    if choice == 'y':
        compare_solutions()
    
    print("\n演示结束！")

