import json


class MappingLoader:

    def __init__(self):

        with open(
            "/app/mappings/vendor_registry.json",
            "r"
        ) as f:

            self.vendor_registry = json.load(f)

    def load_mapping(
        self,
        publication
    ):

        if publication not in self.vendor_registry:

            raise ValueError(
                f"Unknown vendor: {publication}"
            )

        mapping_filename = self.vendor_registry[
            publication
        ]

        mapping_path = (
            f"/app/mappings/vendors/{mapping_filename}"
        )

        with open(
            mapping_path,
            "r"
        ) as f:

            return json.load(f)