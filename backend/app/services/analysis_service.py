import asyncio
import asyncpg
import pandas as pd
from typing import Literal

from app.crud.analysis_crud import analysis_crud
from app.utils.preprocessing import preprocess_raw_data

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
    
    # Map analysis type to the correct functions
    analysis_map = {
        "customer": (run_customer_analysis, run_customer_summarization),
        "order": (run_order_analysis, run_order_summarization),
        # "product": (run_product_analysis, run_product_summarization),
    }
    
    analysis_func, summarization_func = analysis_map[analysis_type]
    
    kpi_df = analysis_func(df)
    summary_json = summarization_func(kpi_df)
    
    await analysis_crud.save_analysis_result(
        pool=pool,
        loyalty_program_id=loyalty_program_id,
        analysis_type=f"{analysis_type}_summary",
        result_json=summary_json
    )
    print(f"✅ Completed and saved {analysis_type} analysis.")


async def trigger_all_analyses(pool: asyncpg.Pool, loyalty_program_id: int):
    """
    Orchestrator that fetches data once, then runs all three analysis
    types concurrently.
    """
    print(f"Starting all analyses for loyalty program: {loyalty_program_id}")
    
    # 1. Fetch and preprocess data ONCE
    orders_df = await analysis_crud.get_all_orders_as_df(pool, loyalty_program_id)
    if orders_df.empty:
        print("No orders found. Aborting analysis.")
        return
    preprocessed_df = preprocess_raw_data(orders_df)

    # 2. Run all three analysis pipelines in parallel
    await asyncio.gather(
        _run_one_analysis(pool, preprocessed_df.copy(), loyalty_program_id, "customer"),
        _run_one_analysis(pool, preprocessed_df.copy(), loyalty_program_id, "order")
        # _run_one_analysis(pool, preprocessed_df.copy(), loyalty_program_id, "product"),
    )
    
    print(f"All analyses complete for program: {loyalty_program_id}")