import tkFileDialog
import cv2


class TrackbarManager():
    alg_trk_names = ["canny switch", "canny tresh1", "canny tresh2",  # Canny parameters
                 "dp", "minDist", "param1", "param2", "minRadius", "maxRadius"]  # HoughCircles parameters
    alg_trk_cfg = dict()
    hsv_trk_names = ["h low", "s low", "v low", "h high", "s high", "v high"]
    hsv_trk_cfg = dict()

    alg_window = ""
    filt_window = ""
    with_trackbars = False

    changed = True

    def __init__(self, alg_window, filt_window, conf_file=None, with_trackbars=False):
        self.alg_window = alg_window
        self.filt_window = filt_window
        self.with_trackbars = with_trackbars
        self.changed = True

        for name in self.alg_trk_names:
            self.alg_trk_cfg[name] = 0

        for name in self.hsv_trk_names:
            self.hsv_trk_cfg[name] = 0

        if with_trackbars:
            cv2.namedWindow(alg_window, cv2.CV_WINDOW_AUTOSIZE)
            cv2.namedWindow(filt_window, cv2.CV_WINDOW_AUTOSIZE)

            # Canny config
            cv2.createTrackbar(self.alg_trk_names[0], alg_window, 1, 1, self.report_change)
            cv2.createTrackbar(self.alg_trk_names[1], alg_window, 50, 500, self.report_change)
            cv2.createTrackbar(self.alg_trk_names[2], alg_window, 200, 1000, self.report_change)

            # Hough config
            cv2.createTrackbar(self.alg_trk_names[3], alg_window, 1, 10, self.report_change)
            cv2.createTrackbar(self.alg_trk_names[4], alg_window, 32, 100, self.report_change)
            cv2.createTrackbar(self.alg_trk_names[5], alg_window, 50, 200, self.report_change)
            cv2.createTrackbar(self.alg_trk_names[6], alg_window, 35, 200, self.report_change)
            cv2.createTrackbar(self.alg_trk_names[7], alg_window, 10, 100, self.report_change)
            cv2.createTrackbar(self.alg_trk_names[8], alg_window, 200, 500, self.report_change)

            # hsv filter config
            cv2.namedWindow(filt_window)
            for name in self.hsv_trk_cfg:
                cv2.createTrackbar(name, filt_window, 0, 255, self.report_change)

        self.parse_from_file(conf_file)

    def parse_from_file(self, file_name=None):
        if file_name is not None:
            file_to_load = open(file_name)
        else:
            file_to_load = tkFileDialog.askopenfile()

        lines = file_to_load.readlines()
        file_to_load.close()

        for l in lines:
            conf_param_pair = l.split(':')
            conf_param = conf_param_pair[0]
            value = int(conf_param_pair[1])
            if conf_param in self.alg_trk_cfg:
                self.alg_trk_cfg[conf_param] = value
                if self.with_trackbars:
                    cv2.setTrackbarPos(conf_param, self.alg_window, value)
            elif conf_param in self.hsv_trk_cfg:
                self.hsv_trk_cfg[conf_param] = value
                if self.with_trackbars:
                    cv2.setTrackbarPos(conf_param, self.filt_window, value)

    def parse_to_file(self, file_name=None):
        if file_name is not None:
            file_to_write = open(file_name, mode='w')
        else:
            file_to_write = tkFileDialog.asksaveasfile(mode='w', defaultextension=".conf")

        if file_to_write is not None:
            config_data = ""
            for name in self.hsv_trk_cfg:
                config_data += name + ':' + str(self.hsv_trk_cfg[name]) + '\n'

            for name in self.alg_trk_cfg:
                config_data += name + ':' + str(self.alg_trk_cfg[name]) + '\n'

            file_to_write.write(config_data)
            file_to_write.close()

    def get_conf_dicts(self):
        if self.with_trackbars:
            self.read_alg_data()
            self.read_hsv_data()
        self.changed = False
        return self.alg_trk_cfg, self.hsv_trk_cfg

    def read_alg_data(self):
        for name in self.alg_trk_names:
            self.alg_trk_cfg[name] = cv2.getTrackbarPos(name, self.alg_window)

    def read_hsv_data(self):
        for name in self.hsv_trk_names:
            self.hsv_trk_cfg[name] = cv2.getTrackbarPos(name, self.filt_window)

    def update_needed(self):
        return self.changed

    def report_change(self, x):
        self.changed = True