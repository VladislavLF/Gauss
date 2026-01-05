import os
import sys
import django
import random
import time
from datetime import datetime, timedelta


sys.path.append('/app')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gauss.settings')

max_retries = 30
retry_delay = 2

for i in range(max_retries):
    try:
        django.setup()
        from django.db import connection

        connection.ensure_connection()
        print("Database connection established")
        break
    except Exception as e:
        if i < max_retries - 1:
            print(f"Waiting for database connection... ({i + 1}/{max_retries})")
            time.sleep(retry_delay)
        else:
            print(f"Failed to connect to database: {e}")
            sys.exit(1)

from django.contrib.auth.models import User
from tasks.models import (
    Category_Tasks, Category_Tasks_Filter, Task,
    Category_Options, Theory_category, Theory_item, Comment
)


def clear_database():
    clear_db = os.environ.get('CLEAR_DB_ON_STARTUP', 'false').lower()
    if clear_db not in ['true', '1', 'yes']:
        return

    print("Clearing database...")
    Comment.objects.all().delete()
    Theory_item.objects.all().delete()
    Theory_category.objects.all().delete()
    Category_Options.objects.all().delete()
    Task.objects.all().delete()
    Category_Tasks_Filter.objects.all().delete()
    Category_Tasks.objects.all().delete()
    User.objects.filter(is_superuser=False).delete()
    print("Database cleared")


def create_superuser():
    if not User.objects.filter(username='admin').exists():
        admin_password = os.environ.get('ADMIN_PASSWORD')
        if not admin_password:
            print("ADMIN_PASSWORD not set")
            return None

        User.objects.create_superuser(
            username='admin',
            email='admin@gauss.net',
            password=admin_password
        )
        print("Superuser created")
        return User.objects.get(username='admin')
    else:
        print("Superuser exists")
        return User.objects.get(username='admin')


def create_test_users():
    users_data = [
        {'username': 'student1', 'email': 'student1@example.com'},
        {'username': 'student2', 'email': 'student2@example.com'},
        {'username': 'teacher', 'email': 'teacher@example.com'},
        {'username': 'demo', 'email': 'demo@example.com'},
    ]

    for user_data in users_data:
        if not User.objects.filter(username=user_data['username']).exists():
            password_var = f"TEST_USER_{user_data['username'].upper()}_PASSWORD"
            password = os.environ.get(password_var, 'testpass123')

            User.objects.create_user(
                username=user_data['username'],
                email=user_data['email'],
                password=password
            )
            print(f"User {user_data['username']} created")


def create_categories():
    categories = []
    for i in range(1, 19):
        if i <= 6:
            difficult = 'basic'
        elif i <= 12:
            difficult = 'intermediate'
        else:
            difficult = 'advanced'
        categories.append({'points': str(i), 'difficult': difficult})

    created = 0
    for i, cat_data in enumerate(categories, 1):
        obj, created_flag = Category_Tasks.objects.get_or_create(
            points=cat_data['points'],
            difficult=cat_data['difficult'],
            defaults={'id': i}
        )
        if created_flag:
            created += 1

    print(f"Created {created} task categories")


