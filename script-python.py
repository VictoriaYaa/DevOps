def solution(A, B):
    A.sort()
    B.sort()
    i = 0
    for a in A:
        if i < len(B) and B[i] < a:
            i += 1
        if a == B[i]:
            return a
    return -1


print (solution([1,24,6,3],[15,2,8,9]))