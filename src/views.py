from django.shortcuts import render

# Create your views here.
import razorpay
from django.views.decorators.csrf import csrf_exempt


from src.models import *

def home(request):
    if request.method == 'POST':
        amount = int(request.POST.get('amount')) * 100
        print(amount)
        client = razorpay.Client(auth=('rzp_test_RTTQ388YhSciSW','B38ANzasxi1sYj1YZPmvO6CG'))

        payment = client.order.create({'amount':amount,'currency':'INR','payment_capture':'1'})
        print(payment)
        coffee = Razor(amount = amount,payment_id = payment['id'])
        coffee.save()
        return render(request,'index1.html',{'payment':payment})
    return render(request,'index1.html')
@csrf_exempt
def success(request):
    if request.method == 'POST':
        a = request.POST
        print(a)
        order_id = ''
        for key , val in a.items():
            if key == 'razorpay_order_id':
                order_id = val
                break
        user = Razor.objects.filter(payment_id = order_id).first()
        user.paid = True
        user.save()
        
    return render(request,'success.html')