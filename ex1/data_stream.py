from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple, Union


class DataStream(ABC):
    """Abstract base class for polymorphic data streams."""

    def __init__(self, stream_id: str) -> None:
        self.stream_id: str = stream_id
        self.data_count: int = 0
        self.processed_count: int = 0

    @abstractmethod
    def process_batch(self, data_batch: List[Any]) -> str:
        """Process a batch of data."""
        ...

    def filter_data(
        self, data_batch: List[Any], criteria: Optional[str] = None
    ) -> List[Any]:
        """Filter data based on criteria."""
        if criteria is None:
            return data_batch
        return data_batch

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        """Return stream statistics."""
        return {
            "stream_id": self.stream_id,
            "data_count": self.data_count,
            "processed_count": self.processed_count
        }


class SensorStream(DataStream):
    """Stream handler for sensor data."""

    def __init__(self, stream_id: str) -> None:
        super().__init__(stream_id)
        self.sensor_type: str = "Environmental Data"
        self.readings: List[float] = []

    def process_batch(self, data_batch: List[Any]) -> str:
        """Process sensor data batch."""
        try:
            if not data_batch:
                return "No sensor data to process"

            self.data_count = len(data_batch)
            numeric_readings = [
                float(x) for x in data_batch
                if isinstance(x, (int, float))
            ]

            if not numeric_readings:
                return "No valid numeric readings"

            self.readings = numeric_readings
            self.processed_count = len(numeric_readings)

            result_msg = (
                f"{self.processed_count} readings processed, "
                f"avg temp: {self.readings[0]:.1f}°C"
            )
            return result_msg
        except (ValueError, TypeError) as exc:
            return f"Error processing sensor data: {str(exc)}"

    def filter_data(
        self, data_batch: List[Any], criteria: Optional[str] = None
    ) -> List[Any]:
        """Filter sensor data based on criteria."""
        if criteria == "high":
            if not self.readings:
                return []
            avg = sum(self.readings) / len(self.readings)
            return [
                x for x in data_batch
                if isinstance(x, (int, float)) and float(x) > avg
            ]
        return super().filter_data(data_batch, criteria)

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        """Return sensor stream statistics."""
        stats = super().get_stats()
        stats["sensor_type"] = self.sensor_type
        if self.readings:
            avg_reading = sum(self.readings) / len(self.readings)
            stats["average"] = avg_reading
        return stats


class TransactionStream(DataStream):
    """Stream handler for transaction data."""

    def __init__(self, stream_id: str) -> None:
        super().__init__(stream_id)
        self.transaction_type: str = "Financial Data"
        self.total_flow: int = 0

    def process_batch(self, data_batch: List[Any]) -> str:
        """Process transaction data batch."""
        try:
            if not data_batch:
                return "No transaction data to process"

            self.data_count = len(data_batch)
            buy_flow = sum(
                x for x in data_batch
                if isinstance(x, int) and x > 0
            )
            sell_flow = sum(
                abs(x) for x in data_batch
                if isinstance(x, int) and x < 0
            )

            self.total_flow = buy_flow - sell_flow
            self.processed_count = len(data_batch)

            result_msg = (
                f"{self.processed_count} operations, "
                f"net flow: +{self.total_flow} units"
            )
            return result_msg
        except (ValueError, TypeError) as exc:
            return f"Error processing transaction data: {str(exc)}"

    def filter_data(
        self, data_batch: List[Any], criteria: Optional[str] = None
    ) -> List[Any]:
        """Filter transaction data based on criteria."""
        if criteria == "large":
            return [
                x for x in data_batch
                if isinstance(x, int) and abs(x) > 100
            ]
        return super().filter_data(data_batch, criteria)

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        """Return transaction stream statistics."""
        stats = super().get_stats()
        stats["transaction_type"] = self.transaction_type
        stats["total_flow"] = self.total_flow
        return stats


class EventStream(DataStream):
    """Stream handler for event data."""

    def __init__(self, stream_id: str) -> None:
        super().__init__(stream_id)
        self.event_type: str = "System Events"
        self.error_count: int = 0

    def process_batch(self, data_batch: List[Any]) -> str:
        """Process event data batch."""
        try:
            if not data_batch:
                return "No event data to process"

            self.data_count = len(data_batch)
            self.processed_count = len(data_batch)
            self.error_count = sum(
                1 for x in data_batch
                if isinstance(x, str) and "error" in x.lower()
            )

            error_label = "error" if self.error_count == 1 else "errors"
            msg = (
                f"{self.processed_count} events, "
                f"{self.error_count} {error_label} detected"
            )
            return msg
        except (ValueError, TypeError) as exc:
            return f"Error processing event data: {str(exc)}"

    def filter_data(
        self, data_batch: List[Any], criteria: Optional[str] = None
    ) -> List[Any]:
        """Filter event data based on criteria."""
        if criteria == "error":
            return [
                x for x in data_batch
                if isinstance(x, str) and "error" in x.lower()
            ]
        return super().filter_data(data_batch, criteria)

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        """Return event stream statistics."""
        stats = super().get_stats()
        stats["event_type"] = self.event_type
        stats["error_count"] = self.error_count
        return stats


