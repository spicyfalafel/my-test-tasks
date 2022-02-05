class Post(object):

    def __init__(self, user_id, id, title, body) -> None:
        super().__init__()
        self.user_id = user_id
        self.id = id
        self.title = title
        self.body = body

    @classmethod
    def without_id(cls, title, body):
        return cls("", "", title, body)
