def fib(n, nums={0: 0, 1: 1}):
	if n in nums:
		return nums[n]
	else:
		nums[n] = fib(n-1, nums) + fib(n-2, nums)
		return nums[n]

def fib_either_side_of(n, nums={0: 0, 1: 1}):
	a, b = nums[len(nums)-2], nums[len(nums)-1]
	if a <= n <= b:
		return a, b
	else:
		nums[len(nums)] = a + b
		return fib_either_side_of(n, nums)


print(fib_either_side_of(100*100*100*100*100*123*150023845702029384570293845702394857246387523457967126439263459345345343452646345734567890263475293572365482734658273465823765283459237562394579876543456))