
import cv2
import numpy as np
import ezdxf
import matplotlib.pyplot as plt
# initialize camera capture
def prin(length,height,width):
    top_view_pos = (0, 0)
    front_view_pos = (0, height)
    side_view_pos = (length, 0)

    # create a figure with three subplots
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(10, 4))

    # plot the top view
    ax1.plot([0, length], [0, 0], 'k-', linewidth=2)
    ax1.plot([0, 0], [0, width], 'k-', linewidth=2)
    ax1.plot([length, length], [0, width], 'k-', linewidth=2)
    ax1.plot([0, length], [width, width], 'k-', linewidth=2)
    ax1.set_xlim([-5, length + 5])
    ax1.set_ylim([-5, width + 5])
    ax1.set_aspect('equal')
    ax1.set_xlabel('Length')
    ax1.set_ylabel('Width')
    ax1.set_title('Top View')

    # plot the front view
    ax2.plot([0, length], [height, height], 'k-', linewidth=2)
    ax2.plot([0, 0], [height, height - width], 'k-', linewidth=2)
    ax2.plot([length, length], [height, height - width], 'k-', linewidth=2)
    ax2.plot([0, length], [height - width, height - width], 'k-', linewidth=2)
    ax2.set_xlim([-5, length + 5])
    ax2.set_ylim([height - width - 5, height + 5])
    ax2.set_aspect('equal')
    ax2.set_xlabel('Length')
    ax2.set_ylabel('Height')
    ax2.set_title('Front View')

    # plot the side view
    ax3.plot([0, width], [height, height], 'k-', linewidth=2)
    ax3.plot([0, 0], [height, 0], 'k-', linewidth=2)
    ax3.plot([width, width], [height, 0], 'k-', linewidth=2)
    ax3.plot([0, width], [0, 0], 'k-', linewidth=2)
    ax3.set_xlim([-5, width + 5])
    ax3.set_ylim([-5, height + 5])
    ax3.set_aspect('equal')
    ax3.set_xlabel('Width')
    ax3.set_ylabel('Height')
    ax3.set_title('Side View')

    # plot the lines connecting the views
    # plot the lines connecting the views
    ax1.plot([top_view_pos[0], front_view_pos[0] - 10], [top_view_pos[1], front_view_pos[1]], 'k-')
    ax1.plot([top_view_pos[0], side_view_pos[0]], [top_view_pos[1], side_view_pos[1]], 'k-')
    ax2.plot([front_view_pos[0], top_view_pos[0] + length + 10], [front_view_pos[1], top_view_pos[1]], 'k-')
    ax2.plot([front_view_pos[0], side_view_pos[0]], [front_view_pos[1], side_view_pos[1]], 'k-')
    ax3.plot([side_view_pos[0], top_view_pos[0] + width + 10], [side_view_pos[1], top_view_pos[1]], 'k-')
    ax3.plot([side_view_pos[0], front_view_pos[0]], [side_view_pos[1], front_view_pos[1]], 'k-')

    # adjust the spacing between subplots
    plt.subplots_adjust(wspace=0.1, hspace=0)

    # display the figure
    plt.show()
    # save the drawing as DWG file
    doc = ezdxf.new('R2007')
    msp = doc.modelspace()
    scale = 1

    # add top view entities
    msp.add_line([top_view_pos[0], front_view_pos[0] - 10], [top_view_pos[1], front_view_pos[1]],
                 dxfattribs={'color': 7})
    msp.add_line([top_view_pos[0], side_view_pos[0]], [top_view_pos[1], side_view_pos[1]],
                 dxfattribs={'color': 7})
    msp.add_line((top_view_pos[0], top_view_pos[1]), (top_view_pos[0], top_view_pos[1] + width),
                 dxfattribs={'color': 7})

    # add front view entities
    msp.add_line((front_view_pos[0], front_view_pos[1]), (front_view_pos[0] + length, front_view_pos[1]),
                 dxfattribs={'color': 7})
    msp.add_line((front_view_pos[0] + length, front_view_pos[1]),
                 (front_view_pos[0] + length, front_view_pos[1] - height), dxfattribs={'color': 7})
    msp.add_line((front_view_pos[0], front_view_pos[1]), (front_view_pos[0], front_view_pos[1] - height),
                 dxfattribs={'color': 7})

    # add side view entities
    msp.add_line((side_view_pos[0], side_view_pos[1]), (side_view_pos[0], side_view_pos[1] - height),
                 dxfattribs={'color': 7})
    msp.add_line((side_view_pos[0], side_view_pos[1]), (side_view_pos[0] + width, side_view_pos[1]),
                 dxfattribs={'color': 7})
    msp.add_line((side_view_pos[0] + width, side_view_pos[1]), (side_view_pos[0] + width, side_view_pos[1] - height),
                 dxfattribs={'color': 7})

    # save the drawing
    doc.saveas('drawin.dxf')
    print("saved")


cap = cv2.VideoCapture(0)

# set camera resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1020)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 760)

# create window for output display
cv2.namedWindow("Object Measurement")
images=[]
while True:
    # read frame from camera
    ret, frame = cap.read()
    images.append(frame)
    # apply pre-processing steps to enhance image quality
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 100, 200)

    # identify objects in the image using edge detection
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # loop through each contour and calculate size and position
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 100: # ignore small contours
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, "Object size: " + str(w) + "x" + str(h), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # display the results of the measurement
    cv2.imshow("Object Measurement", frame)

    # check for user input to quit the program
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# release camera and close windows
cap.release()
cv2.destroyAllWindows()
images = np.array(images)
# print the shape of the array to verify the number of captured images
print("Captured images shape:", images.shape)
prin(images.shape[0],images.shape[1],images.shape[2])
