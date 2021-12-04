from django.http import response,JsonResponse
from django.shortcuts import render,get_object_or_404
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.sessions.models import Session

# Create your views here.
def cart_session_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def cart(request,quantity=0,cart_items=None):
    try:
        if request.user.is_authenticated:
            cart_item = Cart.objects.filter(user=request.user, is_active=True).order_by('id')
        else:
            cart = Cart.objects.get(cart_id=cart_session_id(request))
            cart_item = Cart.objects.filter(cart=cart, is_active=True).order_by('id')
        count = cart_item.count()   
        context = {
            'cart_item':cart_item,
            'count':count
        }
        return response(context)
    except ObjectDoesNotExist:
      pass
      
def add_cart(request,course,cart_items=None):
    current_user = request.user
    product = Course.objects.get(id=course)
    if current_user.is_authenticated:
      
        if Cart.objects.filter(course=product, user=current_user).exists():
            cart_item = Cart.objects.get(course=product, user=current_user)
            cart_item.quantity += 1
            cart_item.save()

        else:
            cart_item = Cart.objects.create(
                product = product,
                quantity = 1,
                user = current_user,
            )
            cart_item.save()
            return JsonResponse(cart_item)

    else:
        try:
            cart = Cart.objects.get(cart_id=cart_session_id(request)) # get the cart using the cart_id present in the session
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = cart_session_id(request)
            )
        cart.save()

        try:
            cart_item = Cart.objects.get(course=product, cart=cart)
            cart_item.quantity += 1
            cart_item.save()

        except Cart.DoesNotExist:
            cart_item = Cart.objects.create(
                product = product,
                quantity = 1,
                cart = cart,
            )
            cart_item.save() 
            return JsonResponse(cart_item)  
def minus_cart(request,course):
    current_user = request.user
    if current_user.is_authenticated:
        product = get_object_or_404(Course,id=course)
        cart_item = Cart.objects.get(course= product,user=current_user)
        if cart_item.quantity > 1:
            cart_item.quantity -=1 
            cart_item.save()
        else:
            cart_item.delete()

    else:
        cart = Cart.objects.get(cart_id= cart_session_id(request))
        product = get_object_or_404(Course,id=course)
        cart_item = Cart.objects.get(course= product,cart=cart)
        if cart_item.quantity > 1:
            cart_item.quantity -=1 
            cart_item.save()
        else:
            cart_item.delete()
       
def delete_cart(request,product_id):
    current_user = request.user
    if current_user.is_authenticated:
        product = get_object_or_404(Course,id=product_id)
        cart_item = Cart.objects.get(course=product,user=current_user)
        cart_item.delete()
    else:
        cart= Cart.objects.get(cart_id= cart_session_id(request))
        product = get_object_or_404(Course,id=product_id)
        cart_item = Cart.objects.get(course=product,cart=cart)
        cart_item.delete()


