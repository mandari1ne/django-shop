from django import forms
from .models import CartItem

class AddToCartForm(forms.Form):
    # not empty
    size_id = forms.IntegerField(required=False)

    quantity = forms.IntegerField(min_value=1, initial=1)

    def __init__(self, *args, product=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.product = product

        if product:
            # gt - stock >=0
            sizes = product.product_sizes.filter(stock__gt=0)

            if sizes.exists():
                self.fields['size_id'] = forms.ChoiceField(
                    choices=[(ps.id, ps.size) for ps in sizes],
                            required=True,
                    initial=sizes.first().id
                )

class UpdateCartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['quantity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # существует ли объект модели и у него есть связанный product_size
        if self.instance and self.instance.product_size:
            # добавляет max кол-во на складе
            self.fields['quantity'].validators.append(
                forms.validators.MaxValueValidator(self.instance.product_size.stock)
            )
