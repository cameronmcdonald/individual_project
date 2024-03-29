########################################################################
#
# Copyright (c) 2022, STEREOLABS.
#
# All rights reserved.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
########################################################################

import pyzed.sl as sl
import numpy as np
import socket
import struct

# I added function to send data over UDP to Unity.

def send_position_udp(position, udp_socket):
    packed_data = struct.pack('!ddd', position[0], position[1], position[2])
    udp_socket.sendto(packed_data, ('127.0.0.1', 25001))

def main():
    # Create a Camera object
    zed = sl.Camera()

    # Create a InitParameters object and set configuration parameters
    init_params = sl.InitParameters()
    init_params.depth_mode = sl.DEPTH_MODE.PERFORMANCE
    init_params.coordinate_units = sl.UNIT.METER
    init_params.sdk_verbose = 1

    # Open the camera
    err = zed.open(init_params)
    if err != sl.ERROR_CODE.SUCCESS:
        print("Camera Open : "+repr(err)+". Exit program.")
        exit()

    obj_param = sl.ObjectDetectionParameters()
    obj_param.enable_tracking=True
    obj_param.enable_segmentation=True
    obj_param.detection_model = sl.OBJECT_DETECTION_MODEL.MULTI_CLASS_BOX_MEDIUM

    if obj_param.enable_tracking :
        positional_tracking_param = sl.PositionalTrackingParameters()
        #positional_tracking_param.set_as_static = True
        zed.enable_positional_tracking(positional_tracking_param)

    print("Object Detection: Loading Module...")

    err = zed.enable_object_detection(obj_param)
    if err != sl.ERROR_CODE.SUCCESS :
        print("Enable object detection : "+repr(err)+". Exit program.")
        zed.close()
        exit()

    objects = sl.Objects()
    obj_runtime_param = sl.ObjectDetectionRuntimeParameters()
    # I changed threshold to 80% confidence.
    obj_runtime_param.detection_confidence_threshold = 80


    # I added deinition of the UDP socket.
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


    # I added Try/Except with while statement and keyboard interupt in order to allow the script to run indefinetely. 
    try:
        while True:
            zed.grab()
            zed.retrieve_objects(objects, obj_runtime_param)
            if objects.is_new :
                obj_array = objects.object_list
                print(str(len(obj_array))+" Object(s) detected\n")
                if len(obj_array) > 0 :
                    object = obj_array[0]
                    # I added If statement to remove uneccassary info from labels other 'Vehicle'.
                    if repr(object.label) == 'Vehicle':
                        print("Object attributes:")
                        print(" Label '"+repr(object.label)+"' (conf. "+str(int(object.confidence))+"/100)")
                        if obj_param.enable_tracking :
                            print(" Tracking ID: "+str(int(object.id))+" tracking state: "+repr(object.tracking_state)+" / "+repr(object.action_state))
                        
                        # I added position definition and sending of position to sender function.
                        position = object.position
                        send_position_udp(position, udp_socket)
                        velocity = object.velocity
                        dimensions = object.dimensions
                        print(" 3D position: [{0},{1},{2}]\n Velocity: [{3},{4},{5}]\n 3D dimensions: [{6},{7},{8}]".format(position[0],position[1],position[2],velocity[0],velocity[1],velocity[2],dimensions[0],dimensions[1],dimensions[2]))
                        if object.mask.is_init():
                            print(" 2D mask available")
                        print(" Bounding Box 2D ")
                        bounding_box_2d = object.bounding_box_2d
                        for it in bounding_box_2d :
                            print("    "+str(it),end='')
                        print("\n Bounding Box 3D ")
                        bounding_box = object.bounding_box
                        for it in bounding_box :
                            print("    "+str(it),end='')

    except KeyboardInterrupt:
        udp_socket.close()
        exit()

if __name__ == "__main__":
    main()
