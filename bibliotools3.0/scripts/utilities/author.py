class Author:
    
    def __init__(self, data):
        self.id     = 0
        self.rank   = 0       
        self.author = ""

        self.id = int(data[0])
        self.rank = int(data[1])

        if len(data) < 3:
            self.author = "name missing"
        else:
            self.author = data[2]

    def __str__(self):
        return 'author no ' + id + ' ' + author + '\n'

    
