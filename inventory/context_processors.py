from .models import Item
from django.db.models import F

#para acessar pelo navbar. VALOR QUE SERÁ ACESSADO POR todo o codigo

def estoque_minimo(request):
    try:
        count = Item.objects.filter(user=request.user,quantity__lt=10).count()
       # count_products = count.count()
    except:
        count = 0
    return {'estoque_minimo_count': count,
            'estoque_minimo':count}
