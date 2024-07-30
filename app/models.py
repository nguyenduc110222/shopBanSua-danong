from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


# Create your models here.

class Slider(models.Model):
    name = models.CharField(max_length=200, null=True)
    body = models.TextField()
    image = models.ImageField(upload_to='', null=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    category = models.ForeignKey('self',on_delete=models.CASCADE,related_name='sub_categories',null=True,blank=True)
    # kt xem co phai danh muc con hay khong
    is_sub = models.BooleanField(default=False)
    name = models.CharField(max_length=200, null=True)
    slug = models.SlugField(max_length=200,unique=True)
    def __str__(self):
        return self.name

# thay đổi các trường có sẵn trong django cho register
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name','password1','password2']



class Product(models.Model):
    category = models.ManyToManyField(Category,related_name='product')
    name = models.CharField(max_length=100, null=True)
    price = models.IntegerField()
    description = models.TextField(null=True)
    image = models.ImageField(upload_to='', null=True)

    def __str__(self):
        return self.name
    
    @property
    # dinh nghia thuoc tinh khi url cua images ton tai thi tra ve url cua image neu khong thi tra ve default
    def ImageURL(self):
        try:
            url = self.image.url
        except:
            url = ""
        return url

class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False)
    date_order = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False,null=True,blank=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.customer)
    
    @property
    def get_cart_items(self):
        #lấy tất cả trong orderitem
        orderitems = self.orderitem_set.all()
        # lấy số lượng item trong orderitem sau đó tính tổng
        toytal = sum([item.quantity for item in orderitems])
        return toytal
    
    def get_cart_total(self):
        #lấy tất cả trong orderitem
        orderitems = self.orderitem_set.all()
        # lấy giá của product với mỗi item trong orderitem
        total = sum([item.get_total for item in orderitems])
        return total
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=False)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=False)
    quantity = models.IntegerField(default=0, null=True,blank=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.product)
    
    @property
    def get_total(self):
        # tính giá của product với mỗi số lượng product
        total = self.product.price * self.quantity
        return total
class ShippingAddress(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=False)
    product_ship = models.ForeignKey(OrderItem, on_delete=models.SET_NULL, null=True, blank=False)
    quantity = models.IntegerField(null=True, blank=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=10, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.address
