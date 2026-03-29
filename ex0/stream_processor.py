from typing import Any, List, Dict, Union, Optional
from abc import ABC, abstractmethod


class DataProcessor(ABC):

    @abstractmethod
    def process(self, data: Any) -> str:
        pass

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    def format_output(self, result: str) -> str:
        return f"Processed data {result}"


class NumericProcessor(DataProcessor):
    def process(self, data: Any) -> str:
        if isinstance(data, List):
            return f"{data}"
        elif isinstance(data, Dict):
            return f"{list(data.values())}"
        else:
            return f"{data}"

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

    def format_output(self, result: str) -> str:
        valid: bool = True
        for char in result:
            if char.isdigit() or char in ['[', ']', ' ', ',', '.']:
                continue
            else:
                valid = False
                break
        if valid:
            if not result.startswith('['):
                return f"Processed 1 numeric value, value={result}"
            else:
                values: List[str] = result[1:-1].split(', ')
                sum_value: float = sum(float(item) for item in values)
                average_value: float = sum_value / len(values) if values else 0
                return f"Processed {len(values)} numeric values, sum="\
                    f"{sum_value if sum_value % 1 != 0 else int(sum_value)}"\
                    f", average={average_value:.1f}"
        else:
            return f"Processed data {result}"


class TextProcessor(DataProcessor):
    def process(self, data: Any) -> str:
        if isinstance(data, str):
            return f"'{data}'"
        else:
            return f"{data}"

    def validate(self, data: Any) -> bool:
        if isinstance(data, str):
            return True
        else:
            return False

    def format_output(self, result: str) -> str:
        if self.validate(result):
            if result.startswith("'") and result.endswith("'"):
                result = result[1:-1]
                return \
                    f"Processed text: {len(result)} characters,"\
                    f" {result.count(' ')+1} words"
            else:
                return f"Processed data {result} is not valid text data"
        else:
            return f"Processed data {result} is not valid text data"


class LogProcessor(DataProcessor):
    def process(self, data: Any) -> str:
        if isinstance(data, str):
            return f"'{data}'"
        else:
            return f"{data}"

    def validate(self, data: Any) -> bool:
        if isinstance(data, str):
            values = data.split(' ')
            if ':' in values[0]:
                return True
            else:
                return False
        else:
            return False

    def format_output(self, result: str) -> str:
        if self.validate(result):
            if result.startswith("'") and result.endswith("'"):
                result = result[1:-1]
                values = result.split(' ')
                log_level = values[0][0:-1]
                message = ' '.join(values[1:])
                return f"[ALERT] {log_level} level detected :{message}"
            else:
                return f"Processed data {result} is not valid log data"
        else:
            return f"Processed data << {result} >> is not valid log data"


def main() -> None:
    numeric_processor = NumericProcessor()
    text_processor = TextProcessor()
    log_processor = LogProcessor()

    processors: Optional[list[str]] = ["Numeric", "Text", "Log"]
    number_data: Optional[list[Union[int, float]]] = [1, 2, 3, 4.7, 5]
    text_data: Optional[str] = "Hello world"
    log_data: Optional[str] = "ERROR: Something went wrong"
    print(" === CODE NEXUS - DATA PROCESSOR FOUNDATION ===")
    try:
        if not processors:
            raise ValueError("No processors specified")
    except ValueError as e:
        print(f"Error: {e}")
        return
    for processor_type in processors:
        print(f"Initializing {processor_type} Processor...")
        if processor_type == "Numeric":
            result = numeric_processor.process(number_data)
            is_valid = numeric_processor.validate(number_data)
            output = numeric_processor.format_output(result)
            print(f"Processing data : {result}")
            print(
                f"Validation: "
                f"{"Numeric data verified" if is_valid else
                    "Numeric data invalid"}"
            )
            print(f"Output: {output}")
        elif processor_type == "Text":
            result = text_processor.process(text_data)
            is_valid = text_processor.validate(text_data)
            output = text_processor.format_output(result)
            print(f"Processing data : {result}")
            print(
                f"Validation: "
                f"{"Text data verified" if is_valid else
                    "Text data invalid"}"
            )
            print(f"Output: {output}")
        elif processor_type == "Log":
            result = log_processor.process(log_data)
            is_valid = log_processor.validate(log_data)
            output = log_processor.format_output(result)
            print(f"Processing data : {result}")
            print(
                f"Validation: "
                f"{"Log entry verified" if is_valid else
                    "Log entry invalid"}"
            )
            print(f"Output: {output}")
        print()
    print("=== Polymorphic Processing Demo ===")


if __name__ == "__main__":
    main()
