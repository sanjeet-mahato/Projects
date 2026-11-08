
import logging
import re
import unicodedata
from string import ascii_lowercase, ascii_uppercase, digits

from app.services.apploadconfig import config


logger = logging.getLogger(__name__)


class ColumnSignature:

    def __init__(self, values):
        self.values = values
        self._signature = None

        # Load datatype and metric configurations.
        self.data_types = config["column_signature"]["data_types"]
        self.metrics = config["column_signature"]["metrics"]

    @property
    def signature(self):
        # Build the signature only when it is first requested.
        if self._signature is None:
            self.build()

        return self._signature

    # =========================================================
    # Signature construction
    # =========================================================

    def build(self):
        """Build and cache the complete column signature."""

        self._signature = {
            "data_type_distribution": self.get_data_type_distribution(),
            **self.get_length_metrics(),
            "unique_ratio": self.get_unique_ratio(),
            "character_set": self.get_character_set(),
            "average_numeric_ratio": self.get_average_numeric_ratio(),
            "empty_ratio": self.get_empty_ratio(),
        }

        return self._signature

    # =========================================================
    # Value normalization
    # =========================================================

    @staticmethod
    def normalize_value(value):
        """Convert a value to a trimmed string."""

        if value is None:
            return ""

        return str(value).strip()

    def get_non_empty_values(self):
        """Return trimmed, non-empty column values."""

        return [
            self.normalize_value(value)
            for value in self.values
            if self.normalize_value(value)
        ]

    # =========================================================
    # Datatype classification
    # =========================================================

    def get_data_type_index(self, value):
        """Return the first matching datatype index."""

        for index, data_type in enumerate(self.data_types):
            if re.match(data_type["pattern"], value):
                return index

        # String is the configured fallback datatype.
        return len(self.data_types) - 1

    def get_data_type_distribution(self):
        """Calculate the proportion of each configured datatype."""

        distribution = [0.0] * len(self.data_types)

        if not self.values:
            return distribution

        for value in self.values:
            normalized_value = self.normalize_value(value)
            index = self.get_data_type_index(normalized_value)
            distribution[index] += 1

        total = len(self.values)

        return [count / total for count in distribution]

    # =========================================================
    # Length metrics
    # =========================================================

    def get_length_metrics(self):
        """Calculate average, minimum and maximum trimmed lengths."""

        values = self.get_non_empty_values()
        lengths = [len(value) for value in values]

        if not lengths:
            return {
                "average_length": 0.0,
                "min_length": 0,
                "max_length": 0,
            }

        return {
            "average_length": sum(lengths) / len(lengths),
            "min_length": min(lengths),
            "max_length": max(lengths),
        }

    # =========================================================
    # Unique ratio
    # =========================================================

    def get_unique_ratio(self):
        """Calculate unique non-empty values / total non-empty values."""

        values = self.get_non_empty_values()

        if not values:
            return 0.0

        return len(set(values)) / len(values)

    # =========================================================
    # Character set
    # =========================================================

    @staticmethod
    def get_character_category(character):
        """Identify the category of an individual character."""

        if character in ascii_lowercase:
            return "lowercase"

        if character in ascii_uppercase:
            return "uppercase"

        if character in digits:
            return "digits"

        if character.isspace():
            return "whitespace"

        # Unicode punctuation and symbols.
        category = unicodedata.category(character)

        if category.startswith(("P", "S")):
            return "special"

        return "others"

    def get_character_set(self):
        """Identify all character categories present in the column."""

        categories = {
            "lowercase": False,
            "uppercase": False,
            "digits": False,
            "special": False,
            "whitespace": False,
            "others": False,
        }

        for value in self.values:
            if not self.normalize_value(value):
                continue

            for character in str(value):
                category = self.get_character_category(character)
                categories[category] = True

        return categories

    # =========================================================
    # Average numeric ratio
    # =========================================================

    def get_average_numeric_ratio(self):
        """
        Calculate the average numeric-character ratio per non-empty cell.

        Individual cell ratio =
            numeric characters / total characters in that cell
        """

        values = self.get_non_empty_values()

        if not values:
            return 0.0

        ratios = []

        for value in values:
            numeric_count = sum(character in digits for character in value)
            ratios.append(numeric_count / len(value))

        return sum(ratios) / len(ratios)

    # =========================================================
    # Empty ratio
    # =========================================================

    def get_empty_ratio(self):
        """Calculate whitespace-only or empty cells / total cells."""

        if not self.values:
            return 0.0

        empty_count = sum(
            not self.normalize_value(value)
            for value in self.values
        )

        return empty_count / len(self.values)

    # =========================================================
    # Similarity calculations
    # =========================================================

    @staticmethod
    def get_relative_similarity(value_a, value_b):
        """Compare numeric values using relative difference."""

        denominator = max(abs(value_a), abs(value_b), 1)

        return max(
            0.0,
            1.0 - abs(value_a - value_b) / denominator
        )

    @staticmethod
    def get_ratio_similarity(value_a, value_b):
        """Compare two ratios."""

        return 1.0 - abs(value_a - value_b)

    @staticmethod
    def get_character_set_similarity(set_a, set_b):
        """Compare character categories using Jaccard similarity."""

        categories_a = {
            name for name, present in set_a.items() if present
        }

        categories_b = {
            name for name, present in set_b.items() if present
        }

        union = categories_a | categories_b

        if not union:
            return 1.0

        intersection = categories_a & categories_b

        return len(intersection) / len(union)

    def get_data_type_similarity(self, distribution_a, distribution_b):
        """Compare datatype distributions using weighted Euclidean distance."""

        if len(distribution_a) != len(distribution_b):
            raise ValueError("Datatype distributions have different lengths.")

        if any(data_type["weight"] < 0 for data_type in self.data_types):
            raise ValueError("Datatype weights cannot be negative.")

        total_weight = sum(
            data_type["weight"] for data_type in self.data_types
        )

        if total_weight <= 0:
            raise ValueError("Datatype weights must have a positive total.")

        # Calculate weighted Euclidean distance between distributions.
        distance = sum(
            data_type["weight"] * (value_a - value_b) ** 2
            for data_type, value_a, value_b in zip(
                self.data_types,
                distribution_a,
                distribution_b,
            )
        )

        distance = (distance / total_weight) ** 0.5

        return max(0.0, min(1.0, 1.0 - distance))

    # =========================================================
    # Column comparison
    # =========================================================

    def compare(self, other, column_index: int):
        """Return the weighted similarity between two column signatures."""

        if not isinstance(other, ColumnSignature):
            raise TypeError("Expected another ColumnSignature instance.")

        if any(metric["weight"] < 0 for metric in self.metrics.values()):
            raise ValueError("Metric weights cannot be negative.")

        total_weight = sum(metric["weight"] for metric in self.metrics.values())

        if total_weight <= 0:
            raise ValueError("Metric weights must have a positive total.")

        signature_a = self.signature
        signature_b = other.signature

        # Calculate similarity independently for every configured metric.
        metric_similarities = {
            "data_type_distribution": self.get_data_type_similarity(
                signature_a["data_type_distribution"],
                signature_b["data_type_distribution"],
            ),
            "average_length": self.get_relative_similarity(
                signature_a["average_length"],
                signature_b["average_length"],
            ),
            "min_length": self.get_relative_similarity(
                signature_a["min_length"],
                signature_b["min_length"],
            ),
            "max_length": self.get_relative_similarity(
                signature_a["max_length"],
                signature_b["max_length"],
            ),
            "unique_ratio": self.get_ratio_similarity(
                signature_a["unique_ratio"],
                signature_b["unique_ratio"],
            ),
            "character_set": self.get_character_set_similarity(
                signature_a["character_set"],
                signature_b["character_set"],
            ),
            "average_numeric_ratio": self.get_ratio_similarity(
                signature_a["average_numeric_ratio"],
                signature_b["average_numeric_ratio"],
            ),
            "empty_ratio": self.get_ratio_similarity(
                signature_a["empty_ratio"],
                signature_b["empty_ratio"],
            ),
        }

        weighted_similarity = sum(
            metric["weight"] * metric_similarities[name]
            for name, metric in self.metrics.items()
        )

        final_similarity = weighted_similarity / total_weight

        # Log the metric comparison as one block for easier inspection.
        logger.debug(
            "Column comparison | Index: %s\n"
            "  Datatype distribution : %.4f\n"
            "  Average length        : %.4f\n"
            "  Minimum length        : %.4f\n"
            "  Maximum length        : %.4f\n"
            "  Unique ratio          : %.4f\n"
            "  Character set         : %.4f\n"
            "  Numeric ratio         : %.4f\n"
            "  Empty ratio           : %.4f\n"
            "  Final similarity      : %.4f",
            column_index,
            metric_similarities["data_type_distribution"],
            metric_similarities["average_length"],
            metric_similarities["min_length"],
            metric_similarities["max_length"],
            metric_similarities["unique_ratio"],
            metric_similarities["character_set"],
            metric_similarities["average_numeric_ratio"],
            metric_similarities["empty_ratio"],
            final_similarity,
        )

        return final_similarity
