import pandas as pd
from typing import List, Dict, Any

def flatten_order_data_to_dataframe(raw_orders: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Transforms a list of nested order JSON objects into a flat DataFrame
    where each row represents a single item.
    """
    flattened_data = []
    
    for order in raw_orders:
        # Loop through each item in the OrderItem list
        for item in order.get("OrderItem", []):
            flat_row = {
                # --- Mapped Data ---
                'restaurant_name': order.get("Restaurant", {}).get("res_name"),
                'invoice_no': order.get("Order", {}).get("orderID"),
                'date': order.get("Order", {}).get("created_on"),
                'payment_type': order.get("Order", {}).get("payment_type"),
                'order_type': order.get("Order", {}).get("order_type"),
                'customer_phone': order.get("Customer", {}).get("phone"),
                'customer_name': order.get("Customer", {}).get("name"),
                'persons': order.get("Order", {}).get("no_of_persons"),
                'total_tax': order.get("Order", {}).get("tax_total"),
                'discount': order.get("Order", {}).get("discount_total"),
                'delivery_charge': order.get("Order", {}).get("delivery_charges"),
                'round_off': order.get("Order", {}).get("round_off"),
                'total': order.get("Order", {}).get("total"),
                
                # --- Item-Specific Data ---
                'item_name': item.get("name"),
                'item_price': item.get("price"),
                'item_quantity': item.get("quantity"),
                'item_total': item.get("total"),
                
                # --- Missing Data (added with default values) ---
                'waived_off': 0,
                'my_amount': order.get("Order", {}).get("core_total"),
                'category_name': None,
                # ... add any other missing columns your analysis needs
            }
            flattened_data.append(flat_row)
            
    return pd.DataFrame(flattened_data)