def create_filters():
    filters_data = [
        {'name': 'Text Problems', 'slug': 'text-problems', 'cat_id': 1},
        {'name': 'Percentage Problems', 'slug': 'percentage-problems', 'cat_id': 1},
        {'name': 'Motion Problems', 'slug': 'motion-problems', 'cat_id': 1},
        {'name': 'Work Problems', 'slug': 'work-problems', 'cat_id': 1},
        {'name': 'Classical Probability', 'slug': 'classical-probability', 'cat_id': 2},
        {'name': 'Geometric Probability', 'slug': 'geometric-probability', 'cat_id': 2},
        {'name': 'Conditional Probability', 'slug': 'conditional-probability', 'cat_id': 2},
        {'name': 'Triangles', 'slug': 'triangles', 'cat_id': 3},
        {'name': 'Quadrilaterals', 'slug': 'quadrilaterals', 'cat_id': 3},
        {'name': 'Circles', 'slug': 'circles', 'cat_id': 3},
        {'name': 'Polygons', 'slug': 'polygons', 'cat_id': 3},
        {'name': 'Pyramids', 'slug': 'pyramids', 'cat_id': 4},
        {'name': 'Prisms', 'slug': 'prisms', 'cat_id': 4},
        {'name': 'Cylinders', 'slug': 'cylinders', 'cat_id': 4},
        {'name': 'Cones', 'slug': 'cones', 'cat_id': 4},
        {'name': 'Irrational Equations', 'slug': 'irrational-equations', 'cat_id': 5},
        {'name': 'Exponential Equations', 'slug': 'exponential-equations', 'cat_id': 5},
        {'name': 'Logarithmic Equations', 'slug': 'logarithmic-equations', 'cat_id': 5},
        {'name': 'Trigonometric Equations', 'slug': 'trigonometric-equations', 'cat_id': 5},
        {'name': 'Polynomials', 'slug': 'polynomials', 'cat_id': 6},
        {'name': 'Rational Expressions', 'slug': 'rational-expressions', 'cat_id': 6},
        {'name': 'Systems of Equations', 'slug': 'systems-of-equations', 'cat_id': 7},
        {'name': 'Inequalities', 'slug': 'inequalities', 'cat_id': 8},
        {'name': 'Functions', 'slug': 'functions', 'cat_id': 9},
        {'name': 'Derivatives', 'slug': 'derivatives', 'cat_id': 10},
        {'name': 'Integrals', 'slug': 'integrals', 'cat_id': 11},
        {'name': 'Limits', 'slug': 'limits', 'cat_id': 12},
        {'name': 'Sequences', 'slug': 'sequences', 'cat_id': 13},
        {'name': 'Series', 'slug': 'series', 'cat_id': 14},
        {'name': 'Vectors', 'slug': 'vectors', 'cat_id': 15},
        {'name': 'Matrices', 'slug': 'matrices', 'cat_id': 16},
        {'name': 'Complex Numbers', 'slug': 'complex-numbers', 'cat_id': 17},
        {'name': 'Statistics', 'slug': 'statistics', 'cat_id': 18},
    ]

    created = 0
    for filter_data in filters_data:
        try:
            cat = Category_Tasks.objects.get(id=filter_data['cat_id'])
            obj, created_flag = Category_Tasks_Filter.objects.get_or_create(
                name=filter_data['name'],
                slug=filter_data['slug'],
                cat=cat
            )
            if created_flag:
                created += 1
        except Category_Tasks.DoesNotExist:
            print(f"Category {filter_data['cat_id']} not found")

    print(f"Created {created} filters")


