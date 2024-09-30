class User:
    def __init__(self, username : str, groups : list) -> None:
        self.username = username
        self.groups = groups

    def __str__(self) -> str:
        return f"User {self.username} with role {self.role}"