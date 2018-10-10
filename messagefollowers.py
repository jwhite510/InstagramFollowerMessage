from InstagramAPI import InstagramAPI
import time
import instagramcredentials

# function for get recent followers and their ID
def get_recent_followers(api):
    api.getRecentActivity()
    new_stories = api.LastJson['new_stories']
    people_who_followed = []
    for story in new_stories:

        username = story['args']['inline_follow']['user_info']['username']
        story_type = story['story_type']
        text = story['args']['text']
        profile_id = story['args']['profile_id']

        # make sure its a follow
        if "started following you." in text and story_type == 101:
            people_who_followed.append({'profile_id': profile_id, 'username': username})


    return people_who_followed


def message_user(api, message, user):

    print("messaging user "+user['username'])
    api.direct_message(text=message, recipients=user['profile_id'])



if __name__ == "__main__":

    text="hello! thanks for following"

    api = InstagramAPI(instagramcredentials.username, instagramcredentials.password)
    api.login()

    # get the initial recent followers
    dont_message_these_people = get_recent_followers(api)

    time_started = time.time()
    while True:

        # check if different people are
        recent_followers = get_recent_followers(api)

        for recent_follower in recent_followers:

            # check if they are in the list of messaged people
            if recent_follower in dont_message_these_people:
                pass

            else:
                # message the person and add them to the dont message list
                message_user(api, message=text, user=recent_follower)
                dont_message_these_people.append(recent_follower)

        time.sleep(2)

        elapsed = time.time() - time_started

        if elapsed > 8 * 60 * 60:
            # every 8 hours reset the dont message list
            dont_message_these_people = get_recent_followers(api)
            time_started = time.time()

