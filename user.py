class User:
    def __init__(self, chat_id, username=None, first_name=None, last_name=None):
        self.chat_id = chat_id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name

    def __str__(self):
        if self.username:
            return f"@{self.username}"
        elif self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        else:
            return f"{self.chat_id}"
