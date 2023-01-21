import os

COMPATIBLE_VIDEO_EXTENTIONS = ['.mp4', '.mov', '.MP4', '.MOV']
COMPATIBLE_PHOTO_EXTENTIONS = ['.jpg', '.JPG', '.jpeg', '.JPEG', '.png', '.PNG']
DEBUG_MODE = True


def validate_video_file(filename):
    file_name, file_extension = os.path.splitext(filename)
    if DEBUG_MODE:
        print(file_name)
        print(file_extension)

    if not COMPATIBLE_VIDEO_EXTENTIONS.__contains__(file_extension):
        raise TypeError('Chosen video is not of compatible type. Please provide a .mp4 of .mov format video')


def validate_photo_file(filename):
    if filename == 'desktop.ini':
        return

    file_name, file_extension = os.path.splitext(filename)
    if DEBUG_MODE:
        print(file_name)
        print(file_extension)

    if not COMPATIBLE_PHOTO_EXTENTIONS.__contains__(file_extension):
        raise TypeError('Chosen photo is not of compatible type. Please provide a .jpg of .png format photo')


def validate_directory(dirname):
    file_name, file_extension = os.path.splitext(dirname)
    if DEBUG_MODE:
        print(file_name)
        print(file_extension)

    if file_extension:
        raise NotADirectoryError('Provided path is not a directory. Please provide a directory')
