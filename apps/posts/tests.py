from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from apps.posts.models import Post
from apps.tags.models import Tag
from apps.likes.models import Like
from apps.comments.models import Comment

def create_user(username, password="password1234"):
    return User.objects.create_user(username=username, password=password)

def create_post(author, content):
    return Post.objects.create(author=author, content=content)

def create_tag(tag):
    return Tag.objects.create(name=tag)

class PostViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.password = 'password1234'
        self.post_author = create_user('author', password=self.password)
        self.other_user = create_user('other_user', password=self.password)
        
        # ログイン
        self.client.login(username=self.post_author, password=self.password)
        
    def test_post_list_view(self):
        post1 = create_post(self.post_author, 'Post A')
        post2 = create_post(self.post_author, 'Post B')
        
        response = self.client.get(reverse('posts:post_list'))
        self.assertEqual(response.status_code, 200)
        
        posts = response.context['posts']
        self.assertEqual(len(posts), 2)
        self.assertIn(post1, posts)
        self.assertIn(post2, posts)

    def test_my_posts(self):
        post1 = create_post(self.post_author, '投稿1')
        _ = create_post(self.post_author, '投稿2')
        other_post = create_post(self.other_user, '他人の投稿')
        
        url = reverse('posts:my_posts', kwargs={
            'username': self.post_author.username
        })
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        
        posts = response.context['posts']
        
        self.assertEqual(len(posts), 2)
        self.assertIn(post1, posts)
        self.assertNotIn(other_post, posts)       
        
    def test_delete_post(self):
        post = create_post(self.post_author, '確認用投稿')
        
        url = reverse('posts:post_delete', kwargs={
            'username': self.post_author.username, 
            'post_id': post.id 
        })
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'apps/post/list.html')
        
    def test_edit_post(self):
        post = create_post(self.post_author, '確認用投稿')
        
        url = reverse('posts:post_edit', kwargs={
            'username': self.post_author.username, 
            'post_id': post.id
        })
        
        # 編集後に更新するデータ
        updated_content = '編集済みの投稿'
        updated_tags = 'tag1, tag2, tag3, tag4'
        
        response = self.client.post(url, {
            'content': updated_content, 
            'tags': updated_tags, 
        })
        
        # 編集後リダイレクト
        self.assertEqual(response.status_code, 302)
        
        post.refresh_from_db()
        self.assertEqual(post.content, updated_content)
        
        tag_names = sorted([tag.name for tag in post.tags.all()])
        expected_tags = sorted(['tag1', 'tag2', 'tag3', 'tag4'])
        self.assertEqual(tag_names, expected_tags)
        
    def test_create_post(self):
        
        url = reverse('posts:post_create')
        
        new_content = '新規の投稿'
        new_tags = 'tag1, tag2, tag3'
        
        response = self.client.post(url, {
            'author': self.post_author, 
            'content': new_content, 
            'tags': new_tags, 
        })
        
        self.assertEqual(response.status_code, 302)
        
        post = Post.objects.get(content=new_content)
        self.assertEqual(post.author, self.post_author)
        
        tag_names = set(tag.name for tag in post.tags.all())
        expected_tags = set(['tag1', 'tag2', 'tag3'])
        self.assertEqual(tag_names, expected_tags)
        
    def test_post_detail(self):
        post = create_post(self.post_author, '投稿1')
        tag_names = 'tag1, tag2, tag3'
        
        # タグを追加
        for tag_name in tag_names.split(','):
            tag = Tag.objects.create(name=tag_name.strip())
            post.tags.add(tag)
        
        users = ['user1', 'user2', 'user3', 'user4']
        comments = ['コメント1', 'コメント2', 'コメント3', 'コメント4']
        
        for user, comment in zip(users, comments):
            Comment.objects.create(post=post, author=create_user(user), comment=comment)
        
        url = reverse('posts:post_detail', kwargs={
            'username': self.post_author.username, 
            'post_id': post.id
        })
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        
        # 投稿内容・タグ・コメントがテンプレートに含まれているか確認
        self.assertContains(response, '投稿1')
        self.assertContains(response, 'tag1')
        self.assertContains(response, 'コメント1')
        self.assertContains(response, 'コメント4')

        # 閲覧数が1に増えていることを確認
        post.refresh_from_db()
        self.assertEqual(post.views, 1)
    
    
