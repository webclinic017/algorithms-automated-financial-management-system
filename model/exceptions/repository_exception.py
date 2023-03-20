class RepositoryException(Exception):

    def __init__(self, messages):
        self.messages = messages

    def get_messages(self):
        return self.messages
