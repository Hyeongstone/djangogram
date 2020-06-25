from django.db import models
from djangogram.users import models as user_model

# Create your models here.

# 클래스마다 만들어주기 번거로우니 따로 만들어 상속
# 데이터 생성날짜와 업데이트 날짜
class TimeStampedModel(models.Model):
    create_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True)
    
    # Meta를 만들 시 TimeStampedModel은 단독으로 테이블 생성 X
    class Meta:
        abstract = True

#사진 저장(게시물)
class Post(TimeStampedModel):
    author = models.ForeignKey(
                user_model.User,
                null = True,
                #on_delete = 외래키를 갖는 USER가 사라지면 어떻게 처리될것인가
                on_delete=models.CASCADE,
                related_name = 'post_author'
            )
    image = models.ImageField(blank = True)
    caption = models.TextField(blank = True)
    image_likes = models.ManyToManyField(
                    user_model.User,
                    related_name = 'post_image_likes'
                )

# 댓글 관리
class Comment(TimeStampedModel):
    author = models.ForeignKey(
            user_model.User,
            null = True,
            #on_delete = 외래키를 갖는 USER가 사라지면 어떻게 처리될것인가
            on_delete=models.CASCADE,
            related_name = 'comment_author'
        )
    posts = models.ForeignKey(
            Post,
            null = True,
            #on_delete = 외래키를 갖는 USER가 사라지면 어떻게 처리될것인가
            on_delete=models.CASCADE,
            related_name = 'comment_post'
        )
    contents = models.TextField(blank=True)