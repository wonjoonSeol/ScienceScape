class FilePath:
   regex = '[0-9]{4}'

   def to_python(self, value):
   	return int(value)    
