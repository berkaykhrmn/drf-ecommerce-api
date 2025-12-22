from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from orders.models import Order
from payments.services import create_payment

class PaymentAPIView(APIView):
    def post(self, request, order_id):
        order = Order.objects.get(id=order_id, user=request.user)
        payment_result = create_payment(request.user, order)
        return Response(payment_result, status=status.HTTP_200_OK)