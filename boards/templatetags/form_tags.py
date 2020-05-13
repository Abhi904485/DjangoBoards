from django import template

register = template.Library()


@register.filter
def input_class(bound_field):
    css_class = ""
    if bound_field.form.is_bound:
        if bound_field.errors:
            css_class = "is-invalid"
        elif field_type(bound_field) != "PasswordInput" or field_type(bound_field) != "EmailInput":
            css_class = "is-valid"
    return "form-control {}".format(css_class)


@register.filter
def field_type(bound_field):
    return bound_field.field.widget.__class__.__name__
