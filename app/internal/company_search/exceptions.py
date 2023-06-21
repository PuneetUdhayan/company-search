class FileFormatNotSupported(Exception):

    def __init__(self):
        self.super("Supported file format are xlsx and csv")


class FileTooLarge(Exception):

    def __init__(self):
        self.super("This service uses Bing API underneath, file size has been limied to 10 record per file to save cost.")


class FileHeadersIncorrect(Exception):

    def __init__(self):
        self.super("Please make sure uploaded file has column 'companies' that contains the companies name.")

