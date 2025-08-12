import pandas as pd
from itertools import combinations
from collections import Counter
from pathlib import Path

from app.utils.preprocessing import preprocess_raw_data


class OrderAnalyzer:
    """Analyzes order-level KPIs and patterns"""

    def compute_invoice_aggregation(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Aggregates invoice-level metrics.
        Returns invoice-level dataframe.
        """
        # Calculate basket size (unique items per invoice)
        basket_sizes = df.groupby('invoice_no')['item_name'].nunique().rename('basket_size')
       
        # Aggregate
        invoice_kpis = (
            df.groupby('invoice_no').agg(
                order_date=('date', 'min'),
                total_quantity=('item_quantity', 'sum'),
                total_discount=('discount', 'sum'),
                total_waived_off=('waived_off', 'sum'),
                net_invoice_value=('net_sales', 'sum')
            )
        )
       
        # Merge basket sizes
        invoice_kpis = invoice_kpis.join(basket_sizes)
       
        # Additional time features
        invoice_kpis['order_day'] = invoice_kpis['order_date'].dt.day_name()
        invoice_kpis['order_hour'] = invoice_kpis['order_date'].dt.hour
       
        invoice_kpis = invoice_kpis.reset_index()
        return invoice_kpis
   
    def compute_cooccurrence_matrix(self, df: pd.DataFrame, top_n: int = 30) -> pd.DataFrame:
        """
        Builds item co-occurrence matrix, filtered to top N most frequent items.
        Returns the symmetric matrix dataframe.
        """
        # Group items by invoice
        invoice_items = df.groupby('invoice_no')['item_name'].apply(list).reset_index()
       
        # Build pair counts
        pair_counter = Counter()
        for items in invoice_items['item_name']:
            unique_items = list(set(items))
            if len(unique_items) > 1:
                pairs = combinations(sorted(unique_items), 2)
                pair_counter.update(pairs)
       
        co_occurrence_df = pd.DataFrame(pair_counter.items(), columns=['item_pair', 'count'])
        co_occurrence_df[['item_1', 'item_2']] = pd.DataFrame(co_occurrence_df['item_pair'].tolist(), index=co_occurrence_df.index)
        co_occurrence_df.drop(columns='item_pair', inplace=True)
       
        # Build symmetric matrix
        matrix_df = pd.pivot_table(
            co_occurrence_df,
            values='count',
            index='item_1',
            columns='item_2',
            fill_value=0
        )
        full_matrix = matrix_df + matrix_df.T.fillna(0)
       
        # Limit to top-N items
        top_items = df['item_name'].value_counts().head(top_n).index
        filtered_matrix = full_matrix.loc[top_items, top_items]
       
        return filtered_matrix


def run_order_analysis(df: pd.DataFrame):
    
    df = preprocess_raw_data(df)
    analyzer = OrderAnalyzer()

    invoice_df = analyzer.compute_invoice_aggregation(df)
    cooc_matrix_df = analyzer.compute_cooccurrence_matrix(df)
   
    return invoice_df, cooc_matrix_df
