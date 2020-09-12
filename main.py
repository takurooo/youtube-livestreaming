# -----------------------------
# import
# -----------------------------
import os
import json
import time

from apiclient.discovery import build

import user_credentials
import youtube_livebroadcasts
import youtube_livestreams

# -----------------------------
# define
# -----------------------------


# -----------------------------
# function
# -----------------------------
def print_response(response):
    print(json.dumps(response, sort_keys=True, indent=4))

def build_youtube_api(apikey, credentials):
    return build("youtube", "v3", developerKey=apikey, credentials=credentials)

def main():
    apikey = user_credentials.get_apikey()
    credentials = user_credentials.get_credentials()

    youtube = build_youtube_api(apikey, credentials)
    livebroadcasts = youtube_livebroadcasts.API(youtube)
    livestreams = youtube_livestreams.API(youtube)

    #---------------------
    # delete all resource
    #---------------------
    # livestreamsがbroadcastsとbindされている場合、
    # bind先のbroadcastsから削除しないとエラーになる.
    # livebroadcasts.delete_all() 
    # livestreams.delete_all() 

    #---------------------
    # Stage1 Set up your broadcast
    #---------------------

    # Step 1.1 Create your broadcast
    response = livebroadcasts.create(title="Test Live Broadcast", scheduled_start_time="2021-09-10T19:00:00Z")
    # print_response(response)
    embedHtml = response["contentDetails"]["monitorStream"]["embedHtml"]
    livebroadcast_id = response["id"]

    # Step 1.2 Create your stream
    response = livestreams.create(title="Test Live Streams")
    # print_response(response)
    livestream_id = response["id"]
    url = response["cdn"]["ingestionInfo"]["ingestionAddress"]
    stream_name = response["cdn"]["ingestionInfo"]["streamName"]

    # Step 1.3: Bind your broadcast to its stream
    livebroadcasts.bind(livebroadcast_id, livestream_id)    

    #---------------------
    # Stage3 Test
    #---------------------

    # Step 3.2: Start your video
    print()
    print("start transmitting video on your video stream.")
    print("url          : ", url)
    print("stream_name  : ", stream_name)
    print("test monitor html : ", embedHtml)
    input("if you start transmitting video, please enter key...")
    print()

    # Step 3.3: Confirm your video stream is active
    livestreams.wait_for_changing_status(livestream_id, "active", 5)

    # Step 3.4: Transition your broadcast's status to testing
    livebroadcasts.transition_status(livebroadcast_id, "testing")
    livebroadcasts.wait_for_changing_status(livebroadcast_id, "testing", 5)

    print()
    input("test is done. if you start livestreaming video, please enter key...")
    print()

    #---------------------
    # Stage 4: Broadcast
    #---------------------
    # Step 4.1: Start your video
    # Step 4.2: Confirm your video stream is active

    # Step 4.3: Transition your broadcast's status to live
    livebroadcasts.transition_status(livebroadcast_id, "live")
    livebroadcasts.wait_for_changing_status(livebroadcast_id, "live", 5)
    print("Start live streaming!!!")

    #---------------------
    # Stage 5: Conclude your broadcast
    #---------------------

    # Step 5.1: Stop streaming
    print()
    input("if you stop transmitting video, please enter key...")
    print()

    # Step 5.2: Transition your broadcast's status to complete
    livebroadcasts.transition_status(livebroadcast_id, "complete")
    livebroadcasts.wait_for_changing_status(livebroadcast_id, "complete", 5)


if __name__ == "__main__":
    main()