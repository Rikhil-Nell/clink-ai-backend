import asyncio
import asyncpg
import pandas as pd

import logfire

from app.schemas.core.enums import AnalysisTypeEnum

from app.crud.analysis_crud import analysis_crud
from app.utils.preprocessing import preprocess_raw_data
from app.utils.data_transformer import flatten_order_data_to_dataframe

from app.analysis.customer_analysis import run_customer_analysis
from app.analysis.order_analysis import run_order_analysis
# from app.analysis.product_analysis import run_product_analysis

from app.summarization.customer_kpi_summarization import run_customer_summarization
from app.summarization.order_kpi_summarization import run_order_summarization
# from app.summarization.product_kpi_summarization import run_product_summarization

async def _run_one_analysis( 
    pool: asyncpg.Pool, 
    df: pd.DataFrame, 
    loyalty_program_id: int, 
    analysis_type: AnalysisTypeEnum
):
    """A generic worker that runs one type of analysis."""
    with logfire.span(
        "run_{analysis_type}_analysis",
        analysis_type=analysis_type.name,
        loyalty_program_id=loyalty_program_id,
        row_count=len(df)
    ):
        analysis_map = {
            AnalysisTypeEnum.CUSTOMER: (run_customer_analysis, run_customer_summarization),
            AnalysisTypeEnum.ORDER: (run_order_analysis, run_order_summarization),
        }

        analysis_func, summarization_func = analysis_map[analysis_type]
        analysis_results = analysis_func(df)

        summary_dict = None
        if analysis_type == AnalysisTypeEnum.CUSTOMER:
            kpi_df = analysis_results
            summary_dict = summarization_func(kpi_df)
        elif analysis_type == AnalysisTypeEnum.ORDER:
            invoice_df, cooc_matrix = analysis_results
            summary_dict = summarization_func(invoice_df=invoice_df, cooc_matrix=cooc_matrix)

        if summary_dict:
            await analysis_crud.save_analysis_result(
                pool=pool,
                loyalty_program_id=loyalty_program_id,
                analysis_type=analysis_type.value,
                result_dict=summary_dict
            )
            logfire.info(
                "Analysis completed",
                analysis_type=analysis_type.name,
                loyalty_program_id=loyalty_program_id
            )
        else:
            logfire.warn(
                "Could not generate summary",
                analysis_type=analysis_type.name,
                loyalty_program_id=loyalty_program_id
            )


@logfire.instrument("trigger_all_analyses for {loyalty_program_id}")
async def trigger_all_analyses(pool: asyncpg.Pool, loyalty_program_id: int):
    """
    Orchestrator that fetches data, transforms it, preprocesses, 
    and then runs all analysis types concurrently.
    """
    # 1. Fetch the raw list of nested JSON orders from the database
    raw_orders_list = await analysis_crud.get_all_orders_as_list(pool, loyalty_program_id)
    
    if not raw_orders_list:
        logfire.warn("No orders found, aborting analysis", loyalty_program_id=loyalty_program_id)
        return
    
    logfire.debug("Orders fetched", order_count=len(raw_orders_list))
        
    # 2. Transform the nested JSON into a flat DataFrame
    flat_df = flatten_order_data_to_dataframe(raw_orders_list)

    # 3. Preprocess
    preprocessed_df = preprocess_raw_data(flat_df)

    # 4. Run all analysis pipelines in parallel
    results = await asyncio.gather(
        _run_one_analysis(pool, preprocessed_df.copy(), loyalty_program_id, AnalysisTypeEnum.CUSTOMER),
        _run_one_analysis(pool, preprocessed_df.copy(), loyalty_program_id, AnalysisTypeEnum.ORDER),
        return_exceptions=True
    )
    
    # Log any failures
    for analysis_type, result in zip([AnalysisTypeEnum.CUSTOMER, AnalysisTypeEnum.ORDER], results):
        if isinstance(result, Exception):
            logfire.error("Analysis failed", analysis_type=analysis_type.name, exc_info=result)
    
    logfire.info("All analyses complete", loyalty_program_id=loyalty_program_id)