# Задание-1:
# Напишите функцию, возвращающую ряд Фибоначчи с n-элемента до m-элемента.
# Первыми элементами ряда считать цифры 1 1

def fibonacci(n, m):
    fib = []
    a, b = 0, 1
    for num in range(m):
        fib.append(b)
        a, b = b, a + b
    n -= 1
    res = [fib[i] for i in range(n, m)]
    del fib
    print(res)
    return res


fibonacci(1, 10)

# Задача-2:
# Напишите функцию, сортирующую принимаемый список по возрастанию.
# Для сортировки используйте любой алгоритм (например пузырьковый).
# Для решения данной задачи нельзя использовать встроенную функцию и метод sort()

def min_num(li):
    min = float('inf')
    for elem in li:
        if elem < min:
            min = elem
    return min

def sort_to_max(origin_list):
    list = [x for x in origin_list]
    sort_list = []
    while len(list):
        for elem in list:
            if elem == min_num(list):
                sort_list.append(elem)
                list.remove(elem)
    del list
    print(sort_list)
    return sort_list

sort_to_max([2, 10, -12, 2.5, 20, -11, 4, 4, 0])



# Задача-3:
# Напишите собственную реализацию стандартной функции filter.
# Разумеется, внутри нельзя использовать саму функцию filter.

def alt_filter(func, itr): # вроде правельно понял, что от меня хотя

    new_itr = [elem for elem in itr if func(elem)]
    if type(itr) is tuple:
        new_itr = tuple(new_itr)
    if type(itr) is set:
        new_itr = set(new_itr)
    if type(itr) is str:
        new_itr = ''.join(new_itr)
    print(new_itr)
    return new_itr

alt_filter(lambda x: x >= 0, {2, 10, -12, 2.5, 20, -11, 4, 4, 0})



# Задача-4:
# Даны четыре точки А1(х1, у1), А2(x2 ,у2), А3(x3 , у3), А4(х4, у4).
# Определить, будут ли они вершинами параллелограмма.
import math



def isparall(a, b, c, d):

    p1 = False
    p2 = False

    ab = math.sqrt((b[0] - a[0])**2 + (b[1] - a[1])**2)
    cb = math.sqrt((b[0] - c[0])**2 + (b[1] - c[1])**2)
    cd = math.sqrt((d[0] - c[0])**2 + (d[1] - c[1])**2)
    ad = math.sqrt((d[0] - a[0])**2 + (d[1] - a[1])**2)
    if ab == cd and cb == ad:
        print('Равенство сторон: верно')
        p1 = True
    else:
        print('Противоположные стороны НЕ равны')

    hO1 = ((a[0] + c[0])/2, (a[1] + c[1])/2)
    hO2 = ((b[0] + d[0])/2, (b[1] + d[1])/2)
    if hO1 == hO2:
        print('Равенство половин диагоналей: верно')
        p2 = True
    else:
        print('Половины диагоналей НЕ равны')

    if p1 and p2:
        print('Вершины A1%s, A2%s, A3%s, A4%s\nобразуют параллелограмм' %
              (a, b, c, d))
    else:
        print('Вершины не образуют параллелограмм')

A1=(-10, 10)
A2=(10, 10)
A3=(10, -10)
A4=(-10, -10)


isparall(A1, A2, A3, A4)