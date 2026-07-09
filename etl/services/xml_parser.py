class XMLParser:

    def parse(
        self,
        root,
        mapping
    ):

        records = []

        record_tag = mapping["record_tag"]

        print(f"Root Tag   : {root.tag}")
        print(f"Record Tag : {record_tag}")

        documents = root.findall(record_tag)

        print(f"Found {len(documents)} {record_tag}(s)")

        for document in documents:

            normalized = {}

            for target_field, source_field in mapping.items():

                if target_field == "record_tag":
                    continue

                element = document.find(source_field)

                if element is None:

                    normalized[target_field] = None
                    continue

                # Handle nested XML (e.g. <longtext><p>...</p></longtext>)
                if list(element):

                    text = " ".join(
                        t.strip()
                        for t in element.itertext()
                        if t.strip()
                    )

                else:

                    text = (
                        element.text.strip()
                        if element.text
                        else ""
                    )

                normalized[target_field] = text

            records.append(normalized)

        return records