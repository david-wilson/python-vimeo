#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2009 Marc Poulhiès
#
# Python module for Vimeo
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Plopifier.  If not, see <http://www.gnu.org/licenses/>.


"""
This is an upload script for Vimeo using its v2 API
"""


import vimeo
import vimeo.config
import sys
import optparse

def main(argv):
    parser = optparse.OptionParser(
        usage='Usage: %prog [options]',
        description="Simple Vimeo uploader")

    # auth/appli stuff
    parser.add_option('-k', '--key',
                      help="Consumer key")
    parser.add_option('-s', '--secret',
                      help="Consumer secret")
    parser.add_option('-t', '--access-token',
                      help="Access token")
    parser.add_option('-y', '--access-token-secret',
                      help="Access token secret")

    parser.add_option('--album', metavar="ALBUM_ID",
                      action="append",
                      help="Specify on which album other commands act."
                           +"Can be used more than once")
    parser.add_option('--group', metavar="GROUP_ID",
                      action="append",
                      help="Specify on which group other commands act."
                           +"Can be used more than once")
    parser.add_option('--channel', metavar="CHANNEL_ID",
                      action="append",
                      help="Specify on which channel other commands act."
                           +"Can be used more than once")
    parser.add_option('--video', metavar="VIDEO_ID",
                      action="append",
                      help="Specify on which video other command acts."
                           +"Can be used more than once")
    parser.add_option('--user', metavar="USER_ID",
                      action="append",
                      help="Specify on which user other command acts."
                           +"Can be used more than once")

    parser.add_option('--quota',
                      help="Get user quota", action="store_true", default=False)

    parser.add_option('--get-groups',
                      help="Get all public groups", action="store_true", default=False)
    parser.add_option('--get-group-files',
                      help="Get list of files for the GROUP_ID", 
                      action="store_true",
                      default=False)
    parser.add_option('--get-group-info',
                      help="Get information of the GROUP_ID", 
                      action="store_true",
                      default=False)
    parser.add_option('--get-group-members',
                      help="Get the members of the GROUP_ID", 
                      action="store_true",
                      default=False)
    parser.add_option('--get-group-video-comments',
                      help="Get a list of the comments for VIDEO_ID in GROUP_ID", 
                      action="store_true",
                      default=False)
    
    parser.add_option('--get-channels',
                      help="Get all public channels", action="store_true", default=False)
    parser.add_option('--get-channel-info',
                      help="Get info on channel CHANNEL_ID",
                      action="store_true")

    parser.add_option('--get-video-info',
                      help="Get info on video VIDEO_ID",
                      action="store_true")

    parser.add_option('--page', metavar="NUM",
                      help="Page number, when it makes sense...")
    parser.add_option('--per-page', metavar="NUM",
                      help="Per page number, when it makes sense...")
    parser.add_option('--sort', metavar="SORT_ID",
                      help="sort order, when it makes sense (accepted values depends on the query)...")
    parser.add_option('--get-channel-moderators',
                      help="Get moderators for channel CHANNEL_ID",
                      action="store_true")
    parser.add_option('--get-channel-subscribers',
                      help="Get subscribers for channel CHANNEL_ID",
                      action="store_true")
    parser.add_option('--get-channel-videos',
                      help="Get videos for channel CHANNEL_ID using the sort SORT_ID",
                      action="store_true")
    parser.add_option('--get-contacts',
                      help="Get all contacts for user USER_ID",
                      action="store_true")
    parser.add_option('--get-mutual-contacts',
                      help="Get the mutual contacts for USER_ID",
                      action="store_true")
    parser.add_option('--get-online-contacts',
                      help="Get the user's online contacts",
                      action="store_true")
    parser.add_option('--get-who-added-contacts',
                      help="Get the contacts who added USER_ID as a contact",
                      action="store_true")

    parser.add_option('--add-video',
                      help="Add the video VIDEO_ID to the album ALBUM_ID and channel" +
                           "CHANNEL_ID.",
                      action="store_true")

    parser.add_option('--remove-video', 
                      help="Remove the video ViDEO_ID from the album ALBUM_ID and channel" +
                           "CHANNEL_ID.",
                      action="store_true")

    parser.add_option('--set-album-description', metavar='DESCRIPTION',
                      help="Set the description for the album ALBUM_ID")

    parser.add_option('--set-channel-description', metavar='DESCRIPTION',
                      help="Set the description for the channel CHANNEL_ID")

    parser.add_option('--set-password', metavar='PASSWORD',
                      help="Set the password for the channel(s), album(s) and video(s) specified with --channel, --album and --video")
    

    (options, args) = parser.parse_args(argv[1:])

    def check_user():
        return options.user != None

    def check_channel():
        return options.channel != None

    def check_video():
	return options.video != None

    def check_group():
        return options.group != None
            
    def check_album():
        return options.album != None

    vconfig = vimeo.config.VimeoConfig(options)

    if not vconfig.has_option("appli", "consumer_key"):
        print "Missing consumer key"
        parser.print_help()
        sys.exit(-1)

    if not vconfig.has_option("appli", "consumer_secret"):
        print "Missing consumer secret"
        parser.print_help()
        sys.exit(-1)

    client = vimeo.VimeoClient(vconfig.get("appli", "consumer_key"),
                               vconfig.get("appli", "consumer_secret"),
                               token=vconfig.get("auth","token"),
                               token_secret=vconfig.get("auth", "token_secret"),
                               format="json")

    if options.quota:
        quota = client.vimeo_videos_upload_getQuota()['upload_space']['free']
        print "Your current quota is", int(quota)/(1024*1024), "MiB"

    elif options.get_channels:
        channels = client.vimeo_channels_getAll(page=options.page,
                                                sort=options.sort,
                                                per_page=options.per_page)
        if channels['perpage'] == "1":
            print "Name (%s):" % channels['channel']['id'], channels['channel']['name']
        else:
            for channel in channels["channel"]:
                print "Name (%s):" % channel['id'], channel['name']
    
    elif options.get_channel_info :
        if not check_channel():
            print "Missing channel"
            parser.print_help()
            sys.exit(-1)
        for chan in options.channel:
            info = client.vimeo_channels_getInfo(channel_id=chan)

            for text_item in ['name', 'description', 'created_on', 'modified_on', 'total_videos',
                              'total_subscribers', 'logo_url', 'badge_url', 'url', 'featured_description']:
                          
                it = info.get(text_item)
                if it:
                    print "%s:" %text_item, info.get(text_item)
            creator = info['creator']
            print "Creator: %s (%s)" %(creator['display_name'], creator['id'])
       
    elif options.get_video_info:
        if not check_video():
            print "Missing video"
            parser.print_help()
            sys.exit(-1)

        for vid in options.video:
            info = client.vimeo_videos_getInfo(video_id=vid)
            ## TODO pretty print results ?
            pprint.pprint(info)
    
    elif options.get_channel_moderators:
        if not check_channel():
            print "Missing channel"
            parser.print_help()
            sys.exit(-1)

        for chan in options.channel:
            moderators = client.vimeo_channels_getModerators(channel_id=chan,
                                                             page=options.page,
                                                             per_page=options.per_page)

            if moderators['perpage'] == "1":
                print "Name: %s (%s)" %(moderators['user']['display_name'], moderators['user']['id'])
            else:
                for moderator in moderators['user']:
                    print "Name: %s (%s)" %(moderator['display_name'], moderator['id'])

    elif options.get_channel_subscribers:
        if not check_channel():
            print "Missing channel"
            parser.print_help()
            sys.exit(-1)

        for chan in options.channel:
            subs = client.vimeo_channels_getSubscribers(channel_id=chan,
                                                        page=options.page,
                                                        per_page=options.per_page)
            if subs['perpage'] == "1":
                print "Name: %s (%s)" %(subs['subscriber']['display_name'], subs['subscriber']['id'])
            else:
                for sub in subs['subscriber']:
                    print "Name: %s (%s)" %(sub['display_name'], sub['id'])

    elif options.get_channel_videos:
        if not check_channel():
            print "Missing channel"
            parser.print_help()
            sys.exit(-1)

        for chan in options.channel:
            vids = client.vimeo_channels_getVideos(channel_id=chan,
                                                   page=options.page,
                                                   per_page=options.per_page)

            ## Here, no need to check per-page, it always returns a list ?!
            for vid in vids['video']:
                print "Video: %s (%s), uploaded %s" %(vid['title'], 
                                                      vid['id'], 
                                                      vid['upload_date'])
    elif options.get_contacts:
        if not check_user():
            print "Missing user"
            parser.print_help()
            sys.exit(-1)

        for user in options.user:
            contacts = client.vimeo_contacts_getAll(user_id=user,
                                                    sort=options.sort,
                                                    page=options.page,
                                                    per_page=options.per_page)
            for contact in contacts['contact']:
                print "Contact: %s (%s)" %(contact['display_name'], contact['id'])

    elif options.add_video:
        if not check_video():
            print "Missing video"
            parser.print_help()
            sys.exit(-1)

        for vid in options.video:
            if options.album:
                for alb in options.album:
                    client.vimeo_albums_addVideo(album_id=alb,
                                                 video_id=vid)
            if options.channel:
                for chan in options.channel:
                    client.vimeo_channels_addVideo(channel_id=chan,
                                                   video_id=vid)
            if options.group:
                for chan in options.group:
                    client.vimeo_groups_addVideo(channel_id=chan,
                                                 video_id=vid)

