import random
import datetime
import uuid
import inspect
from faker import Faker
from typing import Any, List, Dict, Union, Optional, get_origin, get_args # Added get_origin, get_args for better type introspection

# --- Base SyntheticDataGenerator Class ---
class SyntheticDataGenerator:
    # ... (No changes needed in this class from the last version, it's fine) ...
    def __init__(self, locale='en_US'):
        self.fake = Faker(locale)

    def generate_str(self, min_length: int = 1, max_length: int = 20, chars: Optional[str] = None, pattern: Optional[str] = None) -> str:
        # Corrected Faker pystr usage: max_chars is inclusive upper bound
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
                return self.fake.pystr(min_chars=min_length, max_chars=length) # max_chars is actual length or upper bound


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

# --- Wrapper Class for Generated Test Data ---
class GeneratedTestData:
    # ... (This class is fine as is, no changes needed) ...
    def __init__(self, data: Dict[str, Any]):
        self._data = data

    def get_data(self) -> Dict[str, Any]:
        return self._data

    def __str__(self) -> str:
        return str(self._data)

    def __repr__(self) -> str:
        return f"GeneratedTestData({repr(self._data)})"

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def __contains__(self, key: str) -> bool:
        return key in self._data

    def items(self):
        return self._data.items()

    def keys(self):
        return self._data.keys()

    def values(self):
        return self._data.values()


# --- Utility Class for Dynamic Test Data Generation ---

