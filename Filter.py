from TrackbarManager import TrackbarManager
import cv2
import numpy as np


class Filter:
    trk_manager = None
    frame_processed = None
    alg_trk_cfg = None
    hsv_trk_cfg = None
    range_low = None
    range_high = None
    kernel = None
    name = None
    config_enable = None
    area_calc_counter = 0
    MAX_AREA_CALC_COUNT = 10
    area_calc = 0
    filter_type = 0

    # types are 0 - circle, 1 - area
    def __init__(self, ref_img, alg_window, filt_window, conf_file=None,
                 filter_type=0, config_enable=False, kernel=None, name=None):
        if config_enable == False and conf_file == None:
            raise ValueError("configuration disabled and no file given")
        self.trk_manager = TrackbarManager(alg_window, filt_window, conf_file, config_enable)
        self.frame_processed = np.zeros(ref_img.shape, np.uint16)
        self.name = name
        self.config_enable = config_enable
        self.filter_type = filter_type

        self.update()
        if kernel is None:
            self.kernel = np.ones((5, 5), np.uint16)
        else:
            self.kernel = kernel

    def update(self):
        self.alg_trk_cfg, self.hsv_trk_cfg = self.trk_manager.get_conf_dicts()
        self.range_low = np.array([self.hsv_trk_cfg["h low"], self.hsv_trk_cfg["s low"], self.hsv_trk_cfg["v low"]])
        self.range_high = np.array([self.hsv_trk_cfg["h high"], self.hsv_trk_cfg["s high"], self.hsv_trk_cfg["v high"]])

    def work(self, frame):
        # read color filter configuration
        if self.trk_manager.update_needed():
            self.update()

        # perform color filtering
        self.frame_processed = cv2.inRange(frame, self.range_low, self.range_high)

        if self.config_enable:
            cv2.imshow("Processed", self.frame_processed)

        if self.filter_type == 0:
            circles = self.__get_circles()
            return circles
        elif self.filter_type == 1:
            self.area_calc_counter += 1
            if self.area_calc_counter > self.MAX_AREA_CALC_COUNT:
                self.area_calc = self.__get_filtered_area()
                self.area_calc_counter = 0

            return self.area_calc

    def __get_filtered_area(self):
        return np.count_nonzero(self.frame_processed)

    def __get_circles(self):
        cv2.erode(self.frame_processed, self.kernel, self.frame_processed)
        # cv2.dilate(self.frame_processed, self.kernel, dst=frame_processed)

        if 1 == self.alg_trk_cfg["canny switch"]:
            self.frame_processed = cv2.Canny(self.frame_processed,
                                             self.alg_trk_cfg["canny tresh1"], self.alg_trk_cfg["canny tresh2"])

        circles = cv2.HoughCircles(self.frame_processed, cv2.cv.CV_HOUGH_GRADIENT,
                                   self.alg_trk_cfg["dp"], self.alg_trk_cfg["minDist"],
                                   param1=self.alg_trk_cfg["param1"], param2=self.alg_trk_cfg["param2"],
                                   minRadius=self.alg_trk_cfg["minRadius"], maxRadius=self.alg_trk_cfg["maxRadius"])

        return circles

    def close(self):
        if self.config_enable:
            self.trk_manager.parse_to_file()