import pandas as pd

# Helper function to normalize the transaction data
def normalize_transaction_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize the transaction data by converting the timestamp to datetime format
    and rounding the transaction amount to two decimal places.

    :param df: The DataFrame containing transaction data.
    :type df: pd.DataFrame
    :return: The transformed DataFrame with normalized transaction data.
    :rtype: pd.DataFrame
    """
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['amount'] = df['amount'].round(2)
    return df

# Normalize and match chargebacks with transactions
def match_chargebacks_with_transactions(transactions_df: pd.DataFrame, chargebacks_df: pd.DataFrame) -> pd.DataFrame:
    """
    Match chargebacks with the corresponding transactions by merging the chargeback
    and transaction data on the transaction_id field. If a chargeback is present, 
    the amount is added to the transaction data.

    :param transactions_df: The DataFrame containing transaction data.
    :type transactions_df: pd.DataFrame
    :param chargebacks_df: The DataFrame containing chargeback data.
    :type chargebacks_df: pd.DataFrame
    :return: A DataFrame containing merged transaction and chargeback data.
    :rtype: pd.DataFrame
    """
    chargebacks_df['dispute_date'] = pd.to_datetime(chargebacks_df['dispute_date'])
    merged_df = pd.merge(transactions_df, chargebacks_df, on="transaction_id", how="left")
    merged_df['chargeback_amount'] = merged_df['amount_y']
    return merged_df

# Calculate payment success rates
def calculate_payment_success_rate(transactions_df: pd.DataFrame) -> float:
    """
    Calculate the payment success rate by dividing the number of completed transactions
    by the total number of transactions.

    :param transactions_df: The DataFrame containing transaction data.
    :type transactions_df: pd.DataFrame
    :return: The payment success rate.
    :rtype: float
    """
    success_count = len(transactions_df[transactions_df['status_x'] == 'completed'])
    total_count = len(transactions_df)
    return success_count / total_count if total_count > 0 else 0.0

# Key Metrics Calculation
def calculate_business_metrics(transactions_df: pd.DataFrame, chargebacks_df: pd.DataFrame, orders_df: pd.DataFrame) -> dict:
    """
    Calculate key business metrics including daily transaction volume, chargeback rate,
    failed transaction analysis, and payment success rate.

    :param transactions_df: The DataFrame containing transaction data.
    :type transactions_df: pd.DataFrame
    :param chargebacks_df: The DataFrame containing chargeback data.
    :type chargebacks_df: pd.DataFrame
    :param orders_df: The DataFrame containing order data.
    :type orders_df: pd.DataFrame
    :return: A dictionary containing the calculated business metrics.
    :rtype: dict
    """

    # Calculate daily transaction volume and count
    daily_transactions = transactions_df.groupby(transactions_df['timestamp'].dt.date).agg(
        daily_transaction_volume=('amount_x', 'sum'),
        daily_transaction_count=('transaction_id', 'count')
    ).reset_index()

    # Calculate chargeback rates by transaction ID
    chargeback_rates = chargebacks_df.groupby('transaction_id').size().reset_index(name='chargebacks')
    chargeback_rate = chargeback_rates.groupby('transaction_id').agg(chargeback_rate=('chargebacks', 'mean'))

    metrics = {
        "daily_transactions": daily_transactions,
        "chargeback_rate": chargeback_rate,
        "payment_success_rate": calculate_payment_success_rate(transactions_df)
    }
    return metrics
