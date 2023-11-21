import datetime
import simplejson as json

def generate_order_number(pk):
    current_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    order_number = current_time + str(pk)

    return order_number

def order_total_by_vendor(order, vendor_id):
    total_data = order.total_data
    data = total_data.get(str(vendor_id))
    subtotal = 0
    tax = 0
    tax_dict = {}

    for key, val in data.items():
        subtotal += float(key)

        if isinstance(val, str):
            val = val.replace("'", '"')
            val = json.loads(val)
        elif not isinstance(val, dict):
            # Handle the case where val is neither a string nor a dictionary
            continue
        
        tax_dict.update(val)
        # Calculate tax
        for tax_type, tax_rates in val.items():
            for rate, amount in tax_rates.items():
                tax += float(amount)

    total = float(subtotal) + float(tax)
    context = {
        'subtotal': subtotal,
        'tax_dict': tax_dict, 
        'total': total,
    }

    return context