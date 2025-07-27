# src/models.py
import datetime
import uuid
from typing import Optional, List, Dict

# Note: These models do NOT import anything from 'utils' to avoid circular dependencies.
# The Utility class in 'utils' will import and work with these models when needed.

class Address:
    """Example class for an Address with type hints."""
    def __init__(self, street: Optional[str] = None, city: Optional[str] = None,
                 postal_code: Optional[str] = None, country: Optional[str] = None):
        self.street = street
        self.city = city
        self.postal_code = postal_code
        self.country = country

class Product:
    """Example class for a Product with type hints."""
    def __init__(self, product_id: Optional[uuid.UUID] = None, name: Optional[str] = None,
                 price: Optional[float] = None, quantity: Optional[int] = None,
                 description: Optional[str] = None):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity
        self.description = description

class DisputeCase:
    """Example class for a DisputeCase with type hints, including nested classes and lists."""
    def __init__(self,
                 dispute_id: Optional[uuid.UUID] = None,
                 customer_id: Optional[str] = None,
                 transaction_amount: Optional[float] = None,
                 transaction_currency: Optional[str] = None,
                 dispute_reason: Optional[str] = None,
                 dispute_date: Optional[datetime.date] = None,
                 status: Optional[str] = None,
                 is_resolved: Optional[bool] = None,
                 comments: Optional[List[str]] = None,
                 evidence_files: Optional[List[Dict[str, str]]] = None,
                 contact_email: Optional[str] = None,
                 billing_address: Optional[Address] = None,
                 last_updated_at: Optional[datetime.datetime] = None
                ):
        self.dispute_id = dispute_id
        self.customer_id = customer_id
        self.transaction_amount = transaction_amount
        self.transaction_currency = transaction_currency
        self.dispute_reason = dispute_reason
        self.dispute_date = dispute_date
        self.status = status
        self.is_resolved = is_resolved
        self.comments = comments
        self.evidence_files = evidence_files
        self.contact_email = contact_email
        self.billing_address = billing_address
        self.last_updated_at = last_updated_at

class Order:
    """Example class for an Order with type hints, including lists of custom objects."""
    def __init__(self,
                 order_id: Optional[uuid.UUID] = None,
                 customer_email: Optional[str] = None,
                 order_date: Optional[datetime.datetime] = None,
                 total_amount: Optional[float] = None,
                 items: Optional[List[Product]] = None,
                 shipping_address: Optional[Address] = None,
                 payment_method: Optional[str] = None,
                 is_paid: Optional[bool] = None
                ):
        self.order_id = order_id
        self.customer_email = customer_email
        self.order_date = order_date
        self.total_amount = total_amount
        self.items = items
        self.shipping_address = shipping_address
        self.payment_method = payment_method
        self.is_paid = is_paid