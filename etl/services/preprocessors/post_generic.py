class PostGeneric:

    def process(self, records):

        print("Running Post Generic...")

        for record in records:

            self.normalize_author(record)
            self.normalize_publication(record)
            self.trim_values(record)

        return records

    # -----------------------------
    # Normalize Author
    # -----------------------------

    def normalize_author(self, record):

        author = record.get("author")

        if author:
            record["author"] = author.title()

    # -----------------------------
    # Normalize Publication Name
    # -----------------------------

    def normalize_publication(self, record):

        publication = record.get("publication_name")

        if publication:

            mapping = {
                "businessdesk": "BusinessDesk",
                "reuters": "Reuters",
                "bloomberg": "Bloomberg",
                "packreport": "PackReport"
            }

            record["publication_name"] = mapping.get(
                publication.lower(),
                publication
            )

    # -----------------------------
    # Trim all string values
    # -----------------------------

    def trim_values(self, record):

        for key, value in record.items():

            if isinstance(value, str):
                record[key] = value.strip()