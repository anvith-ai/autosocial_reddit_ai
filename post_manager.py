import os

class PostManager:
    def load_replied_posts(self):
        if os.path.exists("replied_posts.txt"):
            with open("replied_posts.txt", "r") as file:
                return set(file.read().splitlines())
        else:
            return set()

    def save_replied_posts(self, replied_posts):
        with open("replied_posts.txt", "w") as file:
            file.write("\n".join(replied_posts))