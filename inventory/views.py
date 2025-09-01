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


# Create your views here.

@login_required
def homepage(request):  #after the urls.py direct to here, the function decide what to make. If shows or save what the user maked

    #filter products by user
    itens = Item.objects.filter(user=request.user)

    return render(request, 'inventory/homepage.html', {'itens':itens})

@login_required
def item_details(request, pk):
     item = get_object_or_404(Item, pk=pk, user=request.user)
     return render(request, 'inventory/item_details.html', {'item': item})

def login_view(request):
     if request.method == 'POST':
          form = LoginForm(data=request.POST)
          if form.is_valid():
               #auth and make login
               user = form.get_user()
               login(request, user)
               return redirect('homepage')
     else:
            form = LoginForm()
     return render(request, 'inventory/User/login.html',{"form":form})

def logout_view(request):
     logout(request)
     return redirect('login')

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
        form = ItemForm(request.POST, request.FILES)   #IF yes, takes the parameter by the USER CREATE A FORM AND SAVE ON DB 
        if form.is_valid():
            #link product with user
            product  = form.save(commit=False)
            product.user = request.user 
            product.save()
            return redirect('homepage')
    else:     
        #when the user register subcategory, we already take 
        form = ItemForm(initial=inital_data)               #create the form and if we have the other context give to the forms

    return render(request, 'inventory/Create_Product/create_product.html',{"form":form})   #send the object to the form

@login_required
def create_category(request):
    next_url = request.GET.get('next', '/')     #take the URL, beside next to save to redirect where the user was

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category =  form.save() 
            #redirect to the previous page
            redirect_url = f"{next_url}?category_id={category.id}"  #send the ID of the category
            return redirect(redirect_url)
    else:
            form = CategoryForm()

    return render(request, 'inventory/Create_Product/create_category.html', {"form":form})

@login_required
def create_subcategory(request):
    next_url = request.GET.get('next', '/')         #take the previous path
    category_id  = request.GET.get('category_id')

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

    return render(request, 'inventory/Create_Product/create_subcategory.html', {"form":form})



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
     produtos_com_estoque_baixo = Item.objects.filter(user=request.user, quantity__lt=10)        #compare with the field minimum stock
   
     return render(request, 'inventory/minimun_stock.html', {'produtos_com_estoque_baixo': produtos_com_estoque_baixo})

@login_required
def stock_movement_report(request):
    itens_movimentados = StockMovement.objects.filter(user=request.user).order_by('-data')  #from newest to the oldest

    #for item_movimentado in itens_movimentados:
     #   print(f"Item {item_movimentado.item.name} - Quantidade {item_movimentado.quantidade} - FROM {item_movimentado.user.email} e {item_movimentado.images}")
    return render(request,'inventory/stock_movement_report.html', {'itens_movimentados': itens_movimentados, })


@login_required
def edit_product(request, pk):
     if not pk:
          raise Http404("Item não especificado para a edição")

     item = get_object_or_404(Item, pk=pk, user=request.user) if pk else None
     form = ItemEditForm()

 #    if request.method == 'POST':
  #      pass   
     
     return render(request, 'inventory/edit_product.html', {'form': form})


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
      
        print()
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


        
        if not movimentacoes.exists:
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
    elementos.append(Paragraph(f"Relatório de Movimentações - {request.user.username}", styles['Heading1']))
    
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

    tabela = Table(data, colWidths=[70,90,50,60,80,80,100])

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
