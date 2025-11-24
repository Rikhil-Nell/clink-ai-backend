from typing import Dict, Any

def separate_forecast_from_offers(data: Dict[str, Any]) -> tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Separates forecast data from offer data.
    
    Args:
        data: Full model dump including forecast
        
    Returns:
        (forecast_data, offers_data) tuple
    """
    # Make a copy to avoid mutating the original
    offers_data = data.copy()
    
    # Extract and remove forecast
    forecast_data = offers_data.pop('forecast', {})
    
    if not forecast_data:
        # If no forecast was generated (shouldn't happen, but defensive)
        forecast_data = {
            "target": 0,
            "budget": 0,
            "predicted_redemptions": 0,
            "roi": "0x"
        }
        print("⚠️  Warning: No forecast data found in model output")
    
    return forecast_data, offers_data