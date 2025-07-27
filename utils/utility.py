# utils/utility.py
import random
import datetime
import uuid
import inspect
from typing import Any, List, Dict, Union, Optional, get_origin, get_args

from faker import Faker # Make sure Faker is imported directly here too
from utils.synthetic_data_generator import SyntheticDataGenerator
from utils.generated_test_data import GeneratedTestData

class Utility:
    _data_generator = SyntheticDataGenerator()
    _faker_instance = Faker('en_US') # Direct Faker instance for specific methods

    _type_to_generator_map = {
        str: _data_generator.generate_str,
        int: _data_generator.generate_int,
        float: _data_generator.generate_float,
        bool: _data_generator.generate_bool,
        datetime.date: _data_generator.generate_date,
        datetime.datetime: _data_generator.generate_datetime,
        uuid.UUID: _data_generator.generate_uuid,
    }

    # Enhanced _field_name_to_generator_map with more specific Faker methods
    _field_name_to_generator_map = {
        "email": _data_generator.generate_email,
        "phone_number": _data_generator.generate_phone_number,
        "phone": _data_generator.generate_phone_number,
        "name": _data_generator.generate_name,
        "first_name": _data_generator.generate_first_name,
        "last_name": _data_generator.generate_last_name,
        "address": _data_generator.generate_address, # This is a fallback if no nested address rules
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
        "iban": _faker_instance.iban, # Direct Faker usage
        "ssn": _faker_instance.ssn,   # Direct Faker usage
        "is_active": _data_generator.generate_bool,
        "is_published": _data_generator.generate_bool,
        "is_resolved": _data_generator.generate_bool,
        "is_paid": _data_generator.generate_bool,
        # Specific address fields
        "street": _faker_instance.street_address,
        "city": _faker_instance.city,
        "postal_code": _faker_instance.postcode,
    }

    @staticmethod
    def _resolve_generator(field_name: str, field_type: Any, path: List[str], rules: Dict[str, Any]):
        # Check for specific rules first using the full path
        full_path = ".".join(path + [field_name]) if path else field_name
        if full_path in rules and "generator" in rules[full_path]:
            # If a custom generator is specified in rules, use it
            return rules[full_path]["generator"]
        elif full_path in rules and "choices" in rules[full_path]:
            # If choices are specified, return a lambda that picks from choices
            return lambda: random.choice(rules[full_path]["choices"])


        lower_field_name = field_name.lower()
        if lower_field_name in Utility._field_name_to_generator_map:
            return Utility._field_name_to_generator_map[lower_field_name]

        origin = get_origin(field_type)
        args = get_args(field_type)

        if origin is Union:
            actual_types = [t for t in args if t is not type(None)]
            if actual_types:
                field_type = actual_types[0]
                origin = get_origin(field_type)
                args = get_args(field_type)

        if origin is list:
            inner_type = args[0] if args else Any
            def generate_list_field(**kwargs):
                generated_list = []
                num_items = random.randint(1, 3)
                for i in range(num_items):
                    # Pass the current path for nested rules
                    item_generator = Utility._resolve_generator(f"{field_name}_item_{i}", inner_type, path + [field_name], rules)
                    generated_list.append(Utility._call_generator_with_kwargs(item_generator, kwargs, f"{field_name}_item_{i}"))
                return generated_list
            return generate_list_field
        elif origin is dict:
            key_type = args[0] if args else str
            value_type = args[1] if args else Any
            def generate_dict_field(**kwargs):
                generated_dict = {}
                num_items = random.randint(1, 2)
                for i in range(num_items):
                    # Pass the current path for nested rules
                    key_gen = Utility._resolve_generator(f"{field_name}_key_{i}", key_type, path + [field_name], rules)
                    value_gen = Utility._resolve_generator(f"{field_name}_value_{i}", value_type, path + [field_name], rules)
                    generated_key = key_gen() if callable(key_gen) else key_gen
                    generated_value = value_gen() if callable(value_gen) else value_gen
                    generated_dict[generated_key] = generated_value
                return generated_dict
            return generate_dict_field
        
        if origin is None and field_type in Utility._type_to_generator_map:
            return Utility._type_to_generator_map[field_type]
        
        # Handle custom class types for nested objects
        if inspect.isclass(field_type) and field_type.__module__ != 'builtins':
            def generate_nested_object(**kwargs):
                # When generating a nested object, pass existing rules and append current field to path
                instance = field_type()
                return Utility.GenerateSyntheticTestDataFor(instance, parent_path=path + [field_name], rules=rules).get_data()
            return generate_nested_object

        print(f"Warning: No specific generator found for field '{field_name}' of type '{field_type}'. Defaulting to generic string.")
        return Utility._data_generator.generate_str


    @staticmethod
    def _call_generator_with_kwargs(generator_func: Any, specific_kwargs: Dict[str, Any], field_name: str) -> Any:
        try:
            if not callable(generator_func):
                return generator_func

            # Special handling for Faker methods that don't take arbitrary kwargs
            # Faker methods usually have fixed signatures.
            # inspect.signature can help here but often safer to filter.
            if hasattr(generator_func, '__self__') and isinstance(generator_func.__self__, Faker):
                # For direct Faker methods, filter kwargs to only those accepted by its signature
                try:
                    sig = inspect.signature(generator_func)
                    accepted_params = {p.name for p in sig.parameters.values() if p.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD}
                    filtered_kwargs = {k: v for k, v in specific_kwargs.items() if k in accepted_params}
                    return generator_func(**filtered_kwargs)
                except TypeError as e:
                    # If kwargs still cause an issue, try without
                    print(f"Warning: Faker method '{generator_func.__name__}' for field '{field_name}' received unaccepted kwargs. Attempting without. Error: {e}")
                    return generator_func()
            else:
                # For our own generators, use the existing logic
                func_signature = inspect.signature(generator_func)
                accepts_kwargs = any(p.kind == inspect.Parameter.VAR_KEYWORD for p in func_signature.parameters.values())

                if accepts_kwargs:
                    return generator_func(**specific_kwargs)
                else:
                    accepted_params = {p.name for p in func_signature.parameters.values() if p.kind != inspect.Parameter.VAR_KEYWORD}
                    filtered_kwargs = {k: v for k, v in specific_kwargs.items() if k in accepted_params}
                    if len(filtered_kwargs) < len(specific_kwargs):
                        unaccepted = set(specific_kwargs.keys()) - set(filtered_kwargs.keys())
                        # Suppress this warning for 'choices' which is handled before calling generator
                        if not any(k.startswith("field_name_") and 'choices' in specific_kwargs for k in unaccepted):
                             print(f"Warning: Unaccepted kwargs {list(unaccepted)} for field '{field_name}' in '{generator_func.__name__}'. Ignoring.")
                    return generator_func(**filtered_kwargs)
        except TypeError as e:
            if "Can't parse date string" in str(e) or "argument 'start_date'" in str(e):
                print(f"Error calling generator '{generator_func.__name__}' for field '{field_name}' with args {specific_kwargs}: {e}. Falling back to default date/datetime.")
                if generator_func == Utility._data_generator.generate_date:
                    return Utility._data_generator.generate_date()
                elif generator_func == Utility._data_generator.generate_datetime:
                    return Utility._data_generator.generate_datetime()
                # For other Faker methods, try calling without args as a fallback
                return generator_func()
            print(f"Error calling generator '{generator_func.__name__}' for field '{field_name}' with args {specific_kwargs}: {e}. Calling without args.")
            return generator_func()
        except Exception as e:
            print(f"Unexpected error calling generator '{generator_func.__name__}' for field '{field_name}': {e}. Returning None.")
            return None


    @staticmethod
    def GenerateSyntheticTestDataFor(instance: Any, parent_path: List[str] = None, rules: Dict[str, Any] = None, **kwargs) -> GeneratedTestData:
        generated_data = {}
        target_class = instance.__class__
        current_path = parent_path if parent_path is not None else []
        rules = rules if rules is not None else {}

        class_annotations = inspect.get_annotations(target_class)

        init_annotations = {}
        if hasattr(target_class, '__init__'):
            init_signature = inspect.signature(target_class.__init__)
            for param_name, param in init_signature.parameters.items():
                if param_name != 'self' and param.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD:
                    if param.annotation is not inspect.Parameter.empty:
                        init_annotations[param_name] = param.annotation
        
        all_annotations = {**class_annotations, **init_annotations}

        for field_name, field_type in all_annotations.items():
            full_field_path = ".".join(current_path + [field_name])

            # Check for direct rules for this field
            if full_field_path in rules:
                field_rule = rules[full_field_path]
                if "choices" in field_rule:
                    generated_data[field_name] = random.choice(field_rule["choices"])
                    continue
                # If a custom generator is specified, use it directly
                elif "generator" in field_rule:
                    generator_func = field_rule["generator"]
                    specific_kwargs = field_rule.get("kwargs", {})
                    generated_data[field_name] = Utility._call_generator_with_kwargs(generator_func, specific_kwargs, field_name)
                    continue

            # Fallback to field_kwargs_key from kwargs if no direct rule
            field_kwargs_key = f"field_name_{field_name}"
            specific_kwargs = kwargs.get(field_kwargs_key, {})
            
            # If choices are passed via old kwargs, handle them
            if "choices" in specific_kwargs:
                if not isinstance(specific_kwargs["choices"], (list, tuple)):
                    raise TypeError(f"Choices for field '{field_name}' must be a list or tuple.")
                generated_data[field_name] = random.choice(specific_kwargs["choices"])
                continue

            generator_func = Utility._resolve_generator(field_name, field_type, current_path, rules)
            generated_data[field_name] = Utility._call_generator_with_kwargs(generator_func, specific_kwargs, field_name)

        return GeneratedTestData(generated_data)

    @staticmethod
    def _infer_json_type(value: Any):
        if isinstance(value, str):
            if len(value) == 36 and value.count('-') == 4:
                try:
                    uuid.UUID(value)
                    return uuid.UUID
                except ValueError:
                    pass
            return str
        elif isinstance(value, int):
            return int
        elif isinstance(value, float):
            return float
        elif isinstance(value, bool):
            return bool
        elif isinstance(value, list):
            if value:
                # Infer type from first element, but allow for mixed lists (though this can be tricky)
                # For simplicity, we'll still pick one type if possible.
                first_element_type = Utility._infer_json_type(value[0])
                return List[first_element_type]
            return List[Any]
        elif isinstance(value, dict):
            return Dict[str, Any] # For nested JSON objects
        elif value is None:
            return type(None)
        return Any


    @staticmethod
    def _generate_value_from_json_sample(field_name: str, sample_value: Any, specific_kwargs: Dict[str, Any], path: List[str], rules: Dict[str, Any]):
        full_field_path = ".".join(path + [field_name])

        # Check for direct rules for this field first
        if full_field_path in rules:
            field_rule = rules[full_field_path]
            if "choices" in field_rule:
                return random.choice(field_rule["choices"])
            elif "generator" in field_rule:
                generator_func = field_rule["generator"]
                specific_kwargs_from_rule = field_rule.get("kwargs", {})
                return Utility._call_generator_with_kwargs(generator_func, specific_kwargs_from_rule, field_name)

        # Fallback to existing kwargs method (like field_name_...)
        if "choices" in specific_kwargs:
            if not isinstance(specific_kwargs["choices"], (list, tuple)):
                raise TypeError(f"Choices for field '{field_name}' must be a list or tuple.")
            return random.choice(specific_kwargs["choices"])

        lower_field_name = field_name.lower()
        if lower_field_name in Utility._field_name_to_generator_map:
            generator = Utility._field_name_to_generator_map[lower_field_name]
            return Utility._call_generator_with_kwargs(generator, specific_kwargs, field_name)

        if sample_value is None:
            if random.random() < 0.2:
                return None
            print(f"Info: Field '{field_name}' had a null sample. Generating string as default. Consider explicit type/format hints for better generation.")
            return Utility._data_generator.generate_str(**specific_kwargs)

        if isinstance(sample_value, dict):
            # Recursively generate nested dictionary, passing current path and rules
            return Utility._generate_data_from_json_dict(sample_value, specific_kwargs, path + [field_name], rules)
        elif isinstance(sample_value, list):
            num_items = random.randint(1, 3)
            generated_list = []
            if sample_value:
                item_sample = sample_value[0]
                for i in range(num_items):
                    item_kwargs = specific_kwargs.get(f"item_kwargs_{i}", specific_kwargs.get("item_kwargs", {}))
                    generated_list.append(Utility._generate_value_from_json_sample(f"{field_name}_item_{i}", item_sample, item_kwargs, path + [field_name], rules))
            else:
                for i in range(num_items):
                    generated_list.append(Utility._data_generator.generate_str(min_length=3, max_length=10))
            return generated_list
        else:
            inferred_type = Utility._infer_json_type(sample_value)
            generator = None
            if inferred_type in Utility._type_to_generator_map:
                generator = Utility._type_to_generator_map[inferred_type]
            elif inferred_type == uuid.UUID:
                generator = Utility._data_generator.generate_uuid
            
            if generator:
                return Utility._call_generator_with_kwargs(generator, specific_kwargs, field_name)
            
            print(f"Warning: Could not find specific generator for JSON value of type {type(sample_value)} for field '{field_name}'. Using default string generator.")
            return Utility._data_generator.generate_str(**specific_kwargs)

    @staticmethod
    def _generate_data_from_json_dict(json_dict: Dict[str, Any], parent_kwargs: Dict[str, Any], current_path: List[str], rules: Dict[str, Any]) -> Dict[str, Any]:
        generated_object_data = {}
        for key, value_sample in json_dict.items():
            field_kwargs_key = f"field_name_{key}"
            specific_kwargs = parent_kwargs.get(field_kwargs_key, {})
            
            generated_object_data[key] = Utility._generate_value_from_json_sample(
                key, value_sample, specific_kwargs, current_path, rules
            )
        return generated_object_data


    @staticmethod
    def GenerateSyntheticTestDataFromJson(json_schema: Dict[str, Any], count: int = 1, rules: Dict[str, Any] = None, **kwargs) -> List[GeneratedTestData]:
        if not isinstance(json_schema, dict):
            raise TypeError("json_schema must be a dictionary representing a JSON object.")
        if not isinstance(count, int) or count < 1:
            raise ValueError("count must be an integer greater than or equal to 1.")
        
        rules = rules if rules is not None else {}

        generated_list = []
        for _ in range(count):
            generated_data = Utility._generate_data_from_json_dict(json_schema, kwargs, [], rules)
            generated_list.append(GeneratedTestData(generated_data))
        
        return generated_list