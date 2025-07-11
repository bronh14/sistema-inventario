def validate_positive_integer(value):
    if not isinstance(value, int) or value < 0:
        raise ValueError("El valor debe ser un número entero positivo.")
    return value

def format_currency(value):
    return f"${value:,.2f}"

def format_material_list(materials):
    return "\n".join([f"{material['nombre']}: {material['cantidad']}" for material in materials])

def prompt_user_input(prompt):
    return input(prompt).strip()