from django.shortcuts import render, redirect       #render give a html page as response, redirect make the user goes to other URL
from .forms import ItemForm, CategoryForm, SubCategoryForm, LoginForm, Item, StockMovementForm, ItemEditForm
from django.shortcuts import redirect
from .models import Category, SubCategory, StockMovement
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.db.models import F
from inventory.context_processors import estoque_minimo
from reportlab.lib.pagesizes import A4 #generate the PDF
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from django.utils.timezone import localtime
from django.db import DatabaseError
from django.contrib import messages
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet
from django.db.models import F, Q
from django.db.models import Sum, DecimalField, ExpressionWrapper
from .forms import RegisterForm
from django.http import HttpResponseForbidden
from .decorators import admin_mode_required
from .models import User
from django.contrib.auth import update_session_auth_hash

# Create your views here.

@login_required
def change_mode(request):
    user = request.user  # o usuário logado
    print("DEBUG: Usuário logado:", user.email, "Role atual:", user.role)

    if request.method == "POST":
        new_role = request.POST.get("role")
        password = request.POST.get("password")
        print("DEBUG: Tentando alterar para:", new_role)
        print("DEBUG: Senha recebida:", password)

        # Verifica a senha do próprio usuário
        user_auth = authenticate(request, username=user.email, password=password)
        print("DEBUG: Resultado do authenticate:", user_auth)

        if user_auth is None:
            messages.error(request, "Senha incorreta. Não foi possível alterar o modo.")
            print("DEBUG: Senha incorreta")
            return redirect("homepage")

        # Aplica a mudança
        user.role = new_role
        user.save()
        print("DEBUG: Role após salvar:", user.role)

        update_session_auth_hash(request, user)
        messages.success(request, f"Modo alterado para {user.get_role_display()}.")
        return redirect("homepage")




@login_required
def homepage(request):  #after the urls.py direct to here, the function decide what to make. If shows or save what the user maked
    #filter products by user
        itens = Item.objects.filter(user=request.user)
        
        nome = request.GET.get("nome")
        preco_min = request.GET.get("preco_min")
        preco_max = request.GET.get("preco_max")
        estoque_min = request.GET.get("estoque_min")
        categoria = request.GET.get("categoria")
        subcategoria = request.GET.get("subcategoria")
        disponivel = request.GET.get("disponivel")

        if nome:
             itens = itens.filter(name__icontains=nome)
        if preco_min:
            itens = itens.filter(price__gte=preco_min)
        if preco_max:
            itens = itens.filter(price__lte=preco_max)
        if estoque_min:
            itens = itens.filter(quantity__gte=estoque_min)
        if categoria:
            itens = itens.filter(category_id=categoria)
        if subcategoria:
             itens = itens.filter(subcategory_id=subcategoria)
        if disponivel == "sim":
            itens = itens.filter(quantity__gt=0)
        elif disponivel == "nao":
            itens = itens.filter(quantity=0)

        if not itens.exists():
             messages.warning(request, "Nenhum Produto encontrado com os filtros selecionados")

        categorias = Category.objects.filter(id__in=Item.objects.filter(user=request.user).values("category")).distinct()

        subcategorias = SubCategory.objects.filter(id__in=Item.objects.filter(user=request.user).values("subcategory")).distinct()

        produtos_com_estoque_baixo = Item.objects.filter(
            user=request.user).filter(quantity__lt=F('minimum_stock'))
        
        if produtos_com_estoque_baixo.exists():
             messages.warning(request, f"⚠️ {produtos_com_estoque_baixo.count()} produto(s) estão com estoque baixo")
        
                   

        return render(request, 'inventory/homepage.html', {
            'itens':itens,
            'categorias': categorias,
            'subcategorias': subcategorias,
            "nome": nome,
            })