###
### Folowing this line, the code has not been fixed yet.
###
    elif options.remove_video:
        if not check_video():
            print "Missing video"
            parser.print_help()
            sys.exit(-1)

        for vid in options.video:
            if options.album:
                for alb in options.album:
                    client.vimeo_albums_removeVideo(vid,
                                                alb)
            if options.channel:
                for chan in options.channel:
                    client.vimeo_channels_removeVideo(vid,
                                                      chan)
    elif options.get_groups:
        groups = client.vimeo_groups_getAll(page=options.page,
                                              sort=options.sort,
                                              per_page=options.per_page)
        for group in groups.findall("groups/group"):
            print "Name (%s):" %group.attrib['id'], group.find('name').text
    elif options.get_groups:
        if not check_group():
            print "Missing group"
            parser.print_help()
            sys.exit(-1)

        for group in option.group:
            groups = client.vimeo_groups_getFiles(group,
                                                  page=options.page,
                                                  per_page=options.per_page)
## FIXME: display the files !
#             for group in groups.findall("groups/group"):
#                 print "Name (%s):" %group.attrib['id'], group.find('name').text
    elif options.get_group_info:
        if not check_group():
            print "Missing group"
            parser.print_help()
            sys.exit(-1)

        for group in option.group:
            group_info = client.vimeo_groups_getInfo(group)
        ## FIXME: display the group info !
    elif options.get_group_members:
        if not check_group():
            print "Missing group"
            parser.print_help()
            sys.exit(-1)

        for group in option.group:
            group_members = client.vimeo_groups_getMembers(group,
                                                           options.page,
                                                           option.per_page,
                                                           option.sort)
        ## FIXME: display the group_members info !
        
    elif options.get_group_moderators:
        if not check_group():
            print "Missing group"
            parser.print_help()
            sys.exit(-1)

        for group in options.group:
            moderators = client.vimeo_groups_getModerators(group,
                                                           page=options.page,
                                                           per_page=options.per_page)
            for moderator in moderators.findall('moderators/user'):
                print "Name: %s (%s)" %(moderator.attrib['display_name'], moderator.attrib['id'])
    elif options.get_group_video_comments:
        if not check_group():
            print "Missing group"
            parser.print_help()
            sys.exit(-1)

        if not check_video():
            print "Missing video"
            parser.print_help()
            sys.exit(-1)

        for group in option.group:
            for video in options.video:
                comments = client.vimeo_groups_getVideoComments(group,
                                                                video,
                                                                page=options.page,
                                                                per_page=options.per_page)
                ##FIXME: display comments !

    elif options.set_album_description:
        if not check_album():
            print "Missing album"
            parser.print_help()
            sys.exit(-1)

        for alb in options.album:
            client.vimeo_albums_setDescription(options.set_album_description,
                                               alb)

    elif options.set_channel_description:
        if not check_channel():
            print "Missing channel"
            parser.print_help()
            sys.exit(-1)

        for chan in options.channel:
            client.vimeo_channels_setDescription(options.set_channel_description,
                                                 chan)
    elif options.set_password:
        if options.channel:
            for chan in options.channel:
                client.vimeo_channels_setPassword(options.set_password,
                                                  chan)
        if options.album:
            for alb in options.album:
                client.vimeo_albums_setPassword(options.set_password,
                                                   alb)
        if options.video:
            for vid in options.video:
                client.vimeo_videos_setPrivacy(privacy='password',
                                               password=options.set_password,
                                               video_id=vid)


if __name__ == '__main__':
    main(sys.argv)


