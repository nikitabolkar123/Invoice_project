from rest_framework import serializers
from .models import Invoice, InvoiceDetail
from django.db import transaction


class InvoiceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceDetail
        fields = '__all__'
        extra_kwargs = {
            'invoice': {'required': False},  # we are making the invoice field not required
        }


class InvoiceSerializer(serializers.ModelSerializer):
    invoice_details = InvoiceDetailSerializer(many=True, required=False)

    class Meta:
        model = Invoice
        fields = '__all__'

    def create(self, validated_data):
        invoice_details_data = validated_data.pop('invoice_details', [])

        with transaction.atomic():
            invoice = Invoice.objects.create(**validated_data)
            for detail_data in invoice_details_data:
                InvoiceDetail.objects.create(invoice=invoice, **detail_data)

        return invoice










    # def create(self, validated_data):
    #     print(validated_data)
    #     invoice_details_data = validated_data.pop('invoice_details',[])
    #     invoice = Invoice.objects.create(**validated_data)
    #     for invoice_detail_data in invoice_details_data:
    #         invoice_detail_data.update({"invoice_id": invoice.id})
    #         print(invoice_detail_data)
    #         InvoiceDetail.objects.create(**invoice_detail_data)
    #     return invoice
