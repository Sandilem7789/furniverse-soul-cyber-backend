#import_products is a management command (not a routing command) to import products from a CSV file into the database.
import csv
from django.core.management.base import BaseCommand
from api.models import Product, Category

class Command(BaseCommand):
    help = 'Import products from a CSV file'
    
    def handle(self, *args, **kwargs):
        with open('data/products.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                category_instance, _ = Category.objects.get_or_create(name=row['category'])
                Product.objects.update_or_create(
                    name=row['name'],
                    description=row['description'],
                    price=row['price'],
                    sale_price=row['sale_price'] if row['sale_price'] else None,
                    image_url=row['image_url'],
                    category=category_instance,
                    is_featured=row['is_featured'].lower() in ('true', '1', 'yes')
                )
        self.stdout.write(self.style.SUCCESS('Products imported successfully'))