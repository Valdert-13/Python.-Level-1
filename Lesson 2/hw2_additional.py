# 1) Написать программу, которая генерирует список со случайными значениями. (модуль random в помощь)
# 2) Найдите сумму чисел списка, которые стоят на четных местах.
# 3) Сделать универсальное решение для того, чтобы можно было отсортировать словарь по значениям
# 4) Сформировать пять списков разной длины и найти в них элементы, которые есть в каждом списке

import random

def a_function(a): # теоритически нужна проверка на длинну списка, но в связи что списков всого 5 шанс что списки будут одинаковыми стремится к 0
    for j in range (random.randint(0, 100)):
        a.append(random.randint(0, 100))

def listsum(numList):
    theSum = 0
    for i in numList[0::2]:
        theSum += i
    return theSum



list1=[]
list2=[]
list3=[]
list4=[]
list5=[]
a_function(list1)


print (list1)
print ("")

print (len(list1))
print ("")


print (listsum(list1))
print ("")

def dict_val(x):
    return x[1]


x = {1: 2, 3: 4, 4: 3, 2: 1, 0: 0}
s_x = sorted(x.items(), key=dict_val)
print (s_x )
print ("")


a_function(list2)
a_function(list3)
a_function(list4)
a_function(list5)


print (list1)
print (list2)
print (list3)
print (list4)
print (list5)
print ("")

result = list(set(list1) & set(list2) &  set(list3) &  set(list4) &  set(list5))

print (result)