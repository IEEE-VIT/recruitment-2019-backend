class Moderator(models.Model):
	moderator_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
	room = models.CharField(max_length=10)

	def save(self, *args, **kwargs):
		super(moderator, self).save(*args, **kwargs)