@login_required
def category_list(request):

    sort = request.GET.get('sort', 'name_asc')

    categories = (
        Category.objects.filter(user=request.user)  # pega só categorias do usuário
        .prefetch_related("subcategories")
        .annotate(
            total_value=Sum(
                F("item__price") * F("item__quantity"),
                output_field=DecimalField(max_digits=12, decimal_places=2)
            )
        )
    )

    if sort == 'name_asc':
         categories = categories.order_by('category')   #A-Z
    elif sort == 'name_desc':
         categories = categories.order_by('-category')  #Z-A
    elif sort == 'value_asc':
         categories = categories.order_by('total_value')
    elif sort == 'value_desc':
         categories = categories.order_by('-total_value')
        
    return render(request, "inventory/category_list.html", {"categories": categories, "sort":sort})


@login_required
def category_detail(request, pk):
     category = get_object_or_404(Category, pk=pk)

     items = Item.objects.filter(category=category, user=request.user).select_related("subcategory")
     
     for item in items:
          item.subtotal = item.price * item.quantity

         # Calcula o valor total da categoria direto no banco
     total_value = items.aggregate(
        total=Sum(ExpressionWrapper(F("price") * F("quantity"), output_field=DecimalField()))
    )["total"] or 0

     return render(request, "inventory/category_detail.html", {
        "category": category,
        "items": items,
        "total_value": total_value,
    })



@login_required
def item_details(request, pk):
     item = get_object_or_404(Item, pk=pk, user=request.user)
     return render(request, 'inventory/item_details.html', {'item': item})

def login_view(request):
     if request.method == 'POST':
          form = LoginForm(request.POST)
          if form.is_valid():
               #auth and make login
               user = form.get_user()
               login(request, user)
               messages.success(request, f"Bem Vindo, {user.username}")
               return redirect('homepage')
          else:
               messages.error(request, "Usuário ou senha inváldio   ")
     else:
            form = LoginForm()
     return render(request, 'inventory/User/login.html',{"form":form})

def register_view(request):
     if request.method == "POST":
          form = RegisterForm(request.POST)
          if form.is_valid():
               user = form.save(commit=False)
               user.username = user.email.split('@')[0]  # gera username automático
               user.save()
               messages.success(request, "Conta Criada com Sucesso. Agora faça login")
               return redirect('login_view')
          else:
               messages.error(request, "Corrija os erros abaixo")
     else:
        form = RegisterForm()
     return render(request, 'inventory/User/register.html', {"form": form})

@login_required
def logout_view(request):
     logout(request)
     messages.info(request, "Você saiu da sua conta.")
     return redirect('login_view')


@admin_mode_required
@login_required
def create_product(request):
    #when the user register a new subcategory we get to the form
    category_id = request.GET.get('category_id')
    subcategory_id = request.GET.get('subcategory_id')
    
    inital_data = {}
#if the user already register, we try to get 
    if category_id:
            try:
                inital_data['category']  = Category.objects.get(id=category_id)
            except Category.DoesNotExist:
                pass
    
    if subcategory_id:
            try:
                inital_data['subcategory'] = SubCategory.objects.get(id=subcategory_id)  
            except SubCategory.DoesNotExist:
                pass          

    if request.method == 'POST':        #check if was a POST
        form = ItemForm(request.POST, request.FILES, user=request.user)   #IF yes, takes the parameter by the USER CREATE A FORM AND SAVE ON DB 
        if form.is_valid():
            #link product with user
            product  = form.save(commit=False)
            product.user = request.user 
            product.save()

            if product.quantity and product.quantity > 0:
                 StockMovement.objects.create(
                      item=product,
                      tipo=StockMovement.ENTRADA,
                      quantidade=product.quantity if product.quantity else 0,
                      quantidade_antes=0,
                      user=request.user,
                      observacao="Movimentação criada automaticamente ao cadastrar produto"
                 )
            return redirect('homepage')
    else:     
        #when the user register subcategory, we already take 
        form = ItemForm(initial=inital_data, user=request.user)               #create the form and if we have the other context give to the forms

    return render(request, 'inventory/Create_Product/create_product.html',{"form":form})   #send the object to the form
