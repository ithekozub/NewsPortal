from django.contrib.auth.models import User
from NewsPaper.models import *

user1 = User.objects.create_user(username='Петр Первый', password='qwerty')
user2 = User.objects.create_user(username='Василий Иванович', password='abc123')

author1 = Author.objects.create(author=user1)
author2 = Author.objects.create(author=user2)

cat1 = Category.objects.create(name='Политика')
cat2 = Category.objects.create(name='Бизнес')
cat3 = Category.objects.create(name='Общество')
cat4 = Category.objects.create(name='Культура')

post1 = Post.objects.create(author=author1, type = 'AR', title= 'Учеба со слезами на глазах: почему россияне не хотят поступать в вузы', text='Обучение в высших учебных заведениях за последние годы утратило свою престижность: согласно исследованию Superjob, проведенному в этом году, дети 43% опрошенных родителей отправятся после школы в вуз — в то время как в 2010 году этот показатель составил 80%. Как объясняют сами молодые россияне, они не видят смысла в учебе. Эксперты при этом отмечают новую тенденцию в отношении россиян к вузам: как оказалось, теперь большую ценность имеет отложенное высшее образование, которое люди получают, уже имея профессию.')

post2 = Post.objects.create(author=author2, type = 'AR', title= 'Врач за 8 млн рублей: роботов отправят в «красную» зону', text='В России приступили к созданию робота, который заменит медиков в «красных» зонах COVID-19. Он будет выглядеть как платформа на колесах с рукой-манипулятором — устройство сможет брать кровь, мазок со слизистой пациента, слушать его легкие, делать УЗИ, приносить еду в палату и даже спрашивать о самочувствии больного. По оценкам инженеров, один такой робот будет стоить 8 млн рублей. «Газета.Ru» рассказывает, как машины помогают бороться с COVID-19 в разных странах..')

post3 = Post.objects.create(author=author2, type = 'NW', title= 'Суэц открыт: судно Ever Given сдвинули с мертвой точки', text='Контейнеровоз Ever Given смогли частично снять с мели. По словам представителя управления Суэцкого канала, этому помогло полнолуние и сильный прилив. Сейчас судно планируется частично разгрузить, оно может идти своим ходом. Канал теперь будет работать для пропуска оказавшихся в морском заторе судов круглосуточно.')

post1.category.add(cat4)
post2.category.add(cat2)
post3.category.add(cat2)
post3.category.add(cat3)

comment1 = Comment.objects.create(post=post1, user=user1, text='Я тоже плачу когда учусь(((')
comment2 = Comment.objects.create(post=post1, user=user2, text='Учиться нужно только в SkillFactory, никаких ВУЗОВ!')
comment3 = Comment.objects.create(post=post2, user=user1, text='Роботы рулят...')
comment4 = Comment.objects.create(post=post3, user=user2, text='О наконецто!')

post1.like()
post2.like()
post1.like()
post1.like()
post3.like()
post1.like()
post1.dislike()
post3.dislike()
comment1.like()
comment1.dislike()
comment1.like()
comment2.like()
comment2.dislike()
comment2.like()
comment2.like()
comment2.like()
comment3.like()
comment4.like()
comment4.like()
comment4.like()
comment4.like()
comment4.like()
comment4.dislike()
comment4.like()

author1.update_rating()
author2.update_rating()

best_author = Author.objects.all().order_by('-rating').values('author__username','rating')[0]
best_author
best_post_id = Post.objects.all().order_by('-rating').values('id')[0].get('id')
best_post = Post.objects.get(id=best_post_id)
best_post.post_time
best_post.author.author
best_post.rating
best_post.title
best_post.preview()

Comment.objects.filter(post=best_post).values('comment_time', 'user', 'rating', 'text')