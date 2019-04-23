import argparse
import re

from instabot import Bot


def find_references(text):
    mask = '(?:^|[^\w])(?:@)([A-Za-z0-9_](?:(?:[A-Za-z0-9_]|(?:\.(?!\.))){0,28}(?:[A-Za-z0-9_]))?)' # https://stackoverflow.com/questions/32543090/instagram-username-regex-php
    usernames = re.findall(mask, text)

    return usernames

def is_user_exist(bot, username):
    user_id = bot.get_user_id_from_username(username)
    
    return user_id is not None


def main():
    fulfilled_condidions_users = []

    parser = argparse.ArgumentParser(description='This program helps you choose the winner of the contest in Instagram')
    parser.add_argument('login')
    parser.add_argument('password')
    parser.add_argument('public_username')
    parser.add_argument('post_url')
    args = parser.parse_args()
    login = args.login
    password = args.password
    public_username = args.public_username
    post_url = args.post_url
    
    bot = Bot()
    bot.login(username=login, password=password)
    post_id = bot.get_media_id_from_link(post_url)
    all_post_likers = bot.get_media_likers(post_id)
    all_public_followers = bot.get_user_followers(public_username)
    all_comments = bot.get_media_comments_all(post_id)

    for comment in all_comments:
        usernames = find_references(comment['text'])
        participant = False
        for username in usernames:
            if is_user_exist(bot, username):
                participant = True
        if not str(comment['user']['pk']) in all_post_likers:
            participant = False
        if not str(comment['user']['pk']) in all_public_followers:
            participant = False

        if participant:
            fulfilled_condidions_users.append((
                comment['user']['pk'],
                comment['user']['username'],
            ))

    print(set(fulfilled_condidions_users))


if __name__ == "__main__":
    main()