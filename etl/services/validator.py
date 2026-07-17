from datetime import datetime


class Validator:

    def __init__(self, rules):

        self.required_fields = rules["required_fields"]

        self.date_fields = rules.get(
            "date_fields",
            []
        )

        # Store (publication_name, article_id)
        self.seen_article_ids = set()

    # -----------------------------
    # Required Fields
    # -----------------------------

    def validate_required_fields(
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

    # -----------------------------
    # Date Validation
    # -----------------------------

    def validate_date_fields(
        self,
        record
    ):

        errors = []

        for field in self.date_fields:

            value = record.get(field)

            if not value:
                continue

            try:

                parsed_date = datetime.strptime(
                    value,
                    "%Y-%m-%d %H:%M:%S"
                )

                if parsed_date > datetime.now():

                    errors.append(
                        f"{field} cannot be in the future"
                    )

            except ValueError:

                errors.append(
                    f"{field} has invalid format"
                )

        return errors

    # -----------------------------
    # Duplicate Validation
    # -----------------------------

    def validate_duplicate_article(
        self,
        record
    ):

        errors = []

        publication_name = record.get("publication_name")
        article_id = record.get("article_id")

        if not publication_name or not article_id:
            return errors

        key = (
            publication_name,
            article_id
        )

        if key in self.seen_article_ids:

            errors.append(
                f"Duplicate article_id '{article_id}' for publication '{publication_name}'"
            )

        else:

            self.seen_article_ids.add(key)

        return errors

    # -----------------------------
    # Master Validation
    # -----------------------------

    def validate(
        self,
        records
    ):

        valid_records = []
        invalid_records = []

        for record in records:

            errors = []

            errors.extend(
                self.validate_required_fields(record)
            )

            errors.extend(
                self.validate_date_fields(record)
            )

            errors.extend(
                self.validate_duplicate_article(record)
            )

            if errors:

                record["validation_errors"] = errors

                invalid_records.append(record)

            else:

                valid_records.append(record)

        return valid_records, invalid_records