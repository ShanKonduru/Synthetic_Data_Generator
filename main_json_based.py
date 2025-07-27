# main_json_based.py
import json
from datetime import date, datetime # Import date and datetime
import uuid # Import uuid
from utils.utility import Utility

# --- Custom JSON Encoder Class (same as above) ---
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()
        if isinstance(obj, uuid.UUID):
            return str(obj)
        return json.JSONEncoder.default(self, obj)

# --- Example JSON Schemas (unchanged) ---
simple_user_json_schema = {
    "id": "abc-123-def-456",
    "username": "example_user",
    "email": "user@example.com",
    "age": 30,
    "is_active": True, # Keep as boolean for better inference
    "registration_date": "2023-01-15",
    "balance": 123.45
}

order_json_schema = {
    "order_id": "ord-789-xyz",
    "customer_email": "customer@email.com",
    "order_date": "2024-07-27T10:30:00",
    "total_amount": 99.99,
    "items": [
        "Product A",
        "Product B"
    ],
    "shipping_address": {
        "street": "123 Main St",
        "city": "Anytown",
        "postal_code": "12345",
        "country": "USA"
    },
    "payment_status": "pending"
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
    "is_published": True # Keep as boolean
}

address_json = """{
  "street": "123 Main St",
  "city": "Anytown",
  "postal_code": "T1A 0B2",
  "country": "Canada"
}"""

person_json = """{
  "first_name": "Shan",
  "middle_name": "",
  "last_name": "Konduru",
  "age": "50"
}"""


product_json ="""{
  "product_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "name": "Wireless Ergonomic Mouse",
  "price": 49.99,
  "quantity": 150,
  "description": "A comfortable and efficient wireless mouse designed for prolonged use."
}"""

disputecase_json ="""{
  "dispute_id": "f0e9d8c7-b6a5-4321-fedc-ba9876543210",
  "customer_id": "CUST-98765",
  "transaction_amount": 125.75,
  "transaction_currency": "USD",
  "dispute_reason": "Item Not Received",
  "dispute_date": "2024-06-10",
  "status": "Pending Review",
  "is_resolved": false,
  "comments": [
    "Customer claims package was never delivered.",
    "Tracking shows delivered to porch."
  ],
  "evidence_files": [
    {
      "file_name": "delivery_proof.pdf",
      "url": "https://example.com/files/delivery_proof.pdf"
    },
    {
      "file_name": "customer_email.txt",
      "url": "https://example.com/files/customer_email.txt"
    }
  ],
  "contact_email": "customer@example.com",
  "billing_address": {
    "street": "456 Oak Ave",
    "city": "Springfield",
    "postal_code": "90210",
    "country": "USA"
  },
  "last_updated_at": "2025-07-27T10:30:00"
}"""

order_json = """{
  "order_id": "ord-7890-abcd-efgh",
  "customer_email": "jane.doe@example.com",
  "order_date": "2025-07-20T14:15:30",
  "total_amount": 199.99,
  "items": [
    {
      "product_id": "1a2b3c4d-5e6f-7a8b-9c0d-1e2f3a4b5c6d",
      "name": "Laptop Backpack",
      "price": 75.00,
      "quantity": 1,
      "description": "Durable and stylish backpack for laptops up to 15 inches."
    },
    {
      "product_id": "9z8y7x6w-5v4u-3t2s-1r0q-9p8o7n6m5l4k",
      "name": "USB-C Hub",
      "price": 35.50,
      "quantity": 2,
      "description": "Multi-port USB-C adapter with HDMI, USB 3.0, and SD card slots."
    }
  ],
  "shipping_address": {
    "street": "789 Pine Ln",
    "city": "Pleasantville",
    "postal_code": "A1B 2C3",
    "country": "Canada"
  },
  "payment_method": "Credit Card",
  "is_paid": true
}"""

person_json_schema = json.loads(person_json)
address_json_schema = json.loads(address_json)
product_json_schema = json.loads(product_json)
disputecase_json_schema = json.loads(disputecase_json)
order_json_schema = json.loads(order_json)

# --- Main Execution ---
if __name__ == "__main__":
    print("--- Generating Simple User Data from JSON ---")
    address = Utility.GenerateSyntheticTestDataFromJson(address_json_schema)
    print(address)

    pesons = Utility.GenerateSyntheticTestDataFromJson(person_json_schema, count=5)
    for i, peson in enumerate(pesons):
      print(f"\nPerson {i+1}:")
      print(json.dumps(peson.get_data(), indent=2, cls=CustomJSONEncoder))

    users = Utility.GenerateSyntheticTestDataFromJson(
        simple_user_json_schema,
        count=2,
        field_name_age={"min_value": 20, "max_value": 70},
        field_name_is_active={"true_probability": 0.8}
    )
    for i, user_data in enumerate(users):
        print(f"\nUser {i+1}:")
        # Use the custom encoder here
        print(json.dumps(user_data.get_data(), indent=2, cls=CustomJSONEncoder))
    print("-" * 50)

    print("\n--- Generating Order Data from JSON ---")
    orders = Utility.GenerateSyntheticTestDataFromJson(
        order_json_schema,
        count=1,
        field_name_total_amount={"min_value": 50.0, "max_value": 500.0, "decimal_places": 2},
        field_name_items={
            "min_length": 5,
            "max_length": 15
        },
        field_name_shipping_address={
            "field_name_country": {"choices": ["USA", "Canada", "UK", "Australia"]}
        },
        field_name_payment_status={"choices": ["paid", "pending", "failed", "refunded"]}
    )
    for order_data in orders:
        print("\nGenerated Order:")
        # Use the custom encoder here
        print(json.dumps(order_data.get_data(), indent=2, cls=CustomJSONEncoder))
    print("-" * 50)

    print("\n--- Generating Blog Post Data from JSON ---")
    blog_posts = Utility.GenerateSyntheticTestDataFromJson(
        blog_post_json_schema,
        count=3,
        field_name_title={"min_length": 20, "max_length": 60},
        field_name_tags={"choices": ["python", "testing", "devops", "cloud", "security", "ai-ml"]},
        field_name_comments={
            "field_name_user": {"min_length": 5, "max_length": 15},
            "field_name_text": {"min_length": 30, "max_length": 100}
        }
    )
    for i, post_data in enumerate(blog_posts):
        print(f"\nBlog Post {i+1}:")
        # Use the custom encoder here
        print(json.dumps(post_data.get_data(), indent=2, cls=CustomJSONEncoder))
    print("-" * 50)