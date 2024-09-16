import numpy as np
import cv2 as cv
import argparse
import os
# import gzip
# import time




def create_labels(save_dir, save_fname, mask_color, img_dir, img_path=None):
    mask_color_ = [min([max([int(i), 0]), 255]) for i in mask_color.split(",")]

    if (img_path is not None):
        img = None
        points = []
        try:
            if (os.path.exists(img_path) and os.path.isfile(img_path)):
                img = cv.imread(img_path)
            else:
                raise ValueError("File not Found")
        except Exception as e:
            print(e)
            exit()
            
        def draw_circle(event,x,y,flags,param):
            if event == cv.EVENT_LBUTTONDBLCLK:
                cv.circle(img,(x,y),5,(255,0,0),-1)
                points.append((x,y))


        cv.namedWindow("Image", cv.WINDOW_NORMAL)
        cv.setMouseCallback("Image", draw_circle)
        while True:
            cv.imshow("Image", cv.fillPoly(img.copy(), [cv.convexHull(np.array(points), returnPoints=True).reshape((-1,2))], mask_color_) if len(points)>2 else img)
            if cv.waitKey(1) & 0xFF == ord("q"):
                break
        cv.destroyAllWindows()

        # print(cv.convexHull(np.array(points), returnPoints=True).reshape((-1,2)))         
        mask = cv.fillPoly(np.zeros_like(img), [cv.convexHull(np.array(points), returnPoints=True).reshape((-1,2))], [1,1,1]).astype(np.uint8)
        np.savetxt(os.path.join(save_dir, "mask.csv" if save_fname is None else save_fname), mask[:,:,0], delimiter=',')

        
    elif (img_dir is not None):
        # handle directory of images
        pass


def main():
    parser = argparse.ArgumentParser(description='Draw Annotations on Images')
    parser.add_argument('--img_dir', type=str, help='path to image directory', default=None)
    parser.add_argument('--img_name', type=str, help='path to image', default=None)
    parser.add_argument('--save_dir', type=str, help='path to mask directory', default=None)
    parser.add_argument('--save_fname', type=str, help='path to mask directory', default=None)
    parser.add_argument('--mask_color', type=str, help='three digits delimited by comma \"255,255,255\"', default="120,120,120")

    
    args = parser.parse_args()

    if (((args.img_dir is None) and (args.img_name is None)) or (args.save_dir is None)):
        print("Path of Images and Masks must be given")
    else:
        if (args.img_name is None):
            create_labels(args.save_dir, args.save_fname, args.mask_color, args.img_dir, None)
        else:
            create_labels(args.save_dir, args.save_fname, args.mask_color, None, args.img_name)



if __name__ == "__main__":
    main()

