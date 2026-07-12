import re


class PreGeneric:

    def process(
        self,
        root
    ):
        print("Running Pre Generic...")

        print("    ✓ Trim whitespace")
        self.trim_whitespace(root)

        print("    ✓ Normalize whitespace")
        self.normalize_whitespace(root)

        

        return root

    # -----------------------------
    # Remove leading/trailing spaces
    # -----------------------------

    def trim_whitespace(
        self,
        element
    ):

        if element.text:
            element.text = element.text.strip()

        if element.tail:
            element.tail = element.tail.strip()

        for child in element:

            self.trim_whitespace(child)

    # -----------------------------
    # Collapse multiple spaces
    # -----------------------------

    def normalize_whitespace(
        self,
        element
    ):

        if element.text:

            element.text = re.sub(
                r"\s+",
                " ",
                element.text
            )

        for child in element:

            self.normalize_whitespace(child)