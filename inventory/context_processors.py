from .models import Item
from django.db.models import F

#para acessar pelo navbar. VALOR QUE SERÁ ACESSADO POR todo o codigo

def estoque_minimo(request):
    try:
        count = Item.objects.filter(
        user=request.user
        ).filter(
        quantity__lt=F('minimum_stock')  # 👈 compara com o campo do próprio item
        ).count()

    except:
        count = 0
    return {'estoque_minimo_count': count,
            'estoque_minimo':count}
