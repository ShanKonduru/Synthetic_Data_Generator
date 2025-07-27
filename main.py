# utils/synthetic_data_generator.py
import random
import datetime
import uuid
from faker import Faker
from typing import Optional, Any

class SyntheticDataGenerator:
    """
    Core class for generating synthetic test data for various fundamental data types.
    Leverages the Faker library for realistic data generation.
    """

    def __init__(self, locale='en_US'):
        self.fake = Faker(locale)

    def generate_str(self, min_length: int = 1, max_length: int = 20, chars: Optional[str] = None, pattern: Optional[str] = None) -> str:
        length = random.randint(min_length, max_length)
        if pattern:
            generated_string = ""
            for char in pattern:
                if char == '#':
                    generated_string += str(random.randint(0, 9))
                elif char == '@':
                    generated_string += random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
                else:
                    generated_string += char
            return generated_string
        else:
            if chars:
                return ''.join(random.choice(chars) for _ in range(length))
            else:
                return self.fake.pystr(min_chars=min_length, max_chars=length)

    def generate_int(self, min_value: int = 0, max_value: int = 100000) -> int:
        return random.randint(min_value, max_value)

    def generate_float(self, min_value: float = 0.0, max_value: float = 1000.0, decimal_places: int = 2) -> float:
        return round(random.uniform(min_value, max_value), decimal_places)

    def generate_bool(self, true_probability: float = 0.5) -> bool:
        return random.random() < true_probability

    def generate_date(self, start_date: str = '-30y', end_date: str = 'today') -> datetime.date:
        return self.fake.date_between(start_date=start_date, end_date=end_date)

    def generate_datetime(self, start_date: str = '-30y', end_date: str = 'today') -> datetime.datetime:
        return self.fake.date_time_between(start_date=start_date, end_date=end_date)

    def generate_email(self) -> str:
        return self.fake.email()

    def generate_phone_number(self) -> str:
        return self.fake.phone_number()

    def generate_uuid(self) -> uuid.UUID:
        return uuid.uuid4()

    def generate_ip_address(self) -> str:
        return self.fake.ipv4()

    def generate_name(self) -> str:
        return self.fake.name()

    def generate_first_name(self) -> str:
        return self.fake.first_name()

    def generate_last_name(self) -> str:
        return self.fake.last_name()

    def generate_address(self) -> str:
        return self.fake.address()

    def generate_country(self) -> str:
        return self.fake.country()

    def generate_currency_code(self) -> str:
        return self.fake.currency_code()

    def generate_credit_card_number(self) -> str:
        return self.fake.credit_card_number()

    def generate_job(self) -> str:
        return self.fake.job()

    def generate_sentence(self, nb_words: int = 6, variable_nb_words: bool = True) -> str:
        return self.fake.sentence(nb_words=nb_words, variable_nb_words=variable_nb_words)