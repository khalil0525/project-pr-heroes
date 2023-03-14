import unittest
from peewee import *
from playhouse.shortcuts import model_to_dict

from src.app.models.timelinepost import TimelinePost

MODELS = [TimelinePost]

# use an in-memory SQLite for tests.
test_db = SqliteDatabase(":memory:")


class TestTimelinePost(unittest.TestCase):
    def setUp(self):
        # Bind model classes to test db. Since we have a complete list of
        # all models, we do not need to recursively bind dependencies.
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)

        test_db.connect()
        test_db.create_tables(MODELS)

    def tearDown(self):
        # Not strictly necessary since SQLite in-memory databases only live
        # for the duration of the connection, and in the next step we close
        # the connection...but a good practice all the same.
        test_db.drop_tables(MODELS)

        # Close connection to db.
        test_db.close()

    def test_timeline_post(self):
        # Create 2 timeline posts.
        first_post = TimelinePost.create(
            name="John Doe", email="john@example.com", content="Hello World, I'm John!"
        )
        assert first_post.id == 1
        second_post = TimelinePost.create(
            name="Jane Doe", email="jane@example.com", content="Hello World, I'm Jane!"
        )
        assert second_post.id == 2
        # TODO: Get timeline posts and assert that they are correct
        timeline_posts = {
            "timeline_posts": [
                model_to_dict(p)
                for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
            ]
        }
        posts = timeline_posts.get("timeline_posts")
        assert len(posts) == 2
