import os
import json

#Convert relative to absolute paths to avoid conflict in crontab
script_path = os.path.abspath(__file__)  # i.e. /path/to/whatever
script_dir = os.path.split(script_path)[0]  #i.e. /path/to/whatever


def check_e_tag_compare_title(CHANNEL_TITLE, e_tag, title):
    videoDetailsAlreadyStored = False
    youtubeJson = script_dir + '/json/youtubeinfo.json'
    #if the file is blank, the video hasnt been stored.
    if os.stat(youtubeJson).st_size == 0:
        videoDetailsAlreadyStored = False

    else:
        with open(script_dir + '/json/youtubeinfo.json', 'r') as readfile:

            storedInfo = json.load(readfile)
            #if storedInfo is an empty dict, the video hasn't bene stored.
            if storedInfo == {}:
                videoDetailsAlreadyStored = False

            #if the key exists and doesn't have a null value
            if title is not None and "{} vid_title".format(CHANNEL_TITLE) in storedInfo:

                if storedInfo["{} vid_title".format(CHANNEL_TITLE)] == title:
                    videoDetailsAlreadyStored = True

            elif e_tag is not None and "{} e_tag".format(CHANNEL_TITLE) in storedInfo:
                # Check if e_tag matches the stored e_tag
                if storedInfo["{} e_tag".format(CHANNEL_TITLE)] == e_tag:
                    videoDetailsAlreadyStored = True

            else:
                # print("else statement in e-tag activated")
                videoDetailsAlreadyStored = False
    # print("return videoDetails frmo CheckEtag")
    return videoDetailsAlreadyStored

