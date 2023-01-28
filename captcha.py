import os
from typing import List


class Captcha:
    def __init__(self, variants: List[str], answer: str, file_path: str) -> None:
        self.variants = variants
        self.answer = answer
        self.file_path = file_path

    def remove(self) -> None:
        os.remove(self.file_path)
