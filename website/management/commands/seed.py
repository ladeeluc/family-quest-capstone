import random
from django.core.management.base import BaseCommand
from familystructure.models import (
    FamilyCircle,
    Person,
    Relation,
)
from socialmedia.models import (
    Post,
    PostReaction,
    Comment,
    CommentReaction,
    CommentNotification,
    Chat,
    Message,
    MessageNotification
)
from useraccount.models import UserAccount

class Command(BaseCommand):
    help = 'Seeds the database with the Doe and Buck families'

    def handle(self, *args, **options):
        dataset = [
            ( # Grandpa
                'Gary',
                'Pops',
                'Harry',
                'Doe',
                'Jr.',
                'The Greatest Grandpa',
                '1923-04-05',
                '2009-10-24',
            ),
            ( # Grandma
                'Gina',
                'Gramgram',
                'Skye',
                'Doe',
                None,
                'The Grammiest Gramma',
                '1921-07-05',
                '2010-01-23',
            ),
            ( # Husband
                'John',
                None,
                'Charles',
                'Doe',
                None,
                'The center of the tree',
                '1958-11-12',
                None,
            ),
            ( # Wife
                'Jane',
                None,
                'Belle',
                'Doe',
                None,
                'Loving wife to John',
                '1956-12-29',
                None,
            ),
            ( # Son
                'Bill',
                'Billy',
                'Harris',
                'Doe',
                None,
                'Mischief Maker',
                '1998-03-15',
                None,
            ),
            ( # Son's Wife
                'Betsy',
                'Bea',
                'Christine',
                'Doe',
                None,
                'Tagline',
                '1999-09-27',
                None,
            ),
            ( # Granddaughter
                'Sally',
                None,
                'Victoria',
                'Doe',
                None,
                'The Precious Child',
                '2020-03-22',
                None,
            ),
            ( # Grandson
                'Samuel',
                'Sam',
                'James',
                'Doe',
                None,
                'Yeah, he is born in the future',
                '2022-09-01',
                None,
            ),
            ( # Daughter
                'Jill',
                None,
                'Reece',
                'Doe',
                None,
                'Certified Girl Boss',
                '1992-10-31',
                None,
            ),
            ( # Wife's Brother / Uncle
                'Peter',
                'Pete',
                'Xavier',
                'Buck',
                None,
                'Coach Buck',
                '1954-02-28',
                None,
            ),
            ( # Aunt
                'Patty',
                None,
                'Lisa',
                'Buck',
                None,
                'Accountant at BigBank',
                '1953-05-27',
                None,
            ),
            ( # Cousin
                'Timothy',
                'Timmy',
                'Jackson',
                'Buck',
                None,
                'Mischief Maker\'s Sidekick',
                '1998-05-12',
                None,
            ),
            ( # Other Grandpa
                'Albert',
                None,
                'Jeffery',
                'Buck',
                'III',
                'Still kickin\'',
                '1920-03-19',
                None,
            ),
            ( # Other Grandma
                'Angela',
                'Angie',
                'May',
                'Buck',
                None,
                'May she RIP',
                '1921-01-08',
                '2011-04-15',
            ),
        ]
        # Make UserAccounts and People
        
        people = []
        accounts = []
        for first, nick, middle, last, title, tagline, birth, death in dataset:
            make_user = random.choice((True, False))
            person = Person.objects.create(
                first_name=first,
                nickname=nick,
                middle_name=middle,
                last_name=last,
                title=title,
                tagline=tagline,
                birth_date=birth,
                death_date=death,
                is_claimed=make_user,
            )
            people.append(person)
            if make_user:
                account = UserAccount.objects.create_user(
                    email=f'{first.lower()}.{last.lower()}@familyquest.com',
                    password='familyquest',
                    person=person,
                )
                accounts.append(account)
        
        # Make Relations between People
        Gary, Gina, John, Jane, Bill, Betsy, Sally, Samuel, Jill, Peter, Patty, Timothy, Albert, Angela = people

        # Gary and Gina are Married
        Relation.objects.create(source=Gary, target=Gina, is_upward=False)

        # Gary and Gina had John
        Relation.objects.create(source=John, target=Gary, is_upward=True)
        Relation.objects.create(source=John, target=Gina, is_upward=True)

        # John married Jane
        Relation.objects.create(source=John, target=Jane, is_upward=False)

        # They had Bill and Jill
        Relation.objects.create(source=Bill, target=John, is_upward=True)
        Relation.objects.create(source=Bill, target=Jane, is_upward=True)
        Relation.objects.create(source=Jill, target=John, is_upward=True)
        Relation.objects.create(source=Jill, target=Jane, is_upward=True)

        # Bill married Betsy
        Relation.objects.create(source=Bill, target=Betsy, is_upward=False)

        # They had Sally and Samuel
        Relation.objects.create(source=Sally, target=Bill, is_upward=True)
        Relation.objects.create(source=Sally, target=Betsy, is_upward=True)
        Relation.objects.create(source=Samuel, target=Bill, is_upward=True)
        Relation.objects.create(source=Samuel, target=Betsy, is_upward=True)

        # Jane's brother is Peter, their parents are Albert and Angela
        Relation.objects.create(source=Jane, target=Albert, is_upward=True)
        Relation.objects.create(source=Jane, target=Angela, is_upward=True)
        Relation.objects.create(source=Peter, target=Albert, is_upward=True)
        Relation.objects.create(source=Peter, target=Angela, is_upward=True)

        # Of course Albert and Angela are married
        Relation.objects.create(source=Albert, target=Angela, is_upward=False)

        # Peter has a wife, Patty
        Relation.objects.create(source=Peter, target=Patty, is_upward=False)

        # They have a son, Timothy
        Relation.objects.create(source=Timothy, target=Peter, is_upward=True)
        Relation.objects.create(source=Timothy, target=Patty, is_upward=True)

        # Make family circles
        doe_family = FamilyCircle.objects.create(
            name='Doe Family',
        )
        for m in [Gary, Gina, John, Jane, Bill, Betsy, Sally, Samuel, Jill]:
            doe_family.members.add(m)
            if doe_family.managers.count() == 0:
                try:
                    doe_family.managers.add(m.useraccount)
                except Person.useraccount.RelatedObjectDoesNotExist:
                    pass


        buck_family = FamilyCircle.objects.create(
            name='The Bucks',
        )
        for m in [Albert, Angela, Peter, Patty, Timothy, Jill]:
            buck_family.members.add(m)
            if buck_family.managers.count() == 0:
                try:
                    buck_family.managers.add(m.useraccount)
                except Person.useraccount.RelatedObjectDoesNotExist:
                    pass

        # Spam social media post stuff

        for member in doe_family.members.all():
            members = doe_family.members.all()
            staff = doe_family.managers.all()
            try:
                if member.is_claimed and member.useraccount not in staff:
                    post = Post.objects.create(
                        title='Hello Doe Family!',
                        content=f'Hi my name is {member}',
                        author=member.useraccount,
                        family_circle=doe_family,
                    )
                    PostReaction.objects.create(
                        reaction_type=PostReaction.ReactionType.THUMBS_UP,
                        reactor=staff[0],
                        target_post=post,
                    )
                    reactors = random.choices(list(doe_family.members.filter(is_claimed=True)), k=random.randint(0,10))
                    for reactor in reactors:
                        PostReaction.objects.create(
                            reaction_type=random.choice(PostReaction.ReactionType.values),
                            reactor=reactor.useraccount,
                            target_post=post,
                        )
                    comment = Comment.objects.create(
                        body='Hi! I manage this family circle. Let me know if you need anything.',
                        author=staff[0],
                        commented_on=post,
                    )
                    CommentNotification.objects.create(
                        target_user=member.useraccount,
                        target_comment=comment,
                    )
                    CommentReaction.objects.create(
                        reaction_type=CommentReaction.ReactionType.HEART,
                        reactor=random.choice(members).useraccount,
                        target_comment=comment,
                    )
                    Comment.objects.create(
                        body='Awesome!',
                        author=random.choice(members).useraccount,
                        commented_on=post,
                    )
            except Person.useraccount.RelatedObjectDoesNotExist:
                    pass

        
        for member in buck_family.members.all():
            members = buck_family.members.all()
            staff = buck_family.managers.all()
            try:
                if member.is_claimed and member.useraccount not in staff:
                    post = Post.objects.create(
                        title='Howdy Buck Family!',
                        content=f'Hi my name is {member}',
                        author=member.useraccount,
                        family_circle=buck_family,
                    )
                    PostReaction.objects.create(
                        reaction_type=PostReaction.ReactionType.THUMBS_UP,
                        reactor=staff[0],
                        target_post=post,
                    )
                    reactors = random.choices(list(buck_family.members.filter(is_claimed=True)), k=random.randint(0,10))
                    for reactor in reactors:
                        PostReaction.objects.create(
                            reaction_type=random.choice(PostReaction.ReactionType.choices),
                            reactor=reactor.useraccount,
                            target_post=post,
                        )
                    comment = Comment.objects.create(
                        body='Hi! I manage this family circle. Let me know if you need anything.',
                        author=staff[0],
                        commented_on=post,
                    )
                    CommentNotification.objects.create(
                        target_user=member.useraccount,
                        target_comment=comment,
                    )
                    CommentReaction.objects.create(
                        reaction_type=CommentReaction.ReactionType.HEART,
                        reactor=random.choice(members).useraccount,
                        target_comment=comment,
                    )
                    Comment.objects.create(
                        body='Awesome!',
                        author=random.choice(members).useraccount,
                        commented_on=post,
                    )
            except Person.useraccount.RelatedObjectDoesNotExist:
                    pass
        
        
        anyone = UserAccount.objects.all()
        text_chars = 'abcdefghijklmnopqrstuvwxyz            '

        # Spam some DMs
        for _ in range(15):
            acc1 = random.choice(anyone)
            acc2 = random.choice(anyone)
            if acc1 != acc2:
                chat = Chat.objects.create()
                chat.members.add(acc1)
                chat.members.add(acc2)
                for _ in range(20):
                    author = random.choice([acc1, acc2])
                    if author == acc1:
                        recipient = acc2
                    else:
                        recipient = acc1
                    message = Message.objects.create(
                        content=''.join(random.choices(text_chars, k=random.choice(range(1,100)))),
                        chat=chat,
                        author=author,
                    )
                    MessageNotification.objects.create(
                        target_user=recipient,
                        target_message=message,
                    )
        
        # Spam some comments
        for _ in range(20):
            author = random.choice(anyone)
            family_circle = random.choice(author.person.family_circles.all())
            posts = Post.objects.filter(family_circle=family_circle)
            post = random.choice(posts)
            comment = Comment.objects.create(
                body=''.join(random.choices(text_chars, k=random.choice(range(1,100)))),
                author=author,
                commented_on=post,
            )

            reactors = random.choices(family_circle.members.filter(is_claimed=True), k=random.randint(0,10))
            for reactor in reactors:
                CommentReaction.objects.create(
                    reaction_type=random.choice(CommentReaction.ReactionType.values),
                    reactor=reactor.useraccount,
                    target_comment=comment,
                )
                    
        self.stdout.write(self.style.SUCCESS('Successfully seeded the database'))
