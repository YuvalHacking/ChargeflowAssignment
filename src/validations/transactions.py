from pydantic import BaseModel, ValidationError, field_validator
from typing import Literal, Optional
import pandas as pd
from utils.logging_config import logger
from typing import List

class PaymentMethod(BaseModel):
    type: Literal['credit_card', 'debit_card', 'wallet']  
    provider: str  

class Transaction(BaseModel):
    transaction_id: str
    order_id: str
    timestamp: str
    amount: float
    currency: str
    status: Literal['completed', 'failed', 'pending']  
    payment_method: List[PaymentMethod] = [] 
    error_code: Optional[str] = None 


    @field_validator('status')
    def validate_status(cls, v: str):
        """
        Validate transaction status to ensure it is one of ['completed', 'failed', 'pending'].

        :param v: The status value to validate.
        :type v: str
        :return: The validated status value.
        :rtype: str
        :raises ValueError: If the status is invalid.
        """
        valid_statuses = ['completed', 'failed', 'pending']
        if v not in valid_statuses:
            logger.error(f"Invalid status: {v}")
            raise ValueError(f"Invalid status: {v}")
        return v

    @field_validator('timestamp')
    def validate_timestamp(cls, v: str):
        """
        Validate that the timestamp is in the correct format (ISO 8601).

        :param v: The timestamp to validate.
        :type v: str
        :return: The validated timestamp.
        :rtype: str
        :raises ValueError: If the timestamp format is invalid.
        """
        try:
            pd.to_datetime(v)
        except ValueError:
            logger.error(f"Invalid timestamp format: {v}")
            raise ValueError(f"Invalid timestamp format: {v}")
        return v

    @field_validator('currency')
    def validate_currency(cls, v):
        """
        Validate that the currency is in the ISO 4217 format (e.g., 'USD', 'EUR').

        :param v: The currency value to validate.
        :type v: str
        :return: The validated currency.
        :rtype: str
        :raises ValueError: If the currency is invalid.
        """
        valid_currencies = ['USD', 'EUR', 'GBP', 'INR', 'AUD', 'CAD']  # Example currencies
        if v not in valid_currencies:
            logger.error(f"Invalid currency: {v}")
            raise ValueError(f"Invalid currency: {v}")
        return v

    # @field_validator('amount')
    # def validate_amount(cls, v: str, values):
    #     """
    #     Validate that the transaction amount matches the order amount.

    #     :param v: The transaction amount to validate.
    #     :type v: float
    #     :param values: A dictionary containing other fields of the model (e.g., order_id).
    #     :type values: dict
    #     :return: The validated amount.
    #     :rtype: float
    #     :raises ValueError: If the transaction amount does not match the order amount.
    #     """
    #     if 'total_amount' in values:
    #         order_amount = values.get('total_amount', 0.0)
    #         if v != order_amount:
    #             logger.error(f"Transaction amount {v} does not match order amount {order_amount}")
    #             raise ValueError(f"Transaction amount {v} does not match order amount {order_amount}")
    #     return v
    
    
def validate_transactions(transactions: pd.DataFrame) -> pd.DataFrame:
    """
    Validate transaction data in a pandas DataFrame.

    :param transactions: DataFrame containing transactions to validate.
    :type transactions: pd.DataFrame
    :return: DataFrame with validated transactions.
    :rtype: pd.DataFrame
    :raises ValidationError: If any validation fails.
    """
    validated_data = []
    
    for _, row in transactions.iterrows():
        try:
            transaction = row.to_dict()  

            validated_transaction = Transaction(**transaction)
            validated_data.append(validated_transaction.dict())  # Append the validated data
        except ValidationError as e:
            logger.error(f"Validation error in transaction {transaction.get('transaction_id')}: {e}")
            raise e

    logger.info(f"Validated {len(validated_data)} transactions successfully.")
    # Convert the validated list of dicts into a DataFrame and return it
    validated_df = pd.DataFrame(validated_data)
    return validated_df
