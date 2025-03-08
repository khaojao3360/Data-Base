from django.db import models
import datetime

class seller(models.Model):
    seller_id = models.CharField(max_length=255, primary_key=True)
    store_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class seller_address(models.Model):
    seller_id = models.OneToOneField(
        seller, on_delete=models.CASCADE, db_column='seller_id'
    )
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=255)
    additional = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)


class product_category(models.Model):
    cat_id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    desc = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    cat_image_url = models.URLField(max_length=2083, null=True, blank=True)


class product(models.Model):
    prod_id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    desc = models.TextField()
    cat_id = models.ForeignKey(
        product_category, on_delete=models.CASCADE, db_column='cat_id'
    )
    seller_id = models.ForeignKey(
        seller, on_delete=models.CASCADE, db_column='seller_id'
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sales = models.IntegerField()
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    prod_image_url = models.URLField(max_length=2083, null=True, blank=True)


class users(models.Model):
    user_id = models.CharField(max_length=255, primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class user_address(models.Model):
    address_id = models.CharField(max_length=255, primary_key=True)
    user_id = models.ForeignKey(
        users, on_delete=models.CASCADE, db_column='user_id'
    )
    title = models.CharField(max_length=255)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=255)
    additional = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=255)


class user_payment(models.Model):
    payment_id = models.CharField(max_length=255, primary_key=True)
    user_id = models.ForeignKey(
        users, on_delete=models.CASCADE, db_column='user_id'
    )
    payment_method = models.CharField(max_length=255)
    provider = models.CharField(max_length=255)
    account_no = models.CharField(max_length=255, unique=True)
    expiry = models.CharField(max_length=5)
    cvv = models.CharField(max_length=3)


class status(models.Model):
    status_id = models.CharField(max_length=255, primary_key=True)
    status_desc = models.CharField(max_length=255)


class shipping_company(models.Model):
    shipping_company_ID = models.CharField(max_length=255, primary_key=True)
    shipping_name = models.CharField(max_length=255)


class order_details(models.Model):
    order_id = models.BigIntegerField(max_length=255)
    user_id = models.ForeignKey(
        users, on_delete=models.CASCADE, db_column='user_id'
    )
    address_id = models.ForeignKey(
        user_address, on_delete=models.CASCADE, db_column='address_id'
    )
    payment_id = models.ForeignKey(
        user_payment, on_delete=models.CASCADE, db_column='payment_id'
    )
    prod_id = models.ForeignKey(
        product, on_delete=models.CASCADE, db_column='prod_id'
    )
    quantity = models.IntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status_id = models.ForeignKey(
        status, on_delete=models.CASCADE, db_column='status_id'
    )
    shipping_company_ID = models.ForeignKey(
        shipping_company, on_delete=models.CASCADE, db_column='shipping_company_ID'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('order_id', 'prod_id')


class reviews(models.Model):
    prod_id = models.ForeignKey(
        product, on_delete=models.CASCADE, db_column='prod_id'
    )
    rating = models.SmallIntegerField()
    comment = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class cart(models.Model):
    user_id = models.ForeignKey(
        users, on_delete=models.CASCADE, db_column='user_id'
    )
    prod_id = models.ForeignKey(
        product, on_delete=models.CASCADE, db_column='prod_id'
    )

    def delete(self):
        super().delete()


class wishlist(models.Model):
    user_id = models.ForeignKey(
        users, on_delete=models.CASCADE, db_column='user_id'
    )
    prod_id = models.ForeignKey(
        product, on_delete=models.CASCADE, db_column='prod_id'
    )
    def delete(self):
        super().delete()