from django.db.models import Count
from django.shortcuts import render, redirect
from .forms import RegisterForm, VerifyForm
from django.contrib import messages
from .models import User, Product, Cart
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .forms import RequestForm
from django.http import JsonResponse
from django.db.models import Q



# @login_required(login_url="app:register")
def index(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    form = RequestForm()
    main_category = Product.objects.values('main_category').distinct()
    new_arrivals = Product.objects.order_by('-created_at', '-updated_at')
    product = Product.objects.all()

    # main_category_count = Product.objects.values('main_category').distinct().count()
    # context = {'main_category':main_category, 'product':product, 'new_arrivals':new_arrivals, 'form':form}
    return render(request, "app/index.html", locals())


def detail(request, id):
    item = Product.objects.get(id=id)
    product = Product.objects.filter(id=id).values('name')

    context = {'item':item, 'product':product}
    return render(request, "app/detail.html",context)

def category(request, main_category):
    product = Product.objects.filter(main_category=main_category)
    product_count = product.count()
    sub_category = Product.objects.filter(main_category=main_category).values('sub_category').annotate(total=Count('sub_category'))
    sub_type_category = Product.objects.filter(main_category=main_category).values('sub_type_category').annotate(total=Count('sub_type_category'))

    brand = Product.objects.filter(main_category=main_category).values('brand').annotate(total=Count('brand'))
    # context = {'product':product, 'main_category':main_category,'sub_category':sub_category, 'brand':brand, 'sub_type_category':sub_type_category, 'product_count':product_count}
    return render(request, "app/category.html",locals())

def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)

    # Check if the item is already in the cart
    cart_item = Cart.objects.filter(user=user, product=product).first()
    if cart_item:
        # If it is, just update the quantity
        cart_item.quantity += 1
        cart_item.save()
    else:
        # If not, create a new cart entry
        Cart(user=user, product=product, quantity=1).save()

    return redirect('app:cart')

    # return render(request, "app/addtocart.html")


def cart_view(request):
    user = request.user
    cart = Cart.objects.filter(user=user)

    shipping_amount = 10.00
    amount = 0
    totalamount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + value
    totalamount = amount + 10

    # context = {'cart':cart, 'amount':amount, 'totalamount':totalamount}
    return render(request, 'app/addtocart.html', locals())

def get_cart_count(request):
    if request.user.is_authenticated:
        cart_count = Cart.objects.filter(user=request.user).count()
        return JsonResponse({'cart_count': cart_count})
    else:
        return JsonResponse({'cart_count': 0})

def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        totalamount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 10
        print(prod_id)
        data = {
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)

def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        totalamount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 10
        print(prod_id)
        data = {
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)

def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        totalamount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 10
        print(prod_id)
        data = {
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
    

# def remove_cart(request):
#     if request.method == 'GET':
#         prod_id = request.GET.get('prod_id')
        
#         cart_item = get_object_or_404(Cart, product_id=prod_id, user=request.user)
        
#         cart_item.delete()
        
#         return JsonResponse({'success': True})



# user_authentication
def register(request):
    if request.user.is_authenticated:
        return redirect('index')

    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        phone_number = request.POST.get('phone_number')
        if form.is_valid():
            # user not registered
            user = form.save()
            user.save()
            request.session['pk'] = user.pk
            request.session.modified = True
            return redirect('app:verify')
        else:
            # registered users
            user = User.objects.get(phone_number=phone_number)
            if User.objects.filter(phone_number=phone_number).exists():
                if user is not None:
                    request.session['pk'] = user.pk
                    request.session.modified = True
                    return redirect('app:verify')
                return render(request, "app/register.html", {'form': form})

            messages.warning(request, "An error occurred durin registration")

    # context = {'form': form}
    return render(request, "app/register.html", locals())


def verify(request):
    if request.user.is_authenticated:
        return redirect('index')

    form = VerifyForm(request.POST or None)
    pk = request.session.get('pk')
    if pk:
        user = get_object_or_404(User, pk=pk)
        code = user.code
        code_user = f"{code}"
        if not request.POST:
            pass
            # send_sms(code_user, user.phone_number)
        print(code)
        if request.method == 'POST':
            if form.is_valid():
                num = form.cleaned_data.get('number')

                if str(code) == num:
                    user.save()
                    login(request, user)
                    # messages.success(request, "Successfully logged in")
                    print(user.pk)
                    return redirect('app:index')
                else:
                    messages.warning(request, "Authentication failed")

                    return redirect('app:verify')

    # context = {'form': form}
    return render(request, "app/verify.html", locals())


def logoutuser(request):
    logout(request)
    return redirect('app:index')
