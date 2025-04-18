from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product
import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.generic import TemplateView

stripe.api_key = settings.STRIPE_SECRET_KEY

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
            'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        }
        return render(request, 'cart/cart_detail.html', context)
    
class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        cart = request.session.get('cart', {})
        line_items = []

        for product_id, item in cart.items():
            from store.models import Product
            product = Product.objects.get(pk=product_id)
            line_items.append({
                'price_data': {
                    'currency': 'jpy',
                    'product_data': {
                        'name': product.name,
                    },
                    'unit_amount': product.price,
                },
                'quantity': item['quantity'],
            })

        if not line_items:
            return JsonResponse({'error': 'カートが空です'}, status=400)

        # ✅ 自動でドメインを取得（http or https も含める）
        scheme = request.scheme  # "http" or "https"
        host = request.get_host()  # "127.0.0.1:8000" or "the-i.onrender.com"
        YOUR_DOMAIN = f"{scheme}://{host}"

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=YOUR_DOMAIN + '/cart/success/',
            cancel_url=YOUR_DOMAIN + '/cart/cancel/',
        )

        return JsonResponse({'id': session.id})
    
class SuccessView(View):
    def get(self, request, *args, **kwargs):
        print("SuccessView called")
        # カートの中身をクリア
        if 'cart' in request.session:
            del request.session['cart']
        return render(request, 'cart/success.html')

class CancelView(TemplateView):
    template_name = "cart/cancel.html"
