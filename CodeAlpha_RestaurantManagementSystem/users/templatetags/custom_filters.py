from django import template

register = template.Library()

@register.filter
def get_item(form, dish_id):
    """Get form field for a specific dish ID"""
    field_name = f'quantity_{dish_id}'
    return form[field_name]