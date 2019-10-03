class TextCheck:
    def __init__(self, text):
        self.text = text

    def check_float(self):
        try:
            float(self.text)
            return True
        except:
            return False

    def check_integer(self):
        try:
            int(self.text)
            return True
        except:
            return False