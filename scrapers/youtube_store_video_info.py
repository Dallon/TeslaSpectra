def store_video_details(videoDetails, title, description, embed_url, published_at, e_tag, k):
    # append the following items to videoDetails dictionary
    videoDetails["{} vid_title".format(k)] = title
    videoDetails["{} e_tag".format(k)] = e_tag
    videoDetails["{} description".format(k)] = description

    if "-nocookie" not in embed_url:
        videoDetails["{} embed_url".format(k)] = embed_url[0:19] + "-nocookie" + embed_url[19:]
    elif "-nocookie-nocookie" in embed_url:
        videoDetails["{} embed_url".format(k)] = embed_url[0:19] + "-nocookie" + embed_url[29:]
    else:
        videoDetails["{} embed_url".format(k)] = embed_url
        #the channel title
    videoDetails["{} published_at".format(k)] = str(published_at)
    videoDetails["{}".format(k)] = k
    return videoDetails



