def quicksort(array):
    if len(array) <= 1:
        return array
    lower=[];greater = []
    pivot = array.pop()
    for ele in array:
        if ele < pivot:lower.append(ele)
        else:greater.append(ele)
    return quicksort(lower) + [pivot] + quicksort(greater)

if __name__ == '__main__':
    a = [1,3,2,7,5,9,0,4]
    print quicksort(a)