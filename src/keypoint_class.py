class Keypoint():
    def __init__(self, x, y, confidence):
        self.x = x
        self.y = y
        self.confidence = confidence

    def __repr__(self):
        return ("""x: {x}, y: {y}, confidence: {conf}""".format(x=self.x, y=self.y, conf=self.confidence))
