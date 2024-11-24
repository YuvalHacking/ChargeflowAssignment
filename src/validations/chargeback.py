from pydantic import BaseModel, ValidationError, field_validator
from typing import Literal
import pandas as pd
from utils.logging_config import logger

class Chargeback(BaseModel):
    transaction_id: str
    dispute_date: str
    amount: float
    reason_code: str
    status: Literal['open', 'resolved']
    resolution_date: str


    @field_validator('dispute_date')
    def validate_timestamp(cls, v: str) -> str:
        """
        Validate that the dispute date is in the correct format (ISO 8601).

        :param v: The dispute date to validate.
        :type v: str
        :return: The validated dispute date.
        :rtype: str
        :raises ValueError: If the dispute date format is invalid.
        """
        try:
            pd.to_datetime(v)
        except ValueError:
            logger.error(f"Invalid dispute date format: {v}")
            raise ValueError(f"Invalid dispute date format: {v}")
        return v

    @field_validator('resolution_date')
    def validate_timestamp(cls, v: str) -> str:
        """
        Validate that the resolution date is in the correct format (ISO 8601).

        :param v: The resolution date to validate.
        :type v: str
        :return: The validated resolution date.
        :rtype: str
        :raises ValueError: If the resolution date format is invalid.
        """
        try:
            pd.to_datetime(v)
        except ValueError:
            logger.error(f"Invalid resolution date format: {v}")
            raise ValueError(f"Invalid resolution date format: {v}")
        return v
    
def validate_chargebacks(chargebacks_df: pd.DataFrame) -> pd.DataFrame:
    """
    Validate chargeback data in a pandas DataFrame.

    :param chargebacks_df: DataFrame containing chargeback data.
    :type chargebacks_df: pd.DataFrame
    :return: DataFrame containing validated chargebacks.
    :rtype: pd.DataFrame
    :raises ValidationError: If any validation fails.
    """
    validated_chargebacks = []

    for _, row in chargebacks_df.iterrows():
        try:
            chargeback_data = row.to_dict()

            validated_chargeback = Chargeback(**chargeback_data)
            validated_chargebacks.append(validated_chargeback.dict())  #
        except ValidationError as e:
            logger.error(f"Validation error in chargeback {row.get('chargeback_id')}: {e}")
            raise e

    # Convert the list of validated chargebacks back to a DataFrame
    validated_chargebacks_df = pd.DataFrame(validated_chargebacks)

    logger.info(f"Validated {len(validated_chargebacks_df)} chargebacks successfully.")
    return validated_chargebacks_df
