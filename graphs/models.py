from django.db import models

class Mappings(models.Model):
	TRUE_NAME = models.CharField(max_length = 100, default = "NONAME")
	FILE_NAME = models.CharField(max_length = 100, default = "NONAME")
	FILE_LINK = models.TextField(default = "NOFILE")
	GEXF_LINK = models.TextField(default = "NOGEXF")
