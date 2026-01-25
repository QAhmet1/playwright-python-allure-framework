class PostService:
    def __init__(self, api_client):
        self.client = api_client

    def get_all_posts(self):
        return self.client.call("GET", "/posts")

    def get_single_post(self, post_id):
        return self.client.call("GET", f"/posts/{post_id}")

    def create_post(self, title, body, user_id):
        payload = {"title": title, "body": body, "userId": user_id}
        return self.client.call("POST", "/posts", data=payload)

    def update_post_full(self, post_id, title, body, user_id):
        payload = {"id": post_id, "title": title, "body": body, "userId": user_id}
        return self.client.call("PUT", f"/posts/{post_id}", data=payload)

    def update_post_partial(self, post_id, title):
        payload = {"title": title}
        return self.client.call("PATCH", f"/posts/{post_id}", data=payload)

    def delete_post(self, post_id):
        return self.client.call("DELETE", f"/posts/{post_id}")