class Utility:
    """
    Utility class to dynamically generate synthetic test data for a given class instance
    based on its type hints.
    """
    _data_generator = SyntheticDataGenerator() # Single instance of our generator

    _type_to_generator_map = {
        str: _data_generator.generate_str,
        int: _data_generator.generate_int,
        float: _data_generator.generate_float,
        bool: _data_generator.generate_bool,
        datetime.date: _data_generator.generate_date,
        datetime.datetime: _data_generator.generate_datetime,
        uuid.UUID: _data_generator.generate_uuid,
    }

    _field_name_to_generator_map = {
        "email": _data_generator.generate_email,
        "phone_number": _data_generator.generate_phone_number,
        "phone": _data_generator.generate_phone_number,
        "name": _data_generator.generate_name,
        "first_name": _data_generator.generate_first_name,
        "last_name": _data_generator.generate_last_name,
        "address": _data_generator.generate_address,
        "country": _data_generator.generate_country,
        "currency": _data_generator.generate_currency_code,
        "job_title": _data_generator.generate_job,
        "description": _data_generator.generate_sentence,
        "comment": _data_generator.generate_sentence,
        "title": _data_generator.generate_sentence,
        "id": _data_generator.generate_uuid,
        "uuid": _data_generator.generate_uuid,
        "ip_address": _data_generator.generate_ip_address,
        "credit_card_number": _data_generator.generate_credit_card_number,
        "card_number": _data_generator.generate_credit_card_number,
        "iban": _data_generator.fake.iban,
        "ssn": _data_generator.fake.ssn,
    }

    @staticmethod
    def _resolve_generator(field_name: str, field_type: Any):
        """
        Resolves the appropriate generator function based on field type and name.
        Prioritizes field name mapping for specific realistic data.
        """
        # 1. Check for specific field name mapping (case-insensitive)
        lower_field_name = field_name.lower()
        if lower_field_name in Utility._field_name_to_generator_map:
            return Utility._field_name_to_generator_map[lower_field_name]

        # Use get_origin and get_args for robust handling of generic types (List, Dict, Union)
        origin = get_origin(field_type)
        args = get_args(field_type)

        # 2. Handle Union types (e.g., Optional[str] is Union[str, NoneType])
        if origin is Union:
            actual_types = [t for t in args if t is not type(None)]
            if actual_types:
                field_type = actual_types[0] # Pick the first actual type
                origin = get_origin(field_type) # Re-evaluate origin for the actual type
                args = get_args(field_type) # Re-evaluate args for the actual type

        # 3. Handle complex types like List, Dict, or other custom classes
        if origin is list:
            inner_type = args[0] if args else Any
            return lambda **kwargs: [Utility._resolve_generator(f"{field_name}_item_{i}", inner_type)(**kwargs)
                                     for i in range(random.randint(1, 3))]
        elif origin is dict:
            key_type = args[0] if args else str
            value_type = args[1] if args else Any
            def generate_dict_field(**kwargs):
                generated_dict = {}
                num_items = random.randint(1, 2)
                for i in range(num_items):
                    key_gen = Utility._resolve_generator(f"{field_name}_key_{i}", key_type)
                    value_gen = Utility._resolve_generator(f"{field_name}_value_{i}", value_type)
                    # Handle cases where _resolve_generator might return a direct value instead of a callable
                    generated_key = key_gen() if callable(key_gen) else key_gen
                    generated_value = value_gen() if callable(value_gen) else value_gen
                    generated_dict[generated_key] = generated_value
                return generated_dict
            return generate_dict_field
        
        # 4. Check for general type mapping
        # If origin is None, it's a basic type like str, int, etc.
        if origin is None and field_type in Utility._type_to_generator_map:
            return Utility._type_to_generator_map[field_type]
        
        # 5. Fallback for unhandled types (e.g., if a custom class is hinted)
        if inspect.isclass(field_type) and field_type.__module__ != 'builtins':
            return lambda **kwargs: Utility.GenerateSyntheticTestDataFor(field_type(), **kwargs).get_data()

        # Fallback to a generic string generator if no specific generator is found
        print(f"Warning: No specific generator found for field '{field_name}' of type '{field_type}'. Defaulting to generic string.")
        return Utility._data_generator.generate_str


    @staticmethod
    def GenerateSyntheticTestDataFor(instance: Any, **kwargs) -> GeneratedTestData:
        """
        Generates synthetic test data for all fields of a given class instance
        based on its type hints and common field name conventions.

        Args:
            instance: An instance of the class for which to generate data.
                      Type hints must be present in the class's __init__ method parameters
                      or as class-level annotated attributes.
            **kwargs: Additional keyword arguments for specific field generation.
                      These should be prefixed with 'field_name_'.
                      Example: field_name_age=(min_value=20, max_value=60)
                               field_name_status=(choices=['active', 'inactive'])

        Returns:
            GeneratedTestData: An object containing the generated data as a dictionary.
        """
        generated_data = {}
        target_class = instance.__class__

        # 1. Get annotations from class-level attributes
        class_annotations = inspect.get_annotations(target_class)

        # 2. Get annotations from __init__ method parameters
        # This is often where the primary data model for an object is defined.
        init_annotations = {}
        if hasattr(target_class, '__init__'):
            init_signature = inspect.signature(target_class.__init__)
            # Exclude 'self' parameter
            for param_name, param in init_signature.parameters.items():
                if param_name != 'self' and param.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD:
                    if param.annotation is not inspect.Parameter.empty:
                        init_annotations[param_name] = param.annotation
        
        # Combine annotations, with __init__ parameters taking precedence
        # (as they represent the constructor's expected fields)
        all_annotations = {**class_annotations, **init_annotations}

        for field_name, field_type in all_annotations.items():
            # Check if specific kwargs are provided for this field
            field_kwargs_key = f"field_name_{field_name}"
            specific_kwargs = kwargs.get(field_kwargs_key, {})

            # If 'choices' are provided in specific_kwargs, use them directly
            if "choices" in specific_kwargs:
                if not isinstance(specific_kwargs["choices"], (list, tuple)):
                    raise TypeError(f"Choices for field '{field_name}' must be a list or tuple.")
                generated_data[field_name] = random.choice(specific_kwargs["choices"])
                continue # Move to the next field

            # Resolve the generator function for the field
            generator_func = Utility._resolve_generator(field_name, field_type)

            try:
                # Determine how to call the generator_func based on its signature and kwargs
                if callable(generator_func):
                    # Inspect the function signature to see what arguments it accepts
                    func_signature = inspect.signature(generator_func)
                    
                    # Check if it accepts arbitrary keyword arguments (like **kwargs)
                    accepts_kwargs = any(p.kind == inspect.Parameter.VAR_KEYWORD for p in func_signature.parameters.values())

                    if accepts_kwargs:
                        generated_data[field_name] = generator_func(**specific_kwargs)
                    else:
                        # Filter specific_kwargs to only include parameters the function accepts
                        accepted_params = {p.name for p in func_signature.parameters.values() if p.kind != inspect.Parameter.VAR_KEYWORD}
                        filtered_kwargs = {k: v for k, v in specific_kwargs.items() if k in accepted_params}
                        
                        if len(filtered_kwargs) < len(specific_kwargs):
                            unaccepted = set(specific_kwargs.keys()) - set(filtered_kwargs.keys())
                            print(f"Warning: Unaccepted kwargs {list(unaccepted)} for field '{field_name}' in '{generator_func.__name__}'. Ignoring.")
                        
                        generated_data[field_name] = generator_func(**filtered_kwargs)
                else:
                    # If _resolve_generator returns a direct value (should ideally not happen if a function is expected)
                    generated_data[field_name] = generator_func

            except TypeError as e:
                # If a TypeError occurs, it often means the args passed were wrong for the function.
                # Try calling without any kwargs as a fallback.
                print(f"Error generating data for '{field_name}' with args {specific_kwargs}: {e}. Retrying without specific kwargs.")
                try:
                    if callable(generator_func):
                        generated_data[field_name] = generator_func()
                    else: # If it's not callable, just assign the value directly
                        generated_data[field_name] = generator_func
                except Exception as inner_e:
                    print(f"Fallback without kwargs failed for '{field_name}': {inner_e}")
                    generated_data[field_name] = None # Final fallback if all else fails
            except Exception as e:
                print(f"Unexpected error generating data for '{field_name}': {e}")
                generated_data[field_name] = None # Final fallback

        return GeneratedTestData(generated_data)