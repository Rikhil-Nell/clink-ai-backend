from enum import Enum

class AnalysisTypeEnum(str, Enum):
    customer = "customer_summary"
    product = "product_summary"
    order = "order_summary"