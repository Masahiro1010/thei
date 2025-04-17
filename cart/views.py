from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product

class AddToCartView(View):
    def post(self, request, product_id):
        cart = request.session.get('cart', {})
        product_id = str(product_id)

        if product_id in cart:
            cart[product_id]['quantity'] += 1
        else:
            cart[product_id] = {'quantity': 1}

        request.session['cart'] = cart
        return redirect('cart_detail')


class RemoveFromCartView(View):
    def post(self, request, product_id):
        cart = request.session.get('cart', {})
        product_id = str(product_id)

        if product_id in cart:
            del cart[product_id]
            request.session['cart'] = cart

        return redirect('cart_detail')


class CartDetailView(View):
    def get(self, request):
        cart = request.session.get('cart', {})
        cart_items = []
        total_price = 0

        for product_id, item in cart.items():
            product = get_object_or_404(Product, pk=product_id)
            subtotal = product.price * item['quantity']
            total_price += subtotal

            cart_items.append({
                'product': product,
                'quantity': item['quantity'],
                'subtotal': subtotal,
            })

        context = {
            'cart_items': cart_items,
            'total_price': total_price,
        }
        return render(request, 'cart/cart_detail.html', context)
