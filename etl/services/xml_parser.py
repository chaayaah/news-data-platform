class XMLParser:

    def parse(
        self,
        root,
        mapping
    ):

        records = []

        record_tag = mapping["record_tag"]

        documents = root.findall(record_tag)

        for document in documents:

            normalized = {}

            for target_field, source_field in mapping.items():

                if target_field == "record_tag":
                    continue

                element = document.find(source_field)

                if element is not None:

                    normalized[target_field] = (
                        element.text.strip()
                        if element.text
                        else ""
                    )

                else:

                    normalized[target_field] = None

            records.append(
                normalized
            )

        return records