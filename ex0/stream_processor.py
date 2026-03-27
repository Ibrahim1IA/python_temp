from typing import Any, List, Dict, Union
from abc import ABC, abstractmethod


class DataProcessor:

    @abstractmethod
    def process(self, data: Any) -> str:
        pass

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    def format_output(self, result: str) -> str:
        pass

class NumericProcessor(DataProcessor):
    def process(self, data: Any) -> str:
        return f"{data}"

    def validate(self, data: Any) -> bool:
        print(type(data))
        if isinstance(data, List):
            for item in data:
                if not isinstance(item, (int, float)):
                    return False
            return True
        elif isinstance(data, Dict):
            for value in data.values():
                print(value)
                if not isinstance(value, (int, float)):
                    return False
            return True
        elif isinstance(data, (int, float)):
            return True
        else:
            return False

    def format_output(self, result: str) -> str:
        if not result.startswith('[') and not result.startswith('{'):
            return f"Processed 1 numeric value, value={result}"
        values = result[1:-1].split(', ')
        sum_value = sum(int(item) for item in values)
        return f"Processed {len(values)} numeric values, sum={sum_value}"

testt = NumericProcessor()
value = {10, 4, 5}
proc = testt.process(value)
print(proc)
valid = testt.validate(value)
print(valid)
output = testt.format_output(proc)
print(output)