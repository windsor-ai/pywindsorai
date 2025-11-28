import json
from typing import Any, List, Union


class Filter:
    """
    Helper class to construct API filters.
    Usage: Filter('clicks', 'gt', 0)
    """

    def __init__(self, field: str, operator: str, value: Any):
        """
        :param field: The field name (e.g. 'clicks', 'campaign')
        :param operator: eq, neq, gt, gte, lt, lte, contains, ncontains
        :param value: The value to filter against
        """
        self.field = field
        self.operator = operator
        self.value = value

    def to_list(self) -> List[Any]:
        return [self.field, self.operator, self.value]

    @staticmethod
    def to_json(filters: Union["Filter", List["Filter"], List[Any]]) -> str:
        """
        Converts a Filter object or list of Filters/lists into the
        JSON string format required by the API.
        """
        if not filters:
            return ""

        # If single filter object
        if isinstance(filters, Filter):
            return json.dumps([filters.to_list()])

        # If list of Filter objects, assume AND logic for now
        # (Complex OR logic should be constructed manually as lists)
        if isinstance(filters, list):
            # Check if it's a list of Filter objects
            if all(isinstance(f, Filter) for f in filters):
                # Simply wrap them. The API treats top-level lists as independent conditions
                # but usually requires explicit operator joining for complex logic.
                # For basic list of filters, we map them: [[A], "and", [B]]

                chain = []
                for i, f in enumerate(filters):
                    chain.append(f.to_list())
                    if i < len(filters) - 1:
                        chain.append("and")
                return json.dumps(chain)

            # If the user passed raw lists (manual construction)
            return json.dumps(filters)
