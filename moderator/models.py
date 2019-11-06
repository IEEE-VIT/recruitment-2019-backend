# Todo You haven't imported models - Sukriti


class Moderator(models.Model):
    moderator_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    room = models.CharField(max_length=10)

    def save(self, *args, **kwargs):
        # Todo What is a moderator
        super(moderator, self).save(*args, **kwargs)

    # Todo Add a '__str__' function - Sukriti
