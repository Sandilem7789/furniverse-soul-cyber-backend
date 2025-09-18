from django.db import models

from django.contrib.auth.models import User         # For user authentication


# Category Model
class Category(models.Model):
    name = models.CharField(max_length=100)

# Product Model
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='products/', default='products/default.jpg')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_featured = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.name} – R{self.price}"

# Cart Model
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    class Meta:
        unique_together = ('user', 'product')                                       # Ensure one cart item per user-product pair