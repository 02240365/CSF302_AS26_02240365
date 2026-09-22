# CSF302 : Algorithm Design & Analysis
## Lab Report 3


## Q1: Matrix Multiplication — Strassen's vs Traditional

Compares Traditional matrix multiplication (O(n³)) with Strassen's divide-and-conquer method (O(n^2.81)) for matrix sizes 2 to 128, verifying both give the same result and counting the steps each one takes.

**Output:**

![Q1 terminal output](/screenshots/q1_output.png)

**Graph:**

![Q1 time complexity graph](/screenshots/q1_graph.png)

**Reflection:**
Strassen needs fewer multiplications than the Traditional method, but it does a lot of extra additions to make that work. For the sizes tested here, those extra additions actually made Strassen slower in real time, even though its step count grew more slowly. This showed me that a "better" algorithm on paper isn't always faster in practice for small inputs - the constant overhead matters too.

---

## Q2: Karatsuba's Algorithm for Large Integer Multiplication

Compares Traditional grade-school multiplication (O(n²)) with Karatsuba's divide-and-conquer method (O(n^1.585)) for numbers with 8 to 1024 digits, verifying both give the same result and counting the steps each one takes.

**Output:**

![Q2 terminal output](/screenshots/q2_output.png)

**Graph:**

![Q2 time complexity graph](/screenshots/q2_graph.png)

**Reflection:**
Karatsuba was slower than the Traditional method for small numbers, but once the numbers got large (around 500+ digits), it started doing fewer steps overall. This matches the theory: Karatsuba trades multiplications for additions, and that trade only pays off once the numbers are big enough. It explains why algorithms like this matter for things like cryptography, where numbers can be hundreds of digits long.

---

## Q3: Binary Search vs Ternary Search (Menu-Driven Program)

A menu-driven program that generates a sorted array and searches it using Binary Search (O(log₂ n)) and Ternary Search (O(log₃ n)), counting the comparisons each one makes in the best case, worst case, and across increasing array sizes.

**Output:**

![Q3 menu, array, and best/worst case](/screenshots/q3_output1.png)

![Q3 comparison table across increasing n](/screenshots/q3_output2.png)

![Q3 menu, array, and best/worst case](/screenshots/q3_output3.png)

![Q3 comparison table across increasing n](/screenshots/q3_output4.png)

![Q3 menu, array, and best/worst case](/screenshots/q3_output5.png)

![Q3 comparison table across increasing n](/screenshots/q3_output6.png)

![Q3 menu, array, and best/worst case](/screenshots/q3_output7.png)

![Q3 comparison table across increasing n](/screenshots/q3_output8.png)

**Graph:**

![Q3 time complexity graph](/screenshots/q3_graph.png)

**Reflection:**
I expected Ternary Search to be faster since it splits the array into three parts instead of two, but it actually made more total comparisons than Binary Search. That's because each round of Ternary Search checks two positions instead of one, so the extra comparisons per round outweigh the fewer rounds. This was a good reminder that fewer "steps" in a recurrence doesn't always mean fewer actual operations.
