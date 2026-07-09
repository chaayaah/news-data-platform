class Validator:

    def __init__(
        self,
        required_fields
    ):

        self.required_fields = required_fields

    def validate(
        self,
        record
    ):

        errors = []

        for field in self.required_fields:

            if not record.get(field):

                errors.append(
                    f"{field} is missing"
                )

        return errors