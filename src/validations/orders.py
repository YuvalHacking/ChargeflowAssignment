from pydantic import BaseModel, ValidationError, field_validator
from typing import Literal, List
import pandas as pd
from utils.logging_config import logger

class Item(BaseModel):
    product_id: str
    quantity: int
    unit_price: float

class Order(BaseModel):
    order_id: str
    customer_id: str
    timestamp: str
    total_amount: float
    currency: str
    items: List[Item] = []
    payment_status: Literal['paid', 'failed', 'refunded']

    @field_validator('payment_status')
    def validate_payment_status(cls, v):
        valid_statuses = ['paid', 'failed', 'refunded']
        if v not in valid_statuses:
            logger.error(f"Invalid payment status: {v}")
            raise ValueError(f"Invalid payment status: {v}")
        return v

    @field_validator('timestamp')
    def validate_timestamp(cls, v: str) -> str:
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
    def validate_currency(cls, v: str) -> str:
        """
        Validate that the currency is one of the accepted values.

        :param v: The currency to validate.
        :type v: str
        :return: The validated currency.
        :rtype: str
        :raises ValueError: If the currency is invalid.
        """
        valid_currencies = ['USD', 'EUR', 'GBP', 'INR', 'AUD', 'CAD']
        if v not in valid_currencies:
            logger.error(f"Invalid currency: {v}")
            raise ValueError(f"Invalid currency: {v}")
        return v

def validate_orders(orders_df: pd.DataFrame) -> pd.DataFrame:
    """
    Validate the orders DataFrame.

    :param orders_df: The DataFrame containing orders to validate.
    :type orders_df: pd.DataFrame
    :return: The validated orders DataFrame.
    :rtype: pd.DataFrame
    """
    validated_orders = []

    for _, row in orders_df.iterrows():
        try:
            order_data = row.to_dict()
            validated_order = Order(**order_data)
            validated_orders.append(validated_order.dict())
        except ValidationError as e:
            logger.error(f"Validation error in order {row.get('order_id')}: {e}")
            raise e

    logger.info(f"Validated {len(validated_orders)} orders successfully.")
    validated_orders_df = pd.DataFrame(validated_orders)
    return validated_orders_df