class StreamProcessor:
    """Orchestrates processing of multiple stream types polymorphically."""

    def __init__(self) -> None:
        self.streams: List[DataStream] = []

    def add_stream(self, stream: DataStream) -> None:
        """Add a stream to the processor."""
        self.streams.append(stream)

    def process_all(
        self, data_batches: List[Tuple]
    ) -> List[str]:
        """Process multiple data batches through different streams."""
        results = []
        try:
            for stream_idx, data_batch in data_batches:
                if 0 <= stream_idx < len(self.streams):
                    result = self.streams[stream_idx].process_batch(data_batch)
                    results.append(result)
                else:
                    results.append("Invalid stream index")
        except Exception as exc:
            results.append(f"Error during batch processing: {str(exc)}")
        return results

    def filter_streams(
        self, criteria: Optional[str] = None
    ) -> List[Dict[str, Union[str, int, float]]]:
        """Filter data across all streams."""
        results = []
        try:
            for stream in self.streams:
                stats = stream.get_stats()
                results.append(stats)
        except Exception as exc:
            results.append({"error": str(exc)})
        return results


def main() -> None:
    """Main program demonstrating polymorphic stream processing."""
    print("=== CODE NEXUS - POLYMORPHIC STREAM SYSTEM ===\n")

    # Initialize streams
    print("Initializing Sensor Stream...")
    sensor = SensorStream("SENSOR_001")
    print(f"Stream ID: {sensor.stream_id}, Type: {sensor.sensor_type}")
    sensor_data = [22.5, 23.1, 21.9]
    print(
        "Processing sensor batch: [ temp:"
        f"{sensor_data[0]}, temp:{sensor_data[1]}, temp:{sensor_data[2]} ]")
    sensor_result = sensor.process_batch(sensor_data)
    print(f"Sensor analysis: {sensor_result}\n")

    # Transaction stream
    print("Initializing Transaction Stream...")
    transaction = TransactionStream("TRANS_001")
    transaction_type = transaction.transaction_type
    print(f"Stream ID: {transaction.stream_id}, Type: {transaction_type}")
    trans_data = [100, -50, 150]
    print("Processing transaction batch: [", end="")
    for i, data in enumerate(trans_data):
        if data > 0:
            print(f"buy:{data}", end=", " if i < len(trans_data) - 1 else "")
        else:
            print(f"sell:{data}", end=", " if i < len(trans_data) - 1 else "")
    print("]")
    trans_result = transaction.process_batch(trans_data)
    print(f"Transaction analysis: {trans_result}\n")

    # Event stream
    print("Initializing Event Stream...")
    event = EventStream("EVENT_001")
    print(f"Stream ID: {event.stream_id}, Type: {event.event_type}")
    event_data = ["login", "error dcs", "logout with error"]
    print(f"Processing event batch: {event_data}")
    event_result = event.process_batch(event_data)
    print(f"Event analysis: {event_result}\n")

    # Polymorphic processing
    print("=== Polymorphic Stream Processing ===")
    processor = StreamProcessor()
    processor.add_stream(sensor)
    processor.add_stream(transaction)
    processor.add_stream(event)

    print("Processing mixed stream types through unified interface...")
    data_batches = [
        (0, [22.5, 24.0]),
        (1, [75, -50, 100, -25]),
        (2, ["login", "logout", "error"])
    ]

    results = processor.process_all(data_batches)
    print("Batch 1 Results:")
    for i, result in enumerate(results):
        print(f"- Stream {i} result: {result}")

    print("\nStream filtering active: High-priority data only")
    sensor_filtered = sensor.filter_data([22.5, 24.0, 21.5], "high")
    trans_filtered = transaction.filter_data([75, -50, 10000, -25], "large")
    print(
        f"Filtered results: {len(sensor_filtered)} sensor alerts, "
        f"{len(trans_filtered)} large transactions"
    )
    print("\nAll streams processed successfully. Nexus throughput optimal.")


if __name__ == "__main__":
    main()