def create_tasks():
    tasks_data = [
        {
            'condition': 'A train travels from City A to City B at 60 km/h and returns at 40 km/h. What is the average speed for the round trip?',
            'solution': 'Average speed = total distance / total time. Let distance = d. Time forward = d/60, time back = d/40. Total time = d/60 + d/40 = (2d+3d)/120 = 5d/120 = d/24. Total distance = 2d. Average speed = 2d / (d/24) = 48 km/h.',
            'answer': '48',
            'cat_id': 1,
            'filter_slug': 'motion-problems',
        },
        {
            'condition': 'If a number is increased by 20% and then decreased by 20%, what is the net percentage change?',
            'solution': 'Let the number be 100. After 20% increase: 120. After 20% decrease: 120 * 0.8 = 96. Net change = (96-100)/100 * 100% = -4%.',
            'answer': '-4%',
            'cat_id': 1,
            'filter_slug': 'percentage-problems',
        },
        {
            'condition': 'Two dice are rolled. What is the probability that the sum is 7?',
            'solution': 'Total outcomes: 6*6 = 36. Favorable outcomes: (1,6),(2,5),(3,4),(4,3),(5,2),(6,1) = 6. Probability = 6/36 = 1/6.',
            'answer': '1/6',
            'cat_id': 2,
            'filter_slug': 'classical-probability',
        },
        {
            'condition': 'In a triangle ABC, angle A = 60°, angle B = 45°, side a = 10. Find side b.',
            'solution': 'Using Law of Sines: a/sinA = b/sinB. 10/sin60 = b/sin45. 10/(√3/2) = b/(√2/2). b = (10 * √2/2) / (√3/2) = 10√2/√3 = (10√6)/3.',
            'answer': '(10√6)/3',
            'cat_id': 3,
            'filter_slug': 'triangles',
        },
        {
            'condition': 'Find the volume of a pyramid with square base side 6 and height 8.',
            'solution': 'Volume = (1/3) * base area * height = (1/3) * 6^2 * 8 = (1/3) * 36 * 8 = 96.',
            'answer': '96',
            'cat_id': 4,
            'filter_slug': 'pyramids',
        },
        {
            'condition': 'Solve: √(x+3) = x-3',
            'solution': 'Square both sides: x+3 = (x-3)^2 = x^2 -6x +9. Rearrange: x^2 -7x +6 = 0. Roots: x=1 and x=6. Check: x=1 gives √4 = -2 (false). x=6 gives √9 = 3 (true). Answer: x=6.',
            'answer': '6',
            'cat_id': 5,
            'filter_slug': 'irrational-equations',
        },
        {
            'condition': 'Factor: x^2 - 5x + 6',
            'solution': 'Find two numbers that multiply to 6 and add to -5: -2 and -3. So: (x-2)(x-3).',
            'answer': '(x-2)(x-3)',
            'cat_id': 6,
            'filter_slug': 'polynomials',
        },
        {
            'condition': 'Solve the system: x+y=5, 2x-y=1',
            'solution': 'Add equations: 3x=6, x=2. Substitute: 2+y=5, y=3. Solution: (2,3).',
            'answer': '(2,3)',
            'cat_id': 7,
            'filter_slug': 'systems-of-equations',
        },
        {
            'condition': 'Solve inequality: 2x - 3 > 7',
            'solution': '2x > 10, x > 5.',
            'answer': 'x > 5',
            'cat_id': 8,
            'filter_slug': 'inequalities',
        },
        {
            'condition': 'Find domain of f(x) = √(4-x)',
            'solution': '4-x ≥ 0, so x ≤ 4. Domain: (-∞, 4].',
            'answer': '(-∞, 4]',
            'cat_id': 9,
            'filter_slug': 'functions',
        },
        {
            'condition': 'Find derivative of f(x) = 3x^2 + 2x - 1',
            'solution': "f'(x) = 6x + 2.",
            'answer': '6x+2',
            'cat_id': 10,
            'filter_slug': 'derivatives',
        },
        {
            'condition': 'Evaluate ∫(2x dx) from 0 to 3',
            'solution': 'Antiderivative: x^2. Evaluate: 3^2 - 0^2 = 9.',
            'answer': '9',
            'cat_id': 11,
            'filter_slug': 'integrals',
        },
        {
            'condition': 'Find limit: lim(x→2) (x^2 - 4)/(x-2)',
            'solution': 'Factor: (x-2)(x+2)/(x-2) = x+2. Limit = 2+2 = 4.',
            'answer': '4',
            'cat_id': 12,
            'filter_slug': 'limits',
        },
        {
            'condition': 'Find 10th term of arithmetic sequence: 2, 5, 8, ...',
            'solution': 'a1=2, d=3. an = a1 + (n-1)d. a10 = 2 + 9*3 = 29.',
            'answer': '29',
            'cat_id': 13,
            'filter_slug': 'sequences',
        },
        {
            'condition': 'Find sum of geometric series: 3 + 6 + 12 + ... + 192',
            'solution': 'a=3, r=2. Last term 192 = 3*2^(n-1). 2^(n-1)=64, n-1=6, n=7. Sum = a(r^n -1)/(r-1) = 3(128-1)/(2-1) = 381.',
            'answer': '381',
            'cat_id': 14,
            'filter_slug': 'series',
        },
        {
            'condition': 'Find dot product of vectors a=(1,2) and b=(3,4)',
            'solution': 'a·b = 1*3 + 2*4 = 3+8 = 11.',
            'answer': '11',
            'cat_id': 15,
            'filter_slug': 'vectors',
        },
        {
            'condition': 'Multiply matrices: [[1,2],[3,4]] * [[5,6],[7,8]]',
            'solution': 'Result = [[1*5+2*7, 1*6+2*8], [3*5+4*7, 3*6+4*8]] = [[19,22],[43,50]].',
            'answer': '[[19,22],[43,50]]',
            'cat_id': 16,
            'filter_slug': 'matrices',
        },
        {
            'condition': 'Simplify: (3+4i)(2-i)',
            'solution': '= 6 -3i +8i -4i^2 = 6 +5i +4 = 10+5i.',
            'answer': '10+5i',
            'cat_id': 17,
            'filter_slug': 'complex-numbers',
        },
        {
            'condition': 'Find mean of data: 10, 20, 30, 40, 50',
            'solution': 'Sum=150, count=5. Mean=150/5=30.',
            'answer': '30',
            'cat_id': 18,
            'filter_slug': 'statistics',
        },
    ]

    created = 0
    for task_data in tasks_data:
        try:
            cat = Category_Tasks.objects.get(id=task_data['cat_id'])
            filter_obj = Category_Tasks_Filter.objects.get(slug=task_data['filter_slug'])

            if not Task.objects.filter(condition=task_data['condition']).exists():
                task = Task.objects.create(
                    condition=task_data['condition'],
                    solution=task_data['solution'],
                    answer=task_data['answer'],
                    cat=cat,
                    filter=filter_obj,
                    is_published=True
                )
                past_date = datetime.now() - timedelta(days=random.randint(1, 365))
                task.time_create = past_date
                task.time_update = past_date
                task.save()
                created += 1

                if created <= 10:
                    create_comments_for_task(task)
        except (Category_Tasks.DoesNotExist, Category_Tasks_Filter.DoesNotExist) as e:
            print(f"Error creating task: {e}")

    for cat_id in range(1, 19):
        for i in range(5):
            condition = f'Sample task {i + 1} for category {cat_id}. This is a practice problem.'
            solution = f'Step-by-step solution for task {i + 1} in category {cat_id}.'
            answer = f'Answer {i + 1} for category {cat_id}'

            if not Task.objects.filter(condition=condition).exists():
                try:
                    cat = Category_Tasks.objects.get(id=cat_id)
                    filters = Category_Tasks_Filter.objects.filter(cat=cat)
                    filter_obj = filters.first() if filters.exists() else None

                    Task.objects.create(
                        condition=condition,
                        solution=solution,
                        answer=answer,
                        cat=cat,
                        filter=filter_obj,
                        is_published=True
                    )
                    created += 1
                except Category_Tasks.DoesNotExist:
                    pass

    print(f"Created {created} tasks")


