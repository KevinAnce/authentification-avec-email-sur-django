from django import template

register = template.Library()

@register.filter
def add_css_classes(field, css_classes):
    css_classes = css_classes.split()
    return field.as_widget(attrs={'class': ' '.join(css_classes)})
