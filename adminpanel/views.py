from django.http.response import HttpResponse
from django.shortcuts import render,redirect

from django.views.generic import View,TemplateView , FormView
from django.views.generic.edit import UpdateView

from store.models import Category, Product ,ContactModel ,Customer ,Order

from adminpanel.models import EmployeeModel


from django.contrib.auth.models import User

from django.contrib.auth import authenticate,login

from adminpanel.forms import ProductAddForm , OrderAddForm ,EmployeeForm ,CreateUserForm ,LoginForm

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
# Create your views here.



class admin(View):
	template_name = 'admin.html'
	@method_decorator(login_required(login_url='login'))
	def get(self,request):
		orders = Order.objects.all().count()
		customers = Customer.objects.all().count()
		

		# total_customers = customers.count()
		# total_orders = orders.count()
		mydictionary={
			'total_orders': orders,
			'total_customers': customers,

			
		}
		return render(request,self.template_name,mydictionary)

# class products(TemplateView):
# 	template_name= 'products.html'

class products(View):
	template_name = 'products.html'
	model= Product
	@method_decorator(login_required(login_url='login'))
	def get(self,request):
		count1 = Product.objects.latest('submitted_at')
		count = Product.objects.all().count()
		mydictionary ={
			'count' : count,
			'count1' : count1
		}
		return render(request,self.template_name,mydictionary)


class ProductAdd(View):
	template_name = 'product_add.html'
	form_class= ProductAddForm
	@method_decorator(login_required(login_url='login'))
	def get(self,request):
		form = self.form_class()
		mydictionary ={
			'form' : form
		}
		return render(request,self.template_name,mydictionary)


	def post(self,request):
		form = self.form_class(request.POST,request.FILES)
		if form.is_valid():
			cat_obj = Category.objects.get(id=request.POST.get('category'))
			product_obj = Product.objects.create(
				category = cat_obj,
				name = request.POST.get('name'),
				price = request.POST.get('price'),
				description = request.POST.get('description'),
				image = request.FILES.get('image')
				)
			return redirect('/dash/products')
		else:
			form = self.form_class()
			return render(request,self.template_name,{'form':form})


class listproduct(View):
	template_name = 'list_product.html'
	@method_decorator(login_required(login_url='login'))
	def get(self,request):
		product = Product.objects.all()
		mydictionary={
			'cat': product
		}
		return render(request,self.template_name,mydictionary)


class deleteproduct(View):
	template_name = 'list_product.html'
	@method_decorator(login_required(login_url='login'))
	def get(self,request,pk):
		cat_obj = Product.objects.get(id=pk).delete()
		products = Product.objects.all()
		mydictionary={
			'cat': products
		}
		return render(request,self.template_name,mydictionary)


class productdetail(View):
	template_name = 'product_detail.html'
	@method_decorator(login_required(login_url='login'))
	def get(self,request,pk):
		obj = Product.objects.get(id=pk)
		mydictionary={
			'cat': obj
		}
		return render(request,self.template_name,mydictionary)
    
class listfeedback(View):
	template_name = 'list_feedback.html'
	@method_decorator(login_required(login_url='login'))
	def get(self,request):
		feed = ContactModel.objects.all()
		mydictionary={
			'cat': feed
		}
		return render(request,self.template_name,mydictionary)

class ProductUpdate(UpdateView):
	template_name= 'product_update.html'
	model= Product
	fields = ['name','price','category','description','image']
	success_url= '/dash/listproduct'

class OrderDetails(View):
	@method_decorator(login_required(login_url='login'))
	def get(self,request):
		orders = Order.objects.all()
		total_orders = orders.count()
		completed = orders.filter(status=True).count()
		pending = orders.filter(status=False).count()
		context = {
			'orders' : orders,
			'total_orders' : total_orders,
			'completed': completed,
			'pending' : pending
		}
		return render(request,'order_details.html',context)

class OrderUpdate(UpdateView):
	template_name= 'order_update.html'
	model= Order
	fields = ['product','quantity','address','phone','status']
	success_url= '/dash/order'
	
