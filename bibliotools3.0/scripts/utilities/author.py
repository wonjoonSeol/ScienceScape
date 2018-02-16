class Author:
    self.id     = 0
    self.rank   = 0       
    self.author = ""

    def __init__(self, data):
        self.id = int(data[0])
        self.rank = int(data[1])

        if len(data) < 3:
            self.author = "name missing"
        else:
            self.author = data[2]


    
