import polars as pl
from src.main import calculate_aggregations

def test_calculate_aggregations() -> None:
    """Test the calculate_aggregations function."""
    data = {
        "category": ["A", "A", "B", "B"],
        "amount": [10.0, 20.0, 30.0, 40.0],
        "quantity": [2, 1, 1, 3],
    }
    df = pl.DataFrame(data)
    
    result = calculate_aggregations(df)
    
    assert len(result) == 2
    assert "category" in result.columns
    assert "total_items_sold" in result.columns
    assert "total_revenue" in result.columns
    assert "average_price" in result.columns
    
    # Check category A
    a_row = result.filter(pl.col("category") == "A")
    assert a_row["total_items_sold"][0] == 3
    assert a_row["total_revenue"][0] == 40.0
    assert a_row["average_price"][0] == 15.0
    
    # Check category B
    b_row = result.filter(pl.col("category") == "B")
    assert b_row["total_items_sold"][0] == 4
    assert b_row["total_revenue"][0] == 150.0
    assert b_row["average_price"][0] == 35.0
