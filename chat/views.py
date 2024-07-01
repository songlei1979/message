from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response


# Create your views here.
def sumNumbers(start_num, end_num):
    if start_num > end_num:
        start_num, end_num = end_num, start_num
    sum = 0
    for i in range(start_num, end_num + 1):
        sum += i
    return sum


@api_view(['Post'])
def sumNumbersView(request):
    if request.method == 'POST':
        start_num = int(request.POST.get('start_num', 0))
        end_num = int(request.POST.get('end_num', 0))
        result = sumNumbers(start_num, end_num)
        return Response({'result': result})

