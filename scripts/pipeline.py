from src.extraction import extract_transactions, extract_chargebacks, extract_orders
from src.clean import clean_dataframe
from src.validations.orders import validate_orders
from src.validations.transactions import validate_transactions
from src.validations.orders import validate_orders
from src.validations.chargeback import validate_chargebacks
from src.transformation import normalize_transaction_data, match_chargebacks_with_transactions, calculate_business_metrics

from pydantic import ValidationError
from utils.logging_config import logger


def main():
    logger.info("Starting the data pipeline")

    try:
        # Step 1: Extract Data
        logger.info("Extracting order data")
        orders = extract_orders('data/orders.json')

        logger.info("Extracting transaction data")
        transactions = extract_transactions('data/transactions.json')

        logger.info("Extracting chargeback data")
        chargebacks = extract_chargebacks('data/chargebacks.csv')

        # Step 2: Clean Data
        orders = clean_dataframe(orders)
        transactions = clean_dataframe(transactions)
        chargebacks = clean_dataframe(chargebacks)

        # Step 3: Validate Data
        logger.info("Validating order data")
        try:
            orders = validate_orders(orders)
        except ValidationError as e:
            logger.error(f"Order validation failed: {e}")
            return
        
        logger.info("Validating transaction data")
        try:
            transactions = validate_transactions(transactions)
        except ValidationError as e:
            logger.error(f"Transaction validation failed: {e}")
            return

        logger.info("Validating chargeback data")
        try:
            chargebacks = validate_chargebacks(chargebacks)
        except ValidationError as e:
            logger.error(f"Chargeback validation failed: {e}")
            return

        # Step 4: Transform Data
        logger.info("Transforming data")
        transactions = normalize_transaction_data(transactions)
        merged = match_chargebacks_with_transactions(transactions, chargebacks)
        metrics = calculate_business_metrics(merged, chargebacks, orders)
        logger.info("Data pipeline completed successfully")

        # Step 5: Output for analysis
        print("Daily Transaction Metrics:")
        print(metrics['daily_transactions'])

        print("\nChargeback Rate by Transaction:")
        print(metrics['chargeback_rate'])

        print("\nPayment Success Rate:")
        print(metrics['payment_success_rate'])

    except Exception as e:
        logger.error(f"Error in data pipeline: {e}")
        raise

if __name__ == "__main__":
    main()