@admin_mode_required
@login_required
def create_category(request):
    next_url = request.GET.get('next', '/')     #take the URL, beside next to save to redirect where the user was

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)  # ← não salva ainda 
            category.user = request.user
            category.save()
            messages.success(request, "Categoria criada com sucesso!")

            #redirect to the previous page
            redirect_url = f"{next_url}?category_id={category.id}"  #send the ID of the category
            return redirect(redirect_url)
    else:
            form = CategoryForm()

    return render(request, 'inventory/Create_Product/create_category.html', {"form":form})
@admin_mode_required
@login_required
def create_subcategory(request):
    next_url = request.GET.get('next', '/')         #take the previous path
    category_id  = request.GET.get('category_id')
    category = None

    if category_id:
            try: 
                 category = Category.objects.get(id=category_id)
            except Category.DoesNotExist:
                 category = None

    if request.method == 'POST':
        form = SubCategoryForm(request.POST)
        if form.is_valid():
            subcategory = form.save()
            #redirect previous page with the context of the category and subcategory
            redirect_url = f"{next_url}?category_id={subcategory.category.id}&subcategory_id={subcategory.id}" #send to the context
            return redirect(redirect_url)
    else:
        inital_data = {}
        if category_id:
            inital_data['category'] = category_id
        form = SubCategoryForm(initial=inital_data)     #pass the DATAS already to the form as context

    return render(request, 'inventory/Create_Product/create_subcategory.html', {"form":form, "category": category})



@login_required
def move_stock(request, pk):
    if not pk:
         raise Http404("Item não especificado")
    
    item = get_object_or_404(Item, pk=pk, user=request.user)  if pk else None
    tipo = request.GET.get('tipo')
         
    if request.method == 'POST':
          form = StockMovementForm(request.POST, user=request.user)
          if form.is_valid():
               form.save()
               return redirect('item_details', pk=pk)
    else:
        inital_data = {'item': item }
        if tipo:
             inital_data['tipo'] = tipo

        form = StockMovementForm(initial=inital_data, user=request.user)

    return render(request,'inventory/move_stock.html', {'form': form, 'item': item})


@login_required
def minimun_stock(request):
    produtos_com_estoque_baixo = Item.objects.filter(
        user=request.user
    ).filter(
        quantity__lt=F('minimum_stock')  # 👈 compara com o campo do próprio item
    )

  
                                                                                
    return render(request, 'inventory/minimun_stock.html', {'produtos_com_estoque_baixo': produtos_com_estoque_baixo})
@admin_mode_required
@login_required
def stock_movement_report(request):
    itens_movimentados = StockMovement.objects.filter(user=request.user).order_by('-data')  #from newest to the oldest

    #for item_movimentado in itens_movimentados:
     #   print(f"Item {item_movimentado.item.name} - Quantidade {item_movimentado.quantidade} - FROM {item_movimentado.user.email} e {item_movimentado.images}")
    return render(request,'inventory/stock_movement_report.html', {'itens_movimentados': itens_movimentados, })

@admin_mode_required
@login_required
def edit_product(request, pk):

     item = get_object_or_404(Item, pk=pk, user=request.user) 

     if request.method == 'POST':
        form = ItemEditForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
             form.save()
             messages.success(request, "Produto Atualizado com Sucesso!")
             return redirect('homepage')
        else:
             messages.error(request, "Erro ao atualizar o produto. Verifique os campos.")
             print(form.errors)
     else:
        form = ItemEditForm(instance=item)

  
     
     return render(request, 'inventory/edit_product.html', {'form': form, 'item': item})

@admin_mode_required    
@login_required
def delete_product(request, pk):
    try:
         item = get_object_or_404(Item, pk=pk, user=request.user)
    except Exception as e:
          messages.error(request, "Produto não encontrado ou você não tem permissão para excluí-lo")
          return redirect('homepage') 
       
    if request.method != 'POST':
          messages.error(request, "Método inválido para exclusão.")
          return redirect('edit_product', pk=pk)
    try:
          item.delete()
          messages.success(request, "Produto excluído com sucesso")
    except Exception as e:
          print(f"[ERRO AO DELETAR PRODUTO] ID {pk}, ERRO {e}")
          messages.error(request, "Erro interno ao excluir produto. Tente novamente mais tarde.")
          return redirect('edit_product', pk=pk)
          
    return redirect('homepage')
    

