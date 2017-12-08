import os

from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand

# source using tutorial:
# https://www.pyimagesearch.com/2015/05/25/basic-motion-detection-and-tracking-with-python-and-opencv/

import datetime
import cv2

from django_cctv.models import MonitorPage


class Command(BaseCommand):
    help = 'Delete records without motion.'

    def add_arguments(self, parser):
        # video / record file
        parser.add_argument('video_path', type=str)

        # visual_output argument
        parser.add_argument(
            '--visual_output',
            action='store_true',
            dest='visual_output',
            help='Enable visual output for development',
        )

        # delete_unmotion_record argument
        parser.add_argument(
            '--delete-empty-video',
            action='store_true',
            dest='delete_unmotion_record',
            help='Enable to delete videos without any motions',
        )

    def handle(self, *args, **options):
        # video file path
        video_file = options['video_path']

        # get an visual output for debugging
        if options['visual_output']:
            visual_output = True
        else:
            visual_output = False

        # delete if a record / video has no motion at all
        if options['delete_unmotion_record']:
            delete_unmotion_record = True
        else:
            delete_unmotion_record = False

        # get model through video_file
        video_name = os.path.basename(video_file)
        video_stream_key = video_name.split("-")[0]
        try:
            monitor_page = MonitorPage.objects.get(stream_key=video_stream_key)
        except ObjectDoesNotExist:
            print("Monitor with stream key '%s' does not exists" % video_stream_key)
            raise

        # if cam_images in monitor_page has cropped attributes
        video_cropped = False

        # if record cropped was selected
        if monitor_page.cam_image:
            if monitor_page.cam_image.focal_point_x:
                # set video_cropped, true every frame will be cropped
                video_cropped = True

                # get cropped height and width
                focal_point_width_halve = monitor_page.cam_image.focal_point_width / 2
                focal_point_height_halve = monitor_page.cam_image.focal_point_height / 2

                # declare x & y coordinates as int
                x_start = int(monitor_page.cam_image.focal_point_x - focal_point_width_halve)
                x_end = int(monitor_page.cam_image.focal_point_x + focal_point_width_halve)
                y_start = int(monitor_page.cam_image.focal_point_y - focal_point_height_halve)
                y_end = int(monitor_page.cam_image.focal_point_y + focal_point_height_halve)

        # minimum area size, default 500
        min_area = 500

        # reading from a video file
        camera = cv2.VideoCapture(video_file)

        # initialize the first frame in the video stream
        firstFrame = None

        # boolean True as long there was no motion detected or visual_mode is on
        motion_detected_or_visual_mode = True

        # loop over the frames of the video
        while motion_detected_or_visual_mode:
            # grab the current frame and initialize the occupied/unoccupied
            # text
            (grabbed, frame) = camera.read()
            text = "Unoccupied"

            # if the frame could not be grabbed, then we have reached the end
            # of the video
            if not grabbed:
                break

            # cropped frame
            if video_cropped:
                frame = frame[y_start:y_end, x_start:x_end]

            # convert frame to grayscale, and blur it
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)

            # if the first frame is None, initialize it
            if firstFrame is None:
                firstFrame = gray
                continue

            # compute the absolute difference between the current frame and
            # first frame
            frameDelta = cv2.absdiff(firstFrame, gray)
            thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

            # dilate the thresholded image to fill in holes, then find contours
            # on thresholded image
            thresh = cv2.dilate(thresh, None, iterations=2)
            (_, cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # loop over the contours
            for c in cnts:
                # if the contour is too small, ignore it
                if cv2.contourArea(c) < min_area:
                    continue
                else:
                    # motion detected
                    if not visual_output:
                        print("motion detected")
                        motion_detected_or_visual_mode = False
                        break

                # compute the bounding box for the contour, draw it on the frame,
                # and update the text
                (x, y, w, h) = cv2.boundingRect(c)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                text = "Occupied"

                # draw the text and timestamp on the frame
                cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                            (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

                # show the frame and record if the user presses a key
                cv2.imshow("Security Feed", frame)
                cv2.imshow("Thresh", thresh)
                cv2.imshow("Frame Delta", frameDelta)
                key = cv2.waitKey(1) & 0xFF

                # if the `q` key is pressed, break from the lop
                if key == ord("q"):
                    break

        # cleanup the camera and close any open windows
        camera.release()
        cv2.destroyAllWindows()

        # delete video without motion
        if delete_unmotion_record:
            os.remove(video_file)
