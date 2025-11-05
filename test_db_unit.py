import unittest
import sqlite3
import os
from db_unit import build_db, save_to_db


class TestDbUnit(unittest.TestCase):
    
    def setUp(self):
        """Set up test database before each test"""
        # Remove the main database to start fresh
        if os.path.exists("reddit_sentiment.db"):
            os.remove("reddit_sentiment.db")
    
    def tearDown(self):
        """Clean up test database after each test"""
        # Clean up the database after tests
        if os.path.exists("reddit_sentiment.db"):
            os.remove("reddit_sentiment.db")
    
    def test_build_db(self):
        """Test that build_db creates the database and posts table"""
        # Create the database
        build_db()
        
        # Verify database was created
        self.assertTrue(os.path.exists("reddit_sentiment.db"))
        
        # Verify table structure
        conn = sqlite3.connect("reddit_sentiment.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='posts'")
        result = cursor.fetchone()
        conn.close()
        
        # Assert table exists
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "posts")
    
    def test_save_to_db(self):
        """Test that save_to_db correctly saves posts with sentiment"""
        # First build the database
        build_db()
        
        # Test data
        platform = "Reddit"
        posts = ["This is a great post!", "Another awesome post!"]
        sentiment_data = {'positive': 10, 'negative': 2}
        
        # Save to database
        save_to_db(platform, posts, sentiment_data)
        
        # Verify data was saved
        conn = sqlite3.connect("reddit_sentiment.db")
        cursor = conn.cursor()
        cursor.execute("SELECT platform, content, sentiment FROM posts")
        results = cursor.fetchall()
        conn.close()
        
        # Assert two posts were saved
        self.assertEqual(len(results), 2)
        
        # Assert first post data
        self.assertEqual(results[0][0], "Reddit")
        self.assertEqual(results[0][1], "This is a great post!")
        self.assertEqual(results[0][2], "Positive")


if __name__ == '__main__':
    unittest.main()
