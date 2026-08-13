class Member:
    def __init__(self, name, member_id):
        self.name = name
        self.member_id = member_id
        self.borrowed_books = []

    def __repr__(self):
        return f"Member('{self.name}' books held {len(self.borrowed_books)})"