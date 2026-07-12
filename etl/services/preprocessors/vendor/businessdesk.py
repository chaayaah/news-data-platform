from etl.services.preprocessors.vendor.base import VendorPreprocessor


class BusinessDeskPreprocessor(VendorPreprocessor):

    def process(self, root):

        print("Running BusinessDesk Preprocessor...")

        return root