from datetime import datetime


class Validator:

    def __init__(
        self,
        rules
    ):

        self.required_fields = rules["required_fields"]

        self.date_fields = rules.get(
            "date_fields",
            []
        )

    def validate(
        self,
        record
    ):

        errors = []

        # -----------------
        # Required Fields
        # -----------------

        for field in self.required_fields:

            if not record.get(field):

                errors.append(
                    f"{field} is missing"
                )

        # -----------------
        # Date Validation
        # -----------------

        for field in self.date_fields:

            value = record.get(field)

            if value:

                try:

                    datetime.strptime(
                        value,
                        "%Y-%m-%d %H:%M:%S"
                    )

                except ValueError:

                    errors.append(
                        f"{field} has invalid format"
                    )

        return errors