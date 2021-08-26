from store.models import Category, Product ,ContactModel , Customer ,Order
from django.shortcuts import redirect, render ,HttpResponseRedirect

from django.views.generic.edit import UpdateView

from django.http import HttpResponse

from django.contrib.auth.hashers import make_password,check_password

# print(make_password('1234'))
# print(check_password('1234','pbkdf2_sha256$260000$Hg0XRapDS7OzK5g03GG2hf$vidlD2DZO6oIPRxMH63deDPGpN3D+m1IKD1DxjVXKbc='))


from store.middlewares.auth import auth_middleware#the decorator is used when it is used inside the function.here is the class. so it needs a method decorator
from django.utils.decorators import method_decorator

from django.views import View
# Create your views here.


class Index(View):
    def get(self,request):
        #print(request.GET)
        cart = request.session.get('cart')
        if not cart:
            request.session['cart'] = {}
        products =None
        #request.session.get('cart').clear()
        category = Category.get_all_categories()
        categoryID = request.GET.get('category')
        #print(categoryID)
        if categoryID:
            products = Product.get_all_products_by_categoryid(categoryID)
        else:
            products = Product.get_all_products();
        

        email = request.session.get('email')
        customer = Customer.get_customer_by_email(email)
        print('customer is',customer)

        context = {

            "products":products,
            "category" : category,
            'customer' : customer
            
            
    
        }
        print('you are :' , request.session.get('email')) #from Login
        
        return render(request,'index.html',context)

    def post(self,request):#add to cart
        product = request.POST.get('product')
        print(product)
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product) #product ->product key
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity-1
                else:
                    cart[product] = quantity+1
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart
        print('cart',request.session['cart'])
        return redirect('home')



def contact(request):
    return render(request,'contact_us.html')

def contactsubmit(request):
    if request.method=='POST':
        obj=ContactModel()
        obj.name=request.POST['name']
        obj.email=request.POST['email']
        obj.message=request.POST['message']
        obj.save()
        return redirect('home')
    
    return render(request,'contact_us.html')

class Signup(View):
    def get(self,request):
        return render(request,'signup.html')
    def post(self,request):
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')
        value = {
            'firstname' : firstname,
            'lastname' : lastname,
            'phone' : phone,
            'email' : email,
            'password' :password
        }
        #valiadation
        error_message = None

        customer = Customer(first_name=firstname,
            last_name=lastname,
            phone = phone,
            email = email,
            password = password
            )
        error_message = self.validateCustomer(customer)
        
        #saving
        if not error_message:
            print(firstname,lastname,phone,email,password)
            customer.password = make_password(customer.password)
            customer.register()
            # return redirect('/') or
            return redirect('home')
        else:
            data = {
                'values' : value,
                'error' : error_message,
            }
            return render(request,'signup.html',data)

    def validateCustomer(self,customer):
        error_message = None;
        if not customer.first_name:
            error_message = 'First Name Required !!'
        # elif len(firstname) < 4 :
        #     error_message = 'First Name must be 4 or more character long'
        elif not customer.last_name:
            error_message = 'Last Name Required !!'
        elif not customer.phone  :
            error_message = 'Phone Number Required'
        elif len(customer.phone) <10 :
            error_message = 'Phone must be 10 character long'
        elif not customer.password  :
            error_message = 'Password Number Required'
        # elif len(password) <6 :
        #     error_message = 'Passwors must be 6 or more character long'
        elif customer.isExists():
            error_message = 'Email address already registered..'

        return error_message


class Login(View):
    return_url = None
    def get(self,request):
        Login.return_url = request.GET.get('return_url')
        return render(request,'login1.html')
    def post(self,request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        #print(email,password)
        customer = Customer.get_customer_by_email(email)
        print(customer)
        error_message = None
        if customer:#here is the code to proceed only after getting the customer(check get_customer_by_email 1st )
            print(customer)
            flag = check_password(password,customer.password)#customer.password-encoded password
            if flag:
                # request.session['customer_id'] = customer.id
#session start,request.session ->we will get a dictionary
                request.session['customer'] = customer.id #saving customer object in session
                request.session['email'] = customer.email
                # return redirect('home')
                if Login.return_url: #if we have return url
                    return HttpResponseRedirect(Login.return_url)
                else:
                    Login.return_url = None
                    return redirect('home')
            else:
                error_message = 'Email or Password invalid !!!'

        else:
            error_message = 'Email or Password invalid !!!'
        print(email, password)
        return render(request,'login1.html',{'error':error_message})


def logout(request):
    request.session.clear()
    return redirect('login1')

class Cart(View):
    
    @method_decorator(auth_middleware)
    def get(self,request):
        print(request.session.get('cart'))
        print(request.session.get('cart').keys())
        #dict to list
        print(list(request.session.get('cart').keys()))
        ids = list(request.session.get('cart').keys())
        products = Product.get_products_by_id(ids)
        print(products)

        email = request.session.get('email')
        customer = Customer.get_customer_by_email(email)


        return render(request,'cart.html',{'products' : products,'customer':customer})

class CheckOut(View):
    def post(self,request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('customer')#customer-it is customer id
        cart = request.session.get('cart')
        products = Product.get_products_by_id(list(cart.keys()))
        print(address , phone , customer , cart , products)

        for product in products:
            print(cart.get(str(product.id)))
            order = Order(customer =Customer(id= customer),
            product = product,
            price = product.price,
            address = address,
            phone = phone,
            quantity = cart.get(str(product.id))) #quantity will get from the cart object

            # print(order)
            order.save()

        request.session['cart'] = {}

        # return redirect('cart')
        return redirect('/razor')

class OrderView(View):
    @method_decorator(auth_middleware)
    def get(self,request):
        customer = request.session.get('customer')
        orders = Order.get_orders_by_customer(customer)
        print(orders)

        email = request.session.get('email')
        customer = Customer.get_customer_by_email(email)

        return render(request,'orders.html',{'orders':orders,'customer':customer})


class ProfileUpdate(UpdateView):
	template_name= 'profile_update.html'
	model= Customer
	fields = ['first_name','last_name','phone','email','profile_pic']
	success_url= '/'