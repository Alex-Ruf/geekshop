from django.db import models

class ProductCategory(models.Model):
    name = models.CharField(max_length=64, unique=True,verbose_name='имя')
    description =models.TextField(verbose_name='описание', blank=True)
    is_active = models.BooleanField(db_index=True,verbose_name="активность", default=True)

    def __str__(self):
        return self.name



class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    name =models.CharField(max_length=128, unique=True,verbose_name='имя')
    image = models.ImageField(upload_to='products_images',blank=True)
    short_desc = models.CharField(max_length=64, verbose_name='описание', blank=True)
    description = models.TextField(verbose_name='описание', blank=True)
    price = models.DecimalField(verbose_name='цена', max_digits=8,decimal_places=2,default=0)
    quantity =models.PositiveSmallIntegerField(verbose_name='количество',default=0)
    is_active = models.BooleanField(db_index=True,verbose_name="активность", default=True)

    def __str__(self):
        return f'{self.name}({self.category.name})'

    @staticmethod
    def get_items():
        return Product.objects.filter()