def create_comments_for_task(task):
    users = list(User.objects.all())
    if not users:
        return

    comments_text = [
        "This problem helped me understand the concept better.",
        "I solved it differently but got the same answer.",
        "The solution is very clear and detailed.",
        "Could you explain step 2 in more detail?",
        "This type of problem often appears on exams.",
        "Thanks for providing this example.",
        "I initially made a mistake but now I understand.",
        "The explanation is very thorough.",
        "This is a good practice problem.",
        "I shared this with my study group.",
    ]

    for i in range(min(3, len(users))):
        user = users[i]
        text = comments_text[i % len(comments_text)]
        past_date = datetime.now() - timedelta(days=random.randint(1, 30), hours=random.randint(1, 12))

        Comment.objects.get_or_create(
            user=user,
            post=task,
            text=text,
            defaults={
                'is_published': True,
                'created': past_date,
                'updated': past_date,
            }
        )


def create_options():
    tasks = list(Task.objects.filter(is_published=True))

    for variant_num in range(1, 6):
        description = f'Practice Variant {variant_num}'
        difficult = random.choice(['basic', 'intermediate', 'advanced'])

        if not Category_Options.objects.filter(description=description).exists():
            if len(tasks) >= 18:
                option_data = {
                    'description': description,
                    'difficult': difficult,
                    'is_published': True,
                }

                selected_tasks = random.sample(tasks, 18) if len(tasks) >= 18 else tasks[:18]

                for i in range(1, 19):
                    if i - 1 < len(selected_tasks):
                        option_data[f'id_number_{i}'] = str(selected_tasks[i - 1].id)
                    else:
                        option_data[f'id_number_{i}'] = ''

                Category_Options.objects.create(**option_data)
                print(f"Created variant {variant_num}")


