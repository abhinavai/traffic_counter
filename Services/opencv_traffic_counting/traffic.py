import os
import logging
import logging.handlers
import random

import numpy as np
import skvideo.io
import cv2
import matplotlib.pyplot as plt
from flask import jsonify
from Services.opencv_traffic_counting import utils
from Services.make_video_on_processed_images import create_video
# without this some strange errors happen
cv2.ocl.setUseOpenCL(False)
random.seed(123)


from Services.opencv_traffic_counting.pipeline import (PipelineRunner,ContourDetection,Visualizer,CsvWriter,VehicleCounter)


class Traffic_counter():

    def __init__(self,image_dir,video_source,shape,exits_pts,make_video):
        self.image_dir = image_dir
        self.video_source = video_source
        self.shape = shape
        self.exit_pts = exits_pts
        self.make_video = make_video


    def train_bg_subtractor(self,bg_subtractor, cap,num):
        '''
            BG substractor need process some amount of frames to start giving result
        '''
        print ('Training BG Subtractor...')
        i = 0
        for frame in cap:
            bg_subtractor.apply(frame, None, 0.001)
            i += 1
            if i >= num:
                return cap


    def main(self):
        log = logging.getLogger("main")

        # creating exit mask from points, where we will be counting our vehicles
        base = np.zeros(self.shape + (3,), dtype='uint8')
        exit_mask = cv2.fillPoly(base, self.exit_pts, (255, 255, 255))[:, :, 0]
        # there is also bgslibrary, that seems to give better BG substruction, but
        # not tested it yet
        bg_subtractor = cv2.createBackgroundSubtractorMOG2(
            history=500, detectShadows=True)

        # processing pipline for programming conviniance
        pipeline = PipelineRunner(pipeline=[
            ContourDetection(bg_subtractor=bg_subtractor,
                             save_image=True, image_dir=self.image_dir),
            # we use y_weight == 2.0 because traffic are moving vertically on video
            # use x_weight == 2.0 for horizontal.
            VehicleCounter(exit_masks=[exit_mask], y_weight=2.0),
            Visualizer(image_dir=self.image_dir),
            CsvWriter(path='/home/tatras/', name='/home/tatras/report.csv')
        ], log_level=logging.DEBUG)

        # Set up image source
        # You can use also CV2, for some reason it not working for me
        cap = skvideo.io.vreader(self.video_source)

        # skipping 500 frames to train bg subtractor
        self.train_bg_subtractor(bg_subtractor, cap, num=2)

        _frame_number = -1
        frame_number = -1
        for frame in cap:
            if not frame.any():
                log.error("Frame capture failed, stopping...")
                break

            # real frame number
            _frame_number += 1

            # skip every 2nd frame to speed up processing
            if _frame_number % 2 != 0:
                continue

            # frame number that will be passed to pipline
            # this needed to make video from cutted frames
            frame_number += 1

            # plt.imshow(frame)
            # plt.show()
            # return

            pipeline.set_context({
                'frame': frame,
                'frame_number': frame_number,
            })
            pipeline.run()

# ============================================================================
    def start_here(self):
        log = utils.init_logging()

        if not os.path.exists(self.image_dir):
            log.debug("Creating image directory `%s`...", self.image_dir)
            os.makedirs(self.image_dir)

        self.main()
        # if self.make_video == 'yes':
        #     create_video().create(img_dir=self.image_dir)

        data = {"success": True,
                "Message": None,
                "data": "Done"
                }
        resp = jsonify(data)
        resp.status_code = 200

        return resp
