from app.agents.registry import get_agent

agent = get_agent("WINBACK", "MISS_YOU")

prompt = """
Customer Facing Analysis

{
  "customer_segments": {
    "new_customers": {
      "count": 7,
      "percentage": 46.67,
      "avg_first_order_value": 361.43
    },
    "total_customers": 15,
    "active_customers": {
      "count": 2,
      "avg_clv": 15034.5,
      "avg_orders": 11.5,
      "percentage": 13.33
    },
    "dormant_customers": {
      "count": 6,
      "percentage": 40,
      "avg_clv_before_dormancy": 275.5
    }
  },
  "financial_summary": {
    "overall_aov": 770.82,
    "total_revenue": 39312,
    "overall_avg_clv": 2620.8,
    "estimated_total_profit": 9828
  },
  "analysis_timestamp": "2025-08-29T00:34:26.424050",
  "additional_insights": {
    "high_value_customers": {
      "count": 3,
      "avg_clv": 11363,
      "threshold": 1924
    },
    "order_frequency_insights": {
      "repeat_customers": 8,
      "single_order_customers": 7,
      "high_frequency_customers": 3
    }
  },
  "coupon_strategy_insights": {
    "miss_you": {
      "suggestion": "A win-back offer should be compelling relative to these averages.",
      "target_customer_count": 6,
      "avg_spend_of_dormant_customers": 231.33,
      "last_order_recency_distribution": {
        "25%": 11,
        "50%": 22,
        "75%": 66.5,
        "max": 2865,
        "min": 0,
        "std": 998.09,
        "mean": 407.4,
        "count": 15
      }
    },
    "stamp_card": {
      "suggestion": "Most active customers place between 8 and 14 orders. Recommend 5 or 7 stamp card.",
      "target_customer_count": 2,
      "order_frequency_distribution": {
        "25%": 8.75,
        "50%": 11.5,
        "75%": 14.25,
        "max": 17,
        "min": 6,
        "std": 7.78,
        "mean": 11.5,
        "count": 2
      }
    },
    "joining_bonus": {
      "suggestion": "Offer joining bonuses cautiously to protect margins.",
      "avg_first_order_value": 361.43,
      "target_customer_count": 7
    }
  }
}


Order Facing analysis

{
  "analysis_config": {
    "peak_hours_threshold": 0.075,
    "high_value_percentile": 0.8
  },
  "invoice_analysis": {
    "total_orders": 51,
    "total_revenue": 20900,
    "total_items_sold": 230,
    "high_value_orders": {
      "count": 51,
      "threshold": 220,
      "percentage": 100
    },
    "temporal_patterns": {
      "peak_days": [
        "Friday",
        "Tuesday",
        "Wednesday"
      ],
      "hour_analysis": {
        "peak_hours": [
          10,
          12
        ],
        "hourly_distribution": {
          "10": 43,
          "12": 5,
          "17": 2,
          "18": 1
        }
      },
      "day_of_week_distribution": {
        "Friday": 31,
        "Tuesday": 9,
        "Thursday": 5,
        "Wednesday": 6
      }
    },
    "average_order_value": 409.8,
    "basket_size_analysis": {
      "max_items": 2,
      "min_items": 2,
      "avg_unique_items": 2,
      "most_common_basket_size": 2
    },
    "average_items_per_order": 4.51,
    "order_value_distribution": {
      "25%": 220,
      "50%": 220,
      "75%": 220,
      "max": 6600,
      "min": 220,
      "std": 997.57,
      "mean": 409.8
    }
  },
  "business_insights": {
    "inventory_insights": [
      {
        "action": "Ensure availability of items that appear in high-value orders",
        "description": "Orders above $220.00 represent high-value customers",
        "insight_type": "high_value_correlation"
      },
      {
        "action": "Focus on items that appear in the strongest co-occurrence pairs to drive basket size",
        "description": "Average order value is $409.80",
        "insight_type": "basket_optimization"
      }
    ],
    "bundle_opportunities": [],
    "cross_sell_recommendations": []
  },
  "analysis_timestamp": "2025-08-29T00:34:26.525225",
  "cooccurrence_analysis": {
    "analysis_scope": "Top 3 most popular items",
    "matrix_summary": {
      "total_possible_pairs": 3,
      "pairs_with_cooccurrence": 0
    },
    "items_in_matrix": 3,
    "strongest_cooccurrences": []
  }
}"""

result = agent.run_sync(user_prompt=prompt)

from pprint import pprint

pprint(result.output.model_dump())