class deleteOrder(View):
	@method_decorator(login_required(login_url='login'))
	def get(self,request,pk):
		order = Order.objects.get(id=pk).delete()
		return redirect('order')


class CustomerView(View):
	@method_decorator(login_required(login_url='login'))
	def get(self,request):
		customers = Customer.objects.all()
		context={
			'customers': customers
		}
		return render(request,'customer.html',context)

class CustomerUpdate(UpdateView):
	template_name= 'customer_update.html'
	model= Customer
	fields = ['first_name','last_name','phone','email','profile_pic']
	success_url= '/dash/customer'

class deleteCustomer(View):
	@method_decorator(login_required(login_url='login'))
	def get(self,request,pk):
		customer = Customer.objects.get(id=pk).delete()
		return redirect('customer')
#employee

class EmployeeView(View):
	@method_decorator(login_required(login_url='login'))
	def get(self,request):
		employees = EmployeeModel.objects.all()
		context={
			'employees': employees
		}
		return render(request,'employee.html',context)

class EmployeeUpdate(UpdateView):
	template_name= 'employee_update.html'
	model= EmployeeModel
	fields = ['name','phone']
	success_url= '/dash/employee'

class deleteEmployee(View):
	@method_decorator(login_required(login_url='login'))
	def get(self,request,pk):
		employee = EmployeeModel.objects.get(id=pk).delete()
		return redirect('employee')


#employee end

###
class CustomerRegister(FormView):
	template_name='customer_register.html'
	form_class= CreateUserForm


	def get(self,request,*args,**kwargs):
		self.object=None
		form_class = self.get_form_class()
		user_form = self.get_form(form_class)
		cust_form = EmployeeForm()
		return self.render_to_response(self.get_context_data(form1=user_form, form2=cust_form))


	def post(self,request,*args,**kwargs):
		self.object=None
		form_class = self.get_form_class()
		user_form = self.get_form(form_class)
		cust_form = EmployeeForm(self.request.POST)
		if (user_form.is_valid() and cust_form.is_valid()):
			return self.form_valid(user_form, cust_form)
		else:
			return self.form_invalid(user_form, cust_form)

	def form_valid(self,user_form,cust_form):
		self.object = user_form.save() #User model save
		self.object.is_staff=True # edit user object
		self.object.save()
		cust_obj = cust_form.save(commit=False) #Customer Model save(contact,address,place,pincode,gender)
		cust_obj.user=self.object #saving OneToOnefield ,edit cust_obj
		cust_obj.save()
		return super(CustomerRegister, self).form_valid(user_form)

	def form_invalid(self,user_form,cust_form):
		return self.render_to_response(self.get_context_data(form1=user_form,form2=cust_form))

	def get_success_url(self, **kwargs):
		return ('/dash/employee')

class Login(View):
	template_name = 'login.html'
	form_class = LoginForm

	def get(self,request):
		form = self.form_class()
		mydictionary ={
			'forms' : form
		}
		return render(request,self.template_name,mydictionary)
	def post(self,request):
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request,username=username,password=password)#1st username is from model
		#if valid,user object will create ,otherwise create None

		if user is not None:
			login(request,user)
			#x = request.user x will hold the username of loggined one
			uname = request.user
			try:
				user_obj = User.objects.get(username=uname)
				cust = EmployeeModel.objects.get(user=user_obj)
			except:
				user_obj=None
				cust=None
			if request.user.is_superuser:
				return redirect('/dash')
			elif cust:
				return redirect('/dash')
			else:
				return redirect('login')
		else:
			return redirect('login') 

###

class StaffProfile(View):
	template_name = 'staff_profile.html'

	def get(self,request):
		logined_username = request.user
		user_obj = User.objects.get(username=logined_username)
		cust_obj = EmployeeModel.objects.get(user=user_obj)
		context = {
		'staff':cust_obj
		}
		return render(request,self.template_name,context)