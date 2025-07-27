# main_json_based.py
import json
from datetime import date, datetime
import uuid
from utils.utility import Utility
from faker import Faker # Import Faker here for rules

# --- Custom JSON Encoder Class (unchanged) ---
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()
        if isinstance(obj, uuid.UUID):
            return str(obj)
        return json.JSONEncoder.default(self, obj)

# --- Define Your Rule Engine Configuration for JSON generation ---
# Note: When using JSON, field paths in rules must match the keys in your JSON schema.
# Also, if you use a direct Faker generator, make sure Faker is imported.
json_generation_rules = {
    "username": {"generator": Utility._faker_instance.user_name},
    "email": {"generator": Utility._faker_instance.email},
    "age": {"generator": Utility._faker_instance.pyint, "kwargs": {"min_value": 18, "max_value": 90}},
    "is_active": {"choices": [True, False]},
    "registration_date": {"generator": Utility._faker_instance.date_this_century, "kwargs": {"before_today": True}},
    "balance": {"generator": Utility._faker_instance.pyfloat, "kwargs": {"min_value": 0.0, "max_value": 10000.0, "right_digits": 2}},

    "shipping_address.street": {"generator": Utility._faker_instance.street_address},
    "shipping_address.city": {"generator": Utility._faker_instance.city},
    "shipping_address.postal_code": {"generator": Utility._faker_instance.postcode},
    "shipping_address.country": {"choices": ["USA", "Canada", "Mexico"]},

    "items.name": {"choices": ["Book", "E-reader", "Headphones", "Charger", "Stylus"]},
    "items.price": {"generator": Utility._faker_instance.pyfloat, "kwargs": {"min_value": 10.0, "max_value": 300.0, "right_digits": 2}},

    "comments.user": {"generator": Utility._faker_instance.first_name},
    "comments.text": {"generator": Utility._faker_instance.paragraph, "kwargs": {"nb_sentences": 2}},
    "comments.timestamp": {"generator": Utility._faker_instance.date_time_this_year},
    "post_id": {"generator": Utility._faker_instance.uuid4},
    "title": {"generator": Utility._faker_instance.sentence, "kwargs": {"nb_words": 10, "variable_nb_words": True}},
    "author": {"generator": Utility._faker_instance.name},
    "publish_date": {"generator": Utility._faker_instance.date_this_decade},
    "content": {"generator": Utility._faker_instance.text},
    "tags": {"choices": ["AI", "Tech", "Science", "History", "Art", "Travel", "Food"]},
    "is_published": {"choices": [True, False]},
}

# --- Your JSON strings --- (Unchanged, converted to dicts below)
address_json_string = """{ "street": "123 Main St", "city": "Anytown", "postal_code": "T1A 0B2", "country": "Canada" }"""
product_json_string ="""{ "product_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef", "name": "Wireless Ergonomic Mouse", "price": 49.99, "quantity": 150, "description": "A comfortable and efficient wireless mouse designed for prolonged use." }"""
disputecase_json_string ="""{ "dispute_id": "f0e9d8c7-b6a5-4321-fedc-ba9876543210", "customer_id": "CUST-98765", "transaction_amount": 125.75, "transaction_currency": "USD", "dispute_reason": "Item Not Received", "dispute_date": "2024-06-10", "status": "Pending Review", "is_resolved": false, "comments": [ "Customer claims package was never delivered.", "Tracking shows delivered to porch." ], "evidence_files": [ { "file_name": "delivery_proof.pdf", "url": "https://example.com/files/delivery_proof.pdf" }, { "file_name": "customer_email.txt", "url": "https://example.com/files/customer_email.txt" } ], "contact_email": "customer@example.com", "billing_address": { "street": "456 Oak Ave", "city": "Springfield", "postal_code": "90210", "country": "USA" }, "last_updated_at": "2025-07-27T10:30:00" }"""
order_json_string = """{ "order_id": "ord-7890-abcd-efgh", "customer_email": "jane.doe@example.com", "order_date": "2025-07-20T14:15:30", "total_amount": 199.99, "items": [ { "product_id": "1a2b3c4d-5e6f-7a8b-9c0d-1e2f3a4b5c6d", "name": "Laptop Backpack", "price": 75.00, "quantity": 1, "description": "Durable and stylish backpack for laptops up to 15 inches." }, { "product_id": "9z8y7x6w-5v4u-3t2s-1r0q-9p8o7n6m5l4k", "name": "USB-C Hub", "price": 35.50, "quantity": 2, "description": "Multi-port USB-C adapter with HDMI, USB 3.0, and SD card slots." } ], "shipping_address": { "street": "789 Pine Ln", "city": "Pleasantville", "postal_code": "A1B 2C3", "country": "Canada" }, "payment_method": "Credit Card", "is_paid": true }"""

