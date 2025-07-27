# main_class_based.py
import json
from datetime import date, datetime
import uuid
from utils.utility import Utility
from src.models import DisputeCase, Order, Product, Address # Ensure Address is imported

# --- Custom JSON Encoder Class (unchanged) ---
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()
        if isinstance(obj, uuid.UUID):
            return str(obj)
        return json.JSONEncoder.default(self, obj)

# --- Define Your Rule Engine Configuration ---
# Keys are dot-separated paths for nested fields.
# Values can contain 'generator' (a callable Faker method or custom function)
# or 'choices' (a list to pick from).
my_generation_rules = {
    # Rules for Address fields (used by DisputeCase and Order)
    "billing_address.street": {"generator": Utility._faker_instance.street_address}, # Direct Faker method
    "billing_address.city": {"generator": Utility._faker_instance.city},
    "billing_address.postal_code": {"generator": Utility._faker_instance.postcode},
    "billing_address.country": {"choices": ["USA", "Canada", "UK", "Australia", "Germany", "France"]},

    "shipping_address.street": {"generator": Utility._faker_instance.street_address},
    "shipping_address.city": {"generator": Utility._faker_instance.city},
    "shipping_address.postal_code": {"generator": Utility._faker_instance.postcode},
    "shipping_address.country": {"choices": ["USA", "Canada", "UK", "Australia", "Japan"]},

    # Other specific rules
    "dispute_reason": {"choices": ["Item Not Received", "Fraudulent Charge", "Product Damaged", "Service Not As Described", "Billing Error"]},
    "status": {"choices": ["Open", "Pending Review", "Closed - Resolved", "Closed - Unresolved", "Escalated"]},
    "contact_email": {"generator": Utility._faker_instance.free_email}, # More specific email
    "last_updated_at": {"generator": Utility._faker_instance.date_time_between, "kwargs": {"start_date": "-2y", "end_date": "now"}},
    "order_date": {"generator": Utility._faker_instance.date_time_this_year, "kwargs": {"before_now": True}},
    "payment_method": {"choices": ["Credit Card", "PayPal", "Bank Transfer", "Crypto", "Invoice"]},
    "total_amount": {"generator": Utility._faker_instance.pyfloat, "kwargs": {"min_value": 50.0, "max_value": 2000.0, "right_digits": 2}},
    "items.name": {"choices": ["Laptop", "Monitor", "Keyboard", "Mouse", "Webcam", "Headphones", "SSD", "RAM"]}, # Rules for list items
    "items.price": {"generator": Utility._faker_instance.pyfloat, "kwargs": {"min_value": 10.0, "max_value": 500.0, "right_digits": 2}},
    "items.quantity": {"generator": Utility._faker_instance.pyint, "kwargs": {"min_value": 1, "max_value": 10}},
}


# --- Main Execution ---
if __name__ == "__main__":
    print("--- Generating DisputeCase Data (Class-based, with Rules) ---")
    dispute_object = DisputeCase()
    dispute_testdata = Utility.GenerateSyntheticTestDataFor(
        dispute_object,
        rules=my_generation_rules # Pass the rules dictionary
    )
    print(f"Generated Dispute Case:\n{json.dumps(dispute_testdata.get_data(), indent=2, cls=CustomJSONEncoder)}")
    print("-" * 50)

    print("\n--- Generating Order Data (Class-based, with Rules) ---")
    order_object = Order()
    order_testdata = Utility.GenerateSyntheticTestDataFor(
        order_object,
        rules=my_generation_rules # Pass the rules dictionary
    )
    print(f"Generated Order Data:\n{json.dumps(order_testdata.get_data(), indent=2, cls=CustomJSONEncoder)}")
    print("-" * 50)

    print("\n--- Generating Product Data (Class-based, with Rules) ---")
    product_object = Product()
    # If Product needs specific rules, add them to my_generation_rules or define a separate rules dict
    product_testdata = Utility.GenerateSyntheticTestDataFor(
        product_object,
        rules=my_generation_rules # Reusing the rules, or could be a specific 'product_rules'
    )
    print(f"Generated Product Data:\n{json.dumps(product_testdata.get_data(), indent=2, cls=CustomJSONEncoder)}")
    print("-" * 50)

    print("\n--- Generating 2 more Dispute Cases (Class-based, with Rules) ---")
    for i in range(2):
        print(f"\nDispute Case {i+1}:")
        dispute_object_2 = DisputeCase()
        data = Utility.GenerateSyntheticTestDataFor(
            dispute_object_2,
            rules=my_generation_rules # Pass the rules dictionary
        )
        print(json.dumps(data.get_data(), indent=2, cls=CustomJSONEncoder))
    print("-" * 50)

    # Example of generating just an Address using rules
    print("\n--- Generating Address Data (Class-based, with Rules) ---")
    address_object = Address()
    address_rules = {
        "street": {"generator": Utility._faker_instance.street_name},
        "city": {"generator": Utility._faker_instance.city},
        "postal_code": {"generator": Utility._faker_instance.postcode},
        "country": {"choices": ["Mexico", "Brazil", "Argentina", "Chile"]},
    }
    address_data = Utility.GenerateSyntheticTestDataFor(
        address_object,
        rules=address_rules
    )
    print(f"Generated Address:\n{json.dumps(address_data.get_data(), indent=2, cls=CustomJSONEncoder)}")
    print("-" * 50)