class PostModelTests(TestCase):
    def setUp(self):
        self.post_author = create_user('author')
        self.like_user = create_user('liker')
        
    def assert_like_exists(self, user, post, expected: bool):
        exists = Like.objects.filter(user=user, post=post).exists()
        self.assertEqual(exists, expected)
            
    def test_is_liked_by(self):
        # ユーザーと投稿を作成
        user = create_user('Bob')
        post = create_post(user, 'TestContent1')
        
        # Like がまだ押されていない
        self.assertFalse(post.is_liked_by(user))
        
        # Like を追加したとき
        Like.objects.create(user=user, post=post)
        self.assertTrue(post.is_liked_by(user))
    
    def test_get_view_count(self):
        test_cases = [0, 16, 53, 100]
        post = create_post(self.post_author, "Hello, world!")
        
        for view_value in test_cases:
            with self.subTest(f"views = {view_value}"):
                post.views = view_value
                post.save()
                self.assertEqual(post.get_view_count(), view_value)
                
    def test_get_posts_by_tag(self):
        def all_with(posts, tag):
            return all(tag in post.tags.all() for post in posts)
        
        # 投稿の作成        
        post1 = create_post(self.post_author, 'TestContent1')
        post2 = create_post(self.post_author, 'TestContent2')
        post3 = create_post(self.post_author, 'TestContent3')
        post4 = create_post(self.post_author, 'TestContent4')
        post5 = create_post(self.post_author, 'TestContent5')
        
        # Tag の作成
        tag1 = create_tag('test_tag1')
        tag2 = create_tag('test_tag2')
        tag3 = create_tag('test_tag3')
        
        # Tag を Post に付ける
        post1.tags.add(tag1, tag2, tag3)
        post2.tags.add(tag1, tag3)
        post3.tags.add(tag1, tag2)
        post4.tags.add(tag1, tag3)
        post5.tags.add(tag1)
        
        posts_with_tag1 = Post.get_posts_by_tag(tag1)
        posts_with_tag2 = Post.get_posts_by_tag(tag2)
        
        with self.subTest('タグの個数'):
            self.assertEqual(posts_with_tag1.count(), 5)
        
        with self.subTest('全ての投稿に tag1 が含まれているか'):
            self.assertTrue(all_with(posts_with_tag1, tag1))
            
        with self.subTest('無効なタグが含まれていない'):
            self.assertIn(post3, posts_with_tag2)
            
        with self.subTest('タグが含まれていない投稿'):
            post_without_tag = create_post(self.post_author, 'TestContent6')
            self.assertNotIn(tag2, post_without_tag.tags.all())
        
    def test_toggle_like_by(self):
        user = create_user('Alice')
        post = create_post(create_user('Tom'), 'TestContent')
        
        states = [
            ('最初は Like なし', False), 
            ('1回目で追加', True), 
            ('2回目で削除', False), 
            ('3回目で再追加', True), 
        ]
        
        for label, expected in states:
            with self.subTest(label):
                self.assert_like_exists(user, post, expected)
                
            post.toggle_like_by(user)
        
    def test_get_posts_by_user(self):
        def all_by(author, posts):
            return all(post.author == author for post in posts)
        
        # 投稿の作成
        posts = [
            'Post A', 
            'Post B', 
            'Post C', 
            'Post D', 
            'Post E'
        ]
        
        for post in posts:
            create_post(self.post_author, post)
        
        # ユーザーの投稿を取得
        author_posts = Post.get_posts(self.post_author)
        
        with self.subTest('投稿数'):
            self.assertEqual(author_posts.count(), 5)
        
        with self.subTest('全ての投稿が user のものか'):
            self.assertTrue(all_by(self.post_author, author_posts))

        with self.subTest('他ユーザーでは投稿0'):
            other_user = create_user('not_author')
            self.assertEqual(Post.get_posts(other_user).count(), 0)
            
    def test_get_all_posts(self):
        user2 = create_user('James')
        
        posts = [
            ('Post D', self.post_author), 
            ('Post E', user2), 
            ('Post F', self.post_author), 
            ('Post G', user2)
        ]
        
        # 投稿の作成
        for post, author in posts:
            create_post(author, post)
        
        posts = Post.get_posts()
        self.assertEqual(posts.count(), 4)