def create_theory():
    theory_categories = [
        'Algebra',
        'Geometry',
        'Trigonometry',
        'Probability',
        'Calculus',
        'Statistics',
        'Discrete Mathematics',
        'Number Theory',
    ]

    created_cats = 0
    for cat_name in theory_categories:
        obj, created = Theory_category.objects.get_or_create(category=cat_name)
        if created:
            created_cats += 1

    print(f"Created {created_cats} theory categories")

    theory_items = [
        {'title': 'Quadratic Equations', 'cat_category': 'Algebra'},
        {'title': 'Polynomials', 'cat_category': 'Algebra'},
        {'title': 'Rational Expressions', 'cat_category': 'Algebra'},
        {'title': 'Exponents and Logarithms', 'cat_category': 'Algebra'},
        {'title': 'Triangle Properties', 'cat_category': 'Geometry'},
        {'title': 'Circle Theorems', 'cat_category': 'Geometry'},
        {'title': 'Solid Geometry', 'cat_category': 'Geometry'},
        {'title': 'Coordinate Geometry', 'cat_category': 'Geometry'},
        {'title': 'Trigonometric Functions', 'cat_category': 'Trigonometry'},
        {'title': 'Trigonometric Identities', 'cat_category': 'Trigonometry'},
        {'title': 'Trigonometric Equations', 'cat_category': 'Trigonometry'},
        {'title': 'Basic Probability', 'cat_category': 'Probability'},
        {'title': 'Conditional Probability', 'cat_category': 'Probability'},
        {'title': 'Random Variables', 'cat_category': 'Probability'},
        {'title': 'Limits and Continuity', 'cat_category': 'Calculus'},
        {'title': 'Derivatives', 'cat_category': 'Calculus'},
        {'title': 'Integrals', 'cat_category': 'Calculus'},
        {'title': 'Differential Equations', 'cat_category': 'Calculus'},
        {'title': 'Descriptive Statistics', 'cat_category': 'Statistics'},
        {'title': 'Probability Distributions', 'cat_category': 'Statistics'},
        {'title': 'Hypothesis Testing', 'cat_category': 'Statistics'},
        {'title': 'Sequences and Series', 'cat_category': 'Discrete Mathematics'},
        {'title': 'Combinatorics', 'cat_category': 'Discrete Mathematics'},
        {'title': 'Graph Theory', 'cat_category': 'Discrete Mathematics'},
        {'title': 'Prime Numbers', 'cat_category': 'Number Theory'},
        {'title': 'Modular Arithmetic', 'cat_category': 'Number Theory'},
        {'title': 'Diophantine Equations', 'cat_category': 'Number Theory'},
    ]

    created_items = 0
    for item_data in theory_items:
        try:
            cat = Theory_category.objects.get(category=item_data['cat_category'])
            obj, created = Theory_item.objects.get_or_create(
                title=item_data['title'],
                cat=cat,
                defaults={
                    'is_published': True,
                }
            )
            if created:
                past_date = datetime.now() - timedelta(days=random.randint(1, 180))
                obj.time_create = past_date
                obj.time_update = past_date
                obj.save()
                created_items += 1
        except Theory_category.DoesNotExist:
            print(f"Category {item_data['cat_category']} not found")

    print(f"Created {created_items} theory items")


def main():
    print("Starting content population...")

    populate_content = os.environ.get('POPULATE_CONTENT', 'false').lower()
    if populate_content not in ['true', '1', 'yes']:
        print("POPULATE_CONTENT not set")
        return

    clear_database()

    print("POPULATE_CONTENT set")
    create_superuser()
    create_test_users()
    create_categories()
    create_filters()
    create_tasks()
    create_theory()
    create_options()

    print("Content population completed")
    print(f"   Users: {User.objects.count()}")
    print(f"   Task categories: {Category_Tasks.objects.count()}")
    print(f"   Filters: {Category_Tasks_Filter.objects.count()}")
    print(f"   Tasks: {Task.objects.count()}")
    print(f"   Exam variants: {Category_Options.objects.count()}")
    print(f"   Theory categories: {Theory_category.objects.count()}")
    print(f"   Theory items: {Theory_item.objects.count()}")
    print(f"   Comments: {Comment.objects.count()}")


if __name__ == '__main__':
    main()
