class FileExceptions(Exception):
    def __init__(self, message):
        super().__init__(message)


class FileCorrupted(FileExceptions):
    def __init__(self):
        super().__init__("File uploaded is corrupted.")


class FileFormatNotSupported(FileExceptions):
    def __init__(self):
        super().__init__("Supported file format are xlsx and csv")


class FileTooLarge(FileExceptions):
    def __init__(self):
        super().__init__(
            "This service uses Bing API underneath, file size has been limied to 10 record per file to save cost."
        )


class FileHeadersIncorrect(FileExceptions):
    def __init__(self):
        super().__init__(
            "Please make sure uploaded file has column 'company' that contains the companies name."
        )


class BingApiNotReachable(Exception):
    def __init__(self):
        super().__init__("Bing API not reachable")


class DatasetDoesNotExist(Exception):
    def __init__(self):
        super().__init__("Dataset does not exist")
