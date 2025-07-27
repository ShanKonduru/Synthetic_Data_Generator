# main_class_based.py
import json
from datetime import date, datetime
import uuid
from utils.utility import Utility
from src.models import DisputeCase, Order, Product # Import your model classes from 'src'

# --- Custom JSON Encoder Class ---
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (date, datetime)):
            # Ensure proper string formatting for dates and datetimes
            # For datetimes, include milliseconds and Z for UTC, or offset if applicable
            return obj.isoformat()
        if isinstance(obj, uuid.UUID):
            return str(obj)
        return json.JSONEncoder.default(self, obj)

# --- Main Execution ---
if __name__ == "__main__":
    print("--- Generating DisputeCase Data (Class-based) ---")
    dispute_object = DisputeCase()
    dispute_testdata = Utility.GenerateSyntheticTestDataFor(
        dispute_object,
        field_name_transaction_amount={"min_value": 10.0, "max_value": 500.0, "decimal_places": 2},
        field_name_dispute_reason={"choices": ["Item Not Received", "Fraudulent Charge", "Product Damaged", "Service Not As Described"]},
        field_name_status={"choices": ["Open", "Pending Review", "Closed - Resolved", "Closed - Unresolved"]},
        field_name_billing_address={
            "field_name_country": {"choices": ["USA", "Canada", "Mexico", "Brazil"]}
        },
        # FIX: Explicitly define date/datetime range for 'last_updated_at'
        field_name_last_updated_at={
            "start_date": "-5y", # E.g., 5 years ago
            "end_date": "now"   # Use "now" for current timestamp. Faker interprets this correctly.
                                # Or use a specific date string like "2025-07-27"
        }
    )
    print(f"Generated Dispute Case:\n{json.dumps(dispute_testdata.get_data(), indent=2, cls=CustomJSONEncoder)}")
    print(f"\nAccessing specific data: Dispute ID = {dispute_testdata['dispute_id']}")
    print(f"Accessing nested data: Billing Address Country = {dispute_testdata['billing_address']['country']}")
    print("-" * 50)

    print("\n--- Generating Order Data (Class-based) ---")
    order_object = Order()
    order_testdata = Utility.GenerateSyntheticTestDataFor(
        order_object,
        field_name_payment_method={"choices": ["Credit Card", "PayPal", "Bank Transfer", "Crypto"]},
        field_name_items={
            "field_name_price": {"min_value": 5.0, "max_value": 50.0, "decimal_places": 2},
            "field_name_quantity": {"min_value": 1, "max_value": 5}
        },
        # FIX: Explicitly define date/datetime range for 'order_date'
        field_name_order_date={
            "start_date": "-1y", # E.g., 1 year ago
            "end_date": "now"
        }
    )
    print(f"Generated Order Data:\n{json.dumps(order_testdata.get_data(), indent=2, cls=CustomJSONEncoder)}")
    print("-" * 50)

    print("\n--- Generating Product Data (Class-based) ---")
    product_object = Product()
    product_testdata = Utility.GenerateSyntheticTestDataFor(
        product_object,
        field_name_price={"min_value": 1.99, "max_value": 999.99}
    )
    print(f"Generated Product Data:\n{json.dumps(product_testdata.get_data(), indent=2, cls=CustomJSONEncoder)}")
    print("-" * 50)

    print("\n--- Generating 2 more Dispute Cases (Class-based) ---")
    for i in range(2):
        print(f"\nDispute Case {i+1}:")
        dispute_object_2 = DisputeCase()
        data = Utility.GenerateSyntheticTestDataFor(
            dispute_object_2,
            field_name_transaction_currency={"choices": ["USD", "EUR", "CAD"]},
            field_name_dispute_reason={"choices": ["Delivery Issue", "Wrong Item"]},
            # FIX: Explicitly define date/datetime range for 'last_updated_at' here too
            field_name_last_updated_at={
                "start_date": "-6m", # E.g., 6 months ago
                "end_date": "now"
            }
        )
        print(json.dumps(data.get_data(), indent=2, cls=CustomJSONEncoder))