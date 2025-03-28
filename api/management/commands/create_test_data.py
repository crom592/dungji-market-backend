from django.core.management.base import BaseCommand
from django.utils.text import slugify
from api.models import Category, Product, GroupBuy, User

class Command(BaseCommand):
    help = 'Creates test data for the Dungji Market'

    def handle(self, *args, **kwargs):
        # Clear existing data
        self.stdout.write('Clearing existing data...')
        GroupBuy.objects.all().delete()
        Product.objects.all().delete()
        Category.objects.all().delete()

        # Create test categories
        self.stdout.write('Creating categories...')
        
        # Main categories
        electronics = Category.objects.create(name='전자기기', slug='electronics')
        fashion = Category.objects.create(name='패션', slug='fashion')
        food = Category.objects.create(name='식품', slug='food')
        
        # Subcategories
        smartphones = Category.objects.create(name='스마트폰', slug='smartphones', parent=electronics)
        laptops = Category.objects.create(name='노트북', slug='laptops', parent=electronics)
        clothes = Category.objects.create(name='의류', slug='clothes', parent=fashion)
        shoes = Category.objects.create(name='신발', slug='shoes', parent=fashion)
        fruits = Category.objects.create(name='과일', slug='fruits', parent=food)
        vegetables = Category.objects.create(name='채소', slug='vegetables', parent=food)

        # Create test products
        self.stdout.write('Creating products...')
        
        products = [
            Product(
                name='아이폰 15 Pro',
                slug=slugify('아이폰 15 Pro'),
                description='어디서나 등장하는 프로급 성능과 디자인. 새로운 티타늄 디자인과 A17 Pro 칩으로 업그레이드된 아이폰 15 Pro.',
                category=smartphones,
                product_type='device',
                base_price=1500000,
                image_url='https://example.com/iphone15.jpg',
                is_available=True
            ),
            Product(
                name='갤럭시 S24 Ultra',
                slug=slugify('갤럭시 S24 Ultra'),
                description='삼성의 최신 플래그십 스마트폰. Galaxy AI를 탑재한 혁신적인 기능들과 함께.',
                category=smartphones,
                product_type='device',
                base_price=1700000,
                image_url='https://example.com/s24.jpg',
                is_available=True
            ),
            Product(
                name='맥북 프로 M3',
                slug=slugify('맥북 프로 M3'),
                description='M3 칩으로 더욱 강력해진 맥북 프로. 전문가를 위한 최고의 성능과 휘러난 배터리 지속시간.',
                category=laptops,
                product_type='device',
                base_price=2500000,
                image_url='https://example.com/macbook.jpg',
                is_available=True
            ),
            Product(
                name='노스페이스 패딩',
                slug=slugify('노스페이스 패딩'),
                description='최고의 따뜻함과 스타일을 동시에. 겨울을 따뜻하게 날 수 있는 노스페이스의 인기 패딩.',
                category=clothes,
                product_type='device',
                base_price=300000,
                image_url='https://example.com/padding.jpg',
                is_available=True
            ),
        ]
        
        Product.objects.bulk_create(products)

        # Create test user if not exists
        user = User.objects.filter(username='test@example.com').first()
        if not user:
            user = User.objects.create_user(
                username='test@example.com',
                email='test@example.com',
                password='testpassword123',
                first_name='Test User',
                role='buyer'
            )
            user.phone_number = '010-1234-5678'
            user.save()
        
        print(f'User type: {type(user)}')
        print(f'User instance: {user}')
        print(f'Is User instance: {isinstance(user, User)}')
        print(f'User class: {User}')

        # Create test group buys
        self.stdout.write('Creating group buys...')
        
        from django.utils import timezone
        from datetime import timedelta
        
        now = timezone.now()
        
        # Get or create organizer user
        organizer = User.objects.filter(username='organizer@example.com').first()
        if not organizer:
            organizer = User.objects.create_user(
                username='organizer@example.com',
                email='organizer@example.com',
                password='testpassword123',
                first_name='공구장',
                role='seller'
            )
        
        # Create active group buys for all products with different statuses and progress
        group_buys = [
            # 아이폰 공구 - 곧 마감
            GroupBuy.objects.create(
                product=products[0],
                creator=organizer,
                min_participants=3,
                max_participants=10,
                current_participants=8,  # 거의 마감
                end_time=now + timedelta(hours=12),  # 12시간 후 마감
                target_price=1300000,  # 20만원 할인
                status='recruiting'
            ),
            # 갤럭시 공구 - 방금 시작
            GroupBuy.objects.create(
                product=products[1],
                creator=organizer,
                min_participants=5,
                max_participants=15,
                current_participants=2,  # 시작 단계
                end_time=now + timedelta(days=7),  # 7일 후 마감
                target_price=1500000,  # 20만원 할인
                status='recruiting'
            ),
            # 맥북 공구 - 중간 단계
            GroupBuy.objects.create(
                product=products[2],
                creator=organizer,
                min_participants=4,
                max_participants=12,
                current_participants=5,  # 중간 정도 참여
                end_time=now + timedelta(days=3),  # 3일 후 마감
                target_price=2200000,  # 30만원 할인
                status='recruiting'
            ),
            # 패딩 공구 - 성공 직전
            GroupBuy.objects.create(
                product=products[3],
                creator=organizer,
                min_participants=5,
                max_participants=20,
                current_participants=18,  # 거의 마감
                end_time=now + timedelta(days=5),  # 5일 후 마감
                target_price=250000,  # 5만원 할인
                status='recruiting'
            )
        ]

        # Add some participants to the group buys
        for i, group_buy in enumerate(group_buys):
            # Add the test user as a participant to first two group buys
            if i < 2:
                group_buy.participants.add(user)

        self.stdout.write(self.style.SUCCESS('Successfully created test data'))
