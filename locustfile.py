from locust import HttpUser, task
import random
import base64

from faker import Faker

with open("locust_test.jpeg", "rb") as f:
    data = f.read()
image = base64.b64encode(data).decode("ascii")
faker = Faker()


class HelloWorldUser(HttpUser):
    meme_max_ind = 1

    @task(2)
    def get_memes(self):
        pages = int(self.meme_max_ind / 10)
        if pages not in [0, 1]:
            page = random.randint(1, pages)
        else:
            page = 1
        self.client.get("/memes", params={'page_number': page})

    @task(5)
    def get_meme(self):
        ind = random.randint(1, self.meme_max_ind if self.meme_max_ind else 0)
        self.client.get(f"/memes/{ind}")

    @task(5)
    def create_meme(self):
        self.client.post(
            "/memes",
            json={"title": faker.company(), "author": faker.name(), "image": image},
        )
        self.meme_max_ind += 1

    @task(1)
    def update_meme(self):
        self.client.delete("/memes/192839128391")
