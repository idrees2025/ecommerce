from django.db import models
from django.contrib.auth.models import User

# Create your models here.
PRODUCT_CATEGORIES =(
    ('keyboard','keyboard'),
    ('huddie','huddie'),
    ('shoes','shoes'),
    ('graphic card','graphic card'),
    ('LED','LED'),
)

class Products(models.Model):
    p_title=models.CharField(max_length=222)
    p_category=models.CharField(choices=PRODUCT_CATEGORIES,max_length=12)
    p_dsc=models.TextField()
    p_price=models.IntegerField(max_length=222)
        
    def __str__(self):
        return self.p_category    

    def main_image(self):
        first_image=self.images.first()
        if first_image:
            return first_image.p_image.url
        return None
    
class productimage(models.Model):
    product=models.ForeignKey(Products,on_delete=models.CASCADE,related_name='images')
    p_image=models.ImageField(upload_to='photo/')

    def __str__(self):
        return f'{self.product.p_title} image'
    
class CartItem(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    color=models.CharField(max_length=222,null=True,blank=True)
    size=models.CharField(max_length=222,null=True,blank=True)
    quantity=models.IntegerField(default=1)

    def total(self):
        return self.product.p_price*self.quantity    
 