from django import forms
from django.utils.safestring import mark_safe


class DeliveryMethodWidget(forms.RadioSelect):
    def render(self, name, value, attrs=None, renderer=None):
        output = []
        for option, label in self.choices:
            label = label.split('|')
            if isinstance(label, (tuple, list)):
                option_label = label[0]
                price = label[1] + ' руб.'
                if 'None' in price:
                    price = 'бесплатно'
            else:
                option_label = label
                price = ''

            output.append(f'<div><label><input type="radio" name="{name}" value="{option}"')
            if str(value) == str(option):
                output.append(' checked="checked"')
            output.append(f'><div class=labprice>'
                          f'<div class="option__label">{option_label}</div>'
                          f'<div class="label__price">{price}</div>'
                          f'</div>'
                          f'</label></div>')

        return mark_safe('\n'.join(output))