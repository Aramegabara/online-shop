from django.db import models


def recalc_cart(cart):
    cart_data = cart.product.aggregate(models.Sum('sum_price'), models.Count('id'))
    if cart_data.get('sum_price__sum'):
        cart.sum_price = cart_data.get('sum_price__sum')
    else:
        cart.sum_price = 0
    cart.total_products = cart_data['id__count']
    cart.save()