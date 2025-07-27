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

# --- Main Execution ---
if __name__ == "__main__":
    print("--- Generating Simple User Data from JSON ---")
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