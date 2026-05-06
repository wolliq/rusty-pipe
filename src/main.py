"""Sample application demonstrating Polars and Loguru."""

import random
from datetime import date, timedelta

import polars as pl
from loguru import logger


def generate_data(num_rows: int = 1000) -> pl.DataFrame:
    """Generate sample sales data."""
    logger.info(f"Generating sample data with {num_rows} rows.")
    categories = ["Electronics", "Clothing", "Food", "Books", "Toys"]
    products = [f"Product_{i}" for i in range(1, 21)]
    start_date = date(2023, 1, 1)

    data = {
        "date": [start_date + timedelta(days=random.randint(0, 365)) for _ in range(num_rows)],
        "product": [random.choice(products) for _ in range(num_rows)],
        "category": [random.choice(categories) for _ in range(num_rows)],
        "amount": [round(random.uniform(10.0, 500.0), 2) for _ in range(num_rows)],
        "quantity": [random.randint(1, 10) for _ in range(num_rows)],
    }

    df = pl.DataFrame(data)
    logger.debug(f"Data generation complete. Shape: {df.shape}")
    return df


def calculate_aggregations(df: pl.DataFrame) -> pl.DataFrame:
    """Calculate total sales amount and quantity per category."""
    logger.info("Calculating aggregations per category.")

    # Calculate total revenue for each row
    df = df.with_columns((pl.col("amount") * pl.col("quantity")).alias("total_revenue"))

    # Group by category and aggregate
    aggregated = (
        df.group_by("category")
        .agg(
            pl.col("quantity").sum().alias("total_items_sold"),
            pl.col("total_revenue").sum().alias("total_revenue"),
            pl.col("amount").mean().alias("average_price"),
        )
        .sort("total_revenue", descending=True)
    )

    logger.success("Aggregation complete.")
    return aggregated


def main() -> None:
    """Execute the main data processing pipeline."""
    logger.info("Starting the Polars aggregation pipeline.")

    try:
        df = generate_data(5000)

        logger.info("Preview of generated data:")
        print(df.head())

        result = calculate_aggregations(df)

        logger.info("Aggregation Results:")
        print(result)

        logger.success("Pipeline executed successfully.")

    except Exception as e:
        logger.exception(f"An error occurred during pipeline execution: {e}")


if __name__ == "__main__":
    main()
