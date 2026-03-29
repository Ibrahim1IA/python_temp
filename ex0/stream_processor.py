from typing import Any, List, Dict, Union, Optional
from abc import ABC, abstractmethod


class DataProcessor(ABC):
    @abstractmethod
    def process(self, data: Any) -> str:
        """Process the data and return result string """
        pass

    @abstractmethod
    def validate(self, data: Any) -> bool:
        """Validate if data is appropriate for this processor """
        pass

    def format_output(self, result: str) -> str:
        """
        Format the output string - Default implementation
        """
        return f"Output: {result}"


class NumericProcessor(DataProcessor):

    def validate(self, data: Any) -> bool:
        if isinstance(data, List):
            for item in data:
                if not isinstance(item, (int, float)):
                    return False
            return True
        elif isinstance(data, Dict):
            for value in data.values():
                if not isinstance(value, (int, float)):
                    return False
            return True
        elif isinstance(data, (int, float)):
            return True
        else:
            return False

    def process(self, data: Any) -> str:
        if not self.validate(data):
            return "Error: Invalid numeric data"
        sum_val = sum(data)
        avg_val = sum_val / len(data)

        return f"Processed {len(data)} numeric values, sum="\
            f"{int(sum_val) if sum_val % 1 == 0 else sum_val}"\
            f", avg={avg_val:.1f}"


class TextProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        return isinstance(data, str)

    def process(self, data: Any) -> str:
        if not self.validate(data):
            return "Error: Invalid text data"
        words = len(data.split())
        return f"Processed text: {len(data)} characters, {words} words"


class LogProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, str):
            values = data.split(' ')
            if ':' in values[0]:
                return True
            else:
                return False
        else:
            return False

    def process(self, data: Any) -> str:
        if not self.validate(data):
            return "Error: Invalid log entry"
        level, message = data.split(":", 1)
        level = level.strip().upper()
        message = message.strip()
        prefix = "[ALERT]" if level == "ERROR" else "[INFO]"
        return f"{prefix} {level} level detected: {message}"

    def format_output(self, result: str) -> str: 
        return result


def main() -> None:
    print("=== CODE NEXUS - DATA PROCESSOR FOUNDATION ===\n")

    processors: Optional[
        list[tuple[str, DataProcessor, Union[list[int], str]]]
    ] = [
        ("Numeric", NumericProcessor(), [1, 2, 3, 4, 5]),
        ("Text", TextProcessor(), "Hello Nexus World"),
        ("Log", LogProcessor(), "ERROR: Connection timeout")
    ]
    try:
        if not processors:
            raise ValueError("No processors specified")
        for name, proc, data in processors:
            print(f"Initializing {name} Processor...")

            display_data = f'"{data}"' if isinstance(data, str) else data
            print(f"Processing data: {display_data}")

            if proc.validate(data):

                v_msg = "Log entry" if name == "Log" else f"{name} data"
                print(f"Validation: {v_msg} verified")
                result = proc.process(data)
                print(proc.format_output(result))
            else:
                print(f"Validation: {name} data invalid")
            print()
    except ValueError as e:
        print(f"Error: {e}")
        return

    print("=== Polymorphic Processing Demo ===")
    print("Processing multiple data types through same interface...")

    mixed_data: Optional[list[tuple[Any, DataProcessor]]] = [
        ([1, 2, 3], NumericProcessor()),
        ("Hello Nexus", TextProcessor()),
        ("INFO: System ready", LogProcessor())
    ]
    try:
        if not mixed_data:
            raise ValueError("No mixed data to process")
        for i, (data, processor) in enumerate(mixed_data, 1):
            res = processor.process(data)
            print(f"Result {i}: {res}")
    except ValueError as e:
        print(f"Error: {e}")
        return

    print("\nFoundation systems online. Nexus ready for advanced streams.")


if __name__ == "__main__":
    main()