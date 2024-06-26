class Keypoint():
    """Class representing one keypoint with it's coordinates and confidence
    """

    def __init__(self, x=None, y=None, confidence=None):
        self.x = x
        self.y = y
        self.confidence = confidence

    # pretty printing
    def __repr__(self):
        return ("""x: {x}, y: {y}, confidence: {conf}""".format(x=self.x, y=self.y, conf=self.confidence))