@login_required
def report_stock_movement(request):
     try:
        movimentacoes = StockMovement.objects.filter(user=request.user).select_related("item").order_by("-data")

        #apliy filters
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")
        tipo = request.GET.get("tipo")
        quant_min = request.GET.get("quant_min")
        quant_max = request.GET.get("quant_max")
      
        if start_date:
             movimentacoes = movimentacoes.filter(data__date__gte=start_date)
        if end_date:
             movimentacoes = movimentacoes.filter(data__date__lte=end_date)
        if tipo in ["E", "S"]:
             movimentacoes = movimentacoes.filter(tipo=tipo)
        if quant_min:
             movimentacoes = movimentacoes.filter(quantidade__gte=quant_min)
        if quant_max:
             movimentacoes = movimentacoes.filter(quantidade__lte=quant_max)


        
        if not movimentacoes.exists():
             messages.info(request, "Você ainda não possui movimentações")
     except DatabaseError as e:
            print(f"Erro ao buscar movimentações {e}")
            movimentacoes = []
            messages.error(request, "Ocorreu um erro ao carregar as suas movimentações")            
          
     return render(request, 'inventory/report_stock_movement.html', {"movimentacoes" : movimentacoes})

@login_required
def dowloand_report_pdf(request):
    movimentacoes = StockMovement.objects.filter(user=request.user)

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    tipo = request.GET.get('tipo')
    quant_min = request.GET.get('quant_min')
    quant_max = request.GET.get('quant_max')
    
    filtros_aplicados = []
    if start_date:
        movimentacoes = movimentacoes.filter(data__gte=start_date)
        filtros_aplicados.append(f"Data Inicial - {start_date}")
    if end_date:
        movimentacoes = movimentacoes.filter(data__lte=end_date)
        filtros_aplicados.append(f"Data Final - {end_date}")
    if tipo:
        movimentacoes = movimentacoes.filter(tipo=tipo)
        filtros_aplicados.append(f"Tipo de Movimentação - {tipo}")
    if quant_min:
        movimentacoes = movimentacoes.filter(quantidade__gte=quant_min)
        filtros_aplicados.append(f"Quantidade Mínima - {quant_min}")
    if quant_max:
        movimentacoes = movimentacoes.filter(quantidade__lte=quant_max)
        filtros_aplicados.append(f"Quantidade Máxima - {quant_max}")



    #response HTTP saying is a PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report_stock.pdf'

    #create object PDF
    doc = SimpleDocTemplate(response, pagesize=A4)
    styles = getSampleStyleSheet()

    elementos = []
    print(filtros_aplicados)
    #title of report
    elementos.append(Paragraph(f"Relatório de Movimentações - {request.user.email}", styles['Heading1']))
    
    if filtros_aplicados:
        elementos.append(Paragraph("Filtros Aplicados no Relatório"))
        for filtro in filtros_aplicados:
            elementos.append(Paragraph(filtro, styles["Normal"]))
    
    elementos.append(Spacer(1, 5*mm))

    #table with data
    data = [["Data", "Item", "Tipo", "Quantidade", "Quantidade Antes", "Quantidade Atual"]]
    for mov in movimentacoes:
         quantidade_antes = mov.quantidade_antes or 0
         quantidade_atual = mov.item.quantity or 0

         data.append([
              mov.data.strftime("%d/%m/%Y %H:%M"),
              mov.item.name,
              "Entrada" if mov.tipo == "E" else "Saída",
              str(mov.quantidade),
              str(quantidade_antes if quantidade_antes > 0 else 0),
              str(quantidade_atual if quantidade_atual > 0 else 0),
            
         ])

    tabela = Table(data, colWidths=[70,160,50,60,80,80,100])

    tabela.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#3498DB")),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("ALIGN", (3, 1), (5, -1), "CENTER"),  # Centraliza colunas numéricas
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTSIZE", (0, 0), (-1, -1), 8),  # Fonte menor
    ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ]))
    
    
    elementos.append(tabela)

    doc.build(elementos)

    return response
