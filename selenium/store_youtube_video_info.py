def store_video_details(videoDetails, title, description, embed_url, published_at, e_tag, k):
    # append the following items to videoDetails dictionary
    videoDetails["{} vid_title".format(k)] = title
    videoDetails["{} e_tag".format(k)] = e_tag
    videoDetails["{} description".format(k)] = description
    videoDetails["{} embed_url".format(k)] = embed_url
    videoDetails["{} published_at".format(k)] = published_at
    #the channel title
    videoDetails["{}".format(k)] = k
    return videoDetails


