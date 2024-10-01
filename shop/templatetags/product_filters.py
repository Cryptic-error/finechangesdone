# from django import template
# from django.template.exceptions import TemplateSyntaxError
# from shop.models import Product

# register = template.Library()

# @register.filter
# def get_product(product_id,hello):
#     try:
#         return Product.objects.get(id=product_id)
#     except Product.DoesNotExist:
#         raise TemplateSyntaxError("Product with ID {} does not exist".format(product_id))


from django import template
from django.template.exceptions import TemplateSyntaxError
from shop.models import Product

register = template.Library()

@register.filter
def get_product(product_id):
    try:
        return Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        raise TemplateSyntaxError("Product with ID {} does not exist".format(product_id))
