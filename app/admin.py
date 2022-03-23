
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import(
    Contact,
    Customer,
    Product,
    Cart,
    OrdrerPlaced,
    Slider
    
    
)

#Register your models here.
@admin.register(Contact)
class ContactModelAdmin(admin.ModelAdmin):
    list_display=['name','email','phone','desc','date']

@admin.register(Slider)
class SliderModelAdmin(admin.ModelAdmin):
    list_display =['image']

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','name','locality','city','zipcode','state']
    
@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    
    list_display =['id','title','selling_price','discounted_price','description','brand','category','product_image'] 



@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display =['id','user','product','quantity']
    
    
    

@admin.register(OrdrerPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['id','user', 'customer','customer_info','product','product_info','quantity', 'ordered_date', 'status',]
    
    
    def customer_info(self,obj):
        link = reverse("admin:app_customer_change",args=[obj.customer.pk])
        return format_html('<a href="{}">{}</a>' ,link,obj.customer.name)
    
    def product_info(self,obj):
        link = reverse("admin:app_product_change",args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>' ,link,obj.product.title)

    