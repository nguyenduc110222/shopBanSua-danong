from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from .models import *
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.core.paginator import Paginator
from .forms import ContactShipping



# Create your views here.
def contact(request):
    return render(request, 'app/contact.html')

def profile(request):
    if request.user.is_authenticated:
        customer = request.user
        # lấy nếu người dùng đã có đơn hàng hoặc tạo đơn hàng của người dùng 
        order, create = Order.objects.get_or_create(customer=customer)
        # lấy tất cả đơn order của customer trong orderitem
        items = order.orderitem_set.all()
        categories = Category.objects.filter(is_sub=False)

    else:
        # nếu chưa đăng nhập thì đưa ra rỗng
        items = []
        order = None
    id = request.GET.get('id')
    if id and id.isdigit():
        users = User.objects.filter(id=id)
    else:
        users = []
    context= {'items': items, 'categories': categories, 'order': order, 'users': users}
    return render(request, 'app/profile.html', context)

def detail(request):
    if request.user.is_authenticated:
        customer = request.user
        # lấy nếu người dùng đã có đơn hàng hoặc tạo đơn hàng của người dùng 
        order, create = Order.objects.get_or_create(customer=customer)
        # lấy tất cả đơn order của customer trong orderitem
        items = order.orderitem_set.all()
        categories = Category.objects.filter(is_sub=False)

    else:
        # nếu chưa đăng nhập thì đưa ra rỗng
        items = []
        order = None
    id = request.GET.get('id','')
    products = Product.objects.filter(id=id)
    context={'products':products,'items': items,'order': order, 'categories': categories}

    return render(request, 'app/detail.html', context)

def category(request):
    customer = request.user
     # lấy nếu người dùng đã có đơn hàng hoặc tạo đơn hàng của người dùng 
    order, create = Order.objects.get_or_create(customer=customer)
    # lấy tất cả đơn order của customer trong orderitem
    items = order.orderitem_set.all()
    # lọc các danh mục có trong category không lấy danh mục con
    categories = Category.objects.filter(is_sub=False)
    # lấy ra danh mục khi user click vào bảng danh mục 
    active_category = request.GET.get('category','')
    # nếu click vào danh mục thì lọc các đường dẫn trong category 
    if active_category:
        products = Product.objects.filter(category__slug=active_category)
    context = {'products': products, 'active_category': active_category,'categories': categories,'items':items,'order':order,'customer':customer}
    return render(request, 'app/category.html', context)
def search(request):
    if request.user.is_authenticated:
        customer = request.user
        # lấy nếu người dùng đã có đơn hàng hoặc tạo đơn hàng của người dùng 
        order, create = Order.objects.get_or_create(customer=customer)
        # lấy tất cả đơn order của customer trong orderitem
        items = order.orderitem_set.all()
    else:
        # nếu chưa đăng nhập thì đưa ra rỗng
        items = []
        order = None
    searched = ""
    keys = []
    if request.method == 'POST':
        searched = request.POST.get("searched", "")
        keys = Product.objects.filter(name__icontains=searched)  # Sử dụng icontains để tìm kiếm không phân biệt chữ hoa chữ thường

    return render(request, 'app/search.html', {'searched': searched, 'keys': keys,'order': order, 'items': items})
def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    context = {'form':form}
    return render(request, 'app/register.html',context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse('Invalid login!')
    context = {}
    return render(request, 'app/login.html',context)
def logoutPage(request):
    logout(request)
    return redirect('login')
def home(request):
    # kiểm tra người dùng đã đăng nhập hay chưa
    if request.user.is_authenticated:
        customer = request.user
        # lấy nếu người dùng đã có đơn hàng hoặc tạo đơn hàng của người dùng 
        order, create = Order.objects.get_or_create(customer=customer)
        # lấy tất cả đơn order của customer trong orderitem
        items = order.orderitem_set.all()
        categories = Category.objects.filter(is_sub=False)
        
    else:
        # nếu chưa đăng nhập thì đưa ra rỗng
        items = []
        order = None
    products = Product.objects.all()
    paginator = Paginator(products,8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    sliders = Slider.objects.all()
    context={'page_obj':page_obj,'products': products, 'items': items, 'order': order, 'categories': categories, 'sliders': sliders}
    return render(request, 'app/home.html', context)

def cart(request):
    # kiểm tra người dùng đã đăng nhập hay chưa
    if request.user.is_authenticated:
        customer = request.user
        # lấy nếu người dùng đã có đơn hàng hoặc tạo đơn hàng của người dùng 
        order, create = Order.objects.get_or_create(customer=customer)
        # lấy tất cả đơn order của customer trong orderitem
        items = order.orderitem_set.all()
        categories = Category.objects.filter(is_sub=False)

    else:
        # nếu chưa đăng nhập thì đưa ra rỗng
        items = []
        order = None
    context={'items': items,'order': order, 'categories': categories}
    return render(request, 'app/cart.html',context)

def checkout(request):
    # kiểm tra người dùng đã đăng nhập hay chưa
    product_ship = None
    if request.user.is_authenticated:
        customer = request.user
        # lấy nếu người dùng đã có đơn hàng hoặc tạo đơn hàng của người dùng 
        order, create = Order.objects.get_or_create(customer=customer, complete=False)
        # lấy tất cả đơn order của customer trong orderitem
        items = order.orderitem_set.all()
        categories = Category.objects.filter(is_sub=False)
        if items.exists():
            product_ship = items.all()
    else:
        # nếu chưa đăng nhập thì đưa ra rỗng
        items = []
        order = None
        
    if request.method == 'POST':
        form = ContactShipping(request.POST)
        if form.is_valid():
            ShippingAddress = form.save(commit=False)
            ShippingAddress.customer = customer
            ShippingAddress.order = order
            if product_ship:
                for product in product_ship:
                    ShippingAddress.product_ship = product
                    ShippingAddress.quantity = product.quantity
            form.save()
            return redirect('checkout')
    else:
        form = ContactShipping()

    context={'order':order,'customer': customer,'items': items,'categories': categories,'form': form}

    return render(request, 'app/checkout.html', context)

def updateItem(request):
    # load dữ liệu đã bóc tách từ json trong file cart.js
    data = json.loads(request.body)
    # lấy json productId từ file cart
    productId = data['productId']
    # lấy json action từ file cart,js
    action = data['action']
    # lấy sản phẩm có id đã đc lấy từ trên
    product = Product.objects.get(id=productId)
    customer = request.user
    order,create = Order.objects.get_or_create(customer=customer)
    orderItem,create = OrderItem.objects.get_or_create(order=order,product = product)
    if action == 'add':
        orderItem.quantity += 1
    elif action =='remove':
        orderItem.quantity -= 1
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete() 
    
    return JsonResponse('added',safe=False)