import pandas as pd

def preprocess_raw_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and preprocess raw order data"""
    # Create a copy to avoid modifying original
    df = df.copy()
    
    # Filter unwanted order types
    df = df[df['order_type'] != "Delivery(Parcel)"]

    # Remove rows with certain items (water, cigarettes etc)
    banned_patterns = r"(?i)\b(water|water bottle|1 ltr|cigarette|cigarettes)\b"
    df = df[~df['item_name'].str.contains(banned_patterns, na=False, regex=True)]
        
    # Define numeric columns
    numeric_cols = [
        'my_amount', 'total_tax', 'discount', 'delivery_charge',
        'container_charge', 'service_charge', 'additional_charge',
        'waived_off', 'round_off', 'total', 'item_price', 
        'item_quantity', 'item_total'
    ]
    
    # Convert to numeric
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Fill nulls in discount columns
    df[['discount', 'waived_off']] = df[['discount', 'waived_off']].fillna(0)
    
    # Drop incomplete rows
    required_cols = ['invoice_no', 'item_name', 'item_quantity', 'item_total']
    df.dropna(subset=required_cols, inplace=True)
    
    # Compute net sales
    df['net_sales'] = df['item_total'] - df[['discount', 'waived_off']].sum(axis=1)
    
    # Add time features
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
        df['YearMonth'] = df['date'].dt.to_period('M')
        df['DateOnly'] = df['date'].dt.date
        df['Weekday'] = df['date'].dt.day_name()
        df['Hour'] = df['date'].dt.hour
    
    return df