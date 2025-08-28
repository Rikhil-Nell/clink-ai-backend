import asyncio
import asyncpg
import pandas as pd
from typing import Literal
import json

from app.crud.analysis_crud import analysis_crud
from app.utils.preprocessing import preprocess_raw_data
from app.utils.data_transformer import flatten_order_data_to_dataframe

# Import your three specific analysis engines
from app.analysis.customer_analysis import run_customer_analysis
from app.analysis.order_analysis import run_order_analysis
# from app.analysis.product_analysis import run_product_analysis

# And your three summarization functions
from app.summarization.customer_kpi_summarization import run_customer_summarization
from app.summarization.order_kpi_summarization import run_order_summarization
# from app.summarization.product_kpi_summarization import run_product_summarization

AnalysisType = Literal["customer", "product", "order"]

async def _run_one_analysis( 
    pool: asyncpg.Pool, 
    df: pd.DataFrame, 
    loyalty_program_id: int, 
    analysis_type: AnalysisType
):
    """A generic worker that runs one type of analysis."""
    print(f"Running {analysis_type} analysis...")
    
    analysis_map = {
        "customer": (run_customer_analysis, run_customer_summarization),
        "order": (run_order_analysis, run_order_summarization),
    }
    
    analysis_func, summarization_func = analysis_map[analysis_type]

    analysis_results = analysis_func(df)

    summary_json = None
    
    if analysis_type == "customer":
        kpi_df = analysis_results
        summary_json = summarization_func(kpi_df)
        
    elif analysis_type == "order":
        invoice_df, cooc_matrix = analysis_results
        summary_json = summarization_func(invoice_df=invoice_df, cooc_matrix=cooc_matrix)

    if summary_json:
        await analysis_crud.save_analysis_result(
            pool=pool,
            loyalty_program_id=loyalty_program_id,
            analysis_type=f"{analysis_type}_summary",
            result_json=summary_json
        )
        print(f"✅ Completed and saved {analysis_type} analysis.")
    else:
        print(f"⚠️ Could not generate summary for {analysis_type} analysis.")

async def trigger_all_analyses(pool: asyncpg.Pool, loyalty_program_id: int):
    """
    Orchestrator that fetches data, TRANSFORMS IT, preprocesses, 
    and then runs all analysis types concurrently.
    """
    print(f"Starting all analyses for loyalty program: {loyalty_program_id}")
    
    # 1. Fetch the raw list of nested JSON orders from the database
    raw_orders_list = await analysis_crud.get_all_orders_as_list(pool, loyalty_program_id)
    
    if not raw_orders_list:
        print("No orders found. Aborting analysis.")
        return
        
    # 2. **THE CRITICAL STEP:** Transform the nested JSON into a flat DataFrame
    flat_df = flatten_order_data_to_dataframe(raw_orders_list)

    # 3. Now, your existing preprocessing function will work correctly
    preprocessed_df = preprocess_raw_data(flat_df)

    # 4. Run all analysis pipelines in parallel
    await asyncio.gather(
        _run_one_analysis(pool, preprocessed_df.copy(), loyalty_program_id, "customer"),
        _run_one_analysis(pool, preprocessed_df.copy(), loyalty_program_id, "order")
        # _run_one_analysis(pool, preprocessed_df.copy(), loyalty_program_id, "product"),
    )
    
    print(f"All analyses complete for program: {loyalty_program_id}")