def fmap(value, istart, istop, ostart, ostop):
    return ostart + (ostop - ostart) * ((value - istart) / (istop - istart))

def hist_eq(nums):
    print(nums)
    height = len(nums)
    width = len(nums[0])
    low = min([min(row) for row in nums])
    high = max([max(row) for row in nums])
    for y in range(height):
        for x in range(width):
            val = nums[y][x]
            histogram_equalized = fmap(val, low, high, 0, 255)
            nums[y][x] = int(histogram_equalized)
    return nums

import numpy as np
nums = np.arange(40).reshape(-1, 10) - 15
nums = nums.tolist()
print(hist_eq(nums))