# --- Convert JSON strings to Python dictionaries (schemas) ---
address_json_schema = json.loads(address_json_string)
product_json_schema = json.loads(product_json_string)
disputecase_json_schema = json.loads(disputecase_json_string)
order_json_schema = json.loads(order_json_string)

# You can still define simple schemas as dictionaries directly
simple_user_json_schema = {
    "id": "abc-123-def-456",
    "username": "example_user",
    "email": "user@example.com",
    "age": 30,
    "is_active": True,
    "registration_date": "2023-01-15",
    "balance": 123.45
}

blog_post_json_schema = {
    "post_id": "post-uuid-123",
    "title": "My Awesome Blog Post",
    "author": "Jane Doe",
    "publish_date": "2024-07-27",
    "content": "This is the content of the blog post.",
    "tags": ["programming", "ai", "data"],
    "comments": [
        {
            "comment_id": "com-1",
            "user": "Alice",
            "text": "Great post!",
            "timestamp": "2024-07-27T11:00:00"
        },
        {
            "comment_id": "com-2",
            "user": "Bob",
            "text": "Very insightful.",
            "timestamp": "2024-07-27T11:05:00"
        }
    ],
    "is_published": True
}

# --- Main Execution ---
if __name__ == "__main__":
    print("--- Generating Simple User Data from JSON String (with Rules) ---")
    users = Utility.GenerateSyntheticTestDataFromJson(
        simple_user_json_schema,
        count=2,
        rules=json_generation_rules # Pass the rules dictionary
    )
    for i, user_data in enumerate(users):
        print(f"\nUser {i+1}:")
        print(json.dumps(user_data.get_data(), indent=2, cls=CustomJSONEncoder))
    print("-" * 50)

    print("\n--- Generating Order Data from JSON String (with Rules) ---")
    orders = Utility.GenerateSyntheticTestDataFromJson(
        order_json_schema,
        count=1,
        rules=json_generation_rules # Pass the rules dictionary
    )
    for order_data in orders:
        print("\nGenerated Order:")
        print(json.dumps(order_data.get_data(), indent=2, cls=CustomJSONEncoder))
    print("-" * 50)

    print("\n--- Generating Blog Post Data from JSON String (with Rules) ---")
    blog_posts = Utility.GenerateSyntheticTestDataFromJson(
        blog_post_json_schema,
        count=3,
        rules=json_generation_rules # Pass the rules dictionary
    )
    for i, post_data in enumerate(blog_posts):
        print(f"\nBlog Post {i+1}:")
        print(json.dumps(post_data.get_data(), indent=2, cls=CustomJSONEncoder))
    print("-" * 50)

    print("\n--- Generating Address Data from JSON String (with Rules) ---")
    addresses = Utility.GenerateSyntheticTestDataFromJson(
        address_json_schema,
        count=1,
        rules=json_generation_rules # Pass the rules dictionary
    )
    for address_data in addresses:
        print("\nGenerated Address:")
        print(json.dumps(address_data.get_data(), indent=2, cls=CustomJSONEncoder))
    print("-" * 50)

    print("\n--- Generating Product Data from JSON String (with Rules) ---")
    products = Utility.GenerateSyntheticTestDataFromJson(
        product_json_schema,
        count=1,
        rules=json_generation_rules # Pass the rules dictionary
    )
    for product_data in products:
        print("\nGenerated Product:")
        print(json.dumps(product_data.get_data(), indent=2, cls=CustomJSONEncoder))
    print("-" * 50)