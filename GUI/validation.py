import os

COMPATIBLE_VIDEO_EXTENTIONS = ['.mp4', '.avi', '.MP4', '.AVI']
COMPATIBLE_PHOTO_EXTENTIONS = ['.jpg', '.JPG', '.jpeg', '.JPEG', '.png', '.PNG']
DEBUG_MODE = True

# Set of functions to validate if file/directory is chosen and is of correct type. Returns true for OK, false for NOT OK

def validate_video_file(filename):
    file_name, file_extension = os.path.splitext(filename)
    if DEBUG_MODE:
        print(file_name)
        print(file_extension)

    if not filename:
        print('No video file chosen')
        return False

    if not COMPATIBLE_VIDEO_EXTENTIONS.__contains__(file_extension):
        raise TypeError('Chosen video is not of compatible type. Please provide a .mp4 of .mov format video')

    return True


def validate_photo_file(filename):
    if filename == 'desktop.ini' or filename == 'results':
        return False

    file_name, file_extension = os.path.splitext(filename)
    if DEBUG_MODE:
        print(file_name)
        print(file_extension)

    if not filename:
        print('No photo file chosen')
        return False

    if not COMPATIBLE_PHOTO_EXTENTIONS.__contains__(file_extension):
        raise TypeError('Chosen photo is not of compatible type. Please provide a .jpg of .png format photo')

    return True


def validate_directory(dirname):
    file_name, file_extension = os.path.splitext(dirname)
    if DEBUG_MODE:
        print(file_name)
        print(file_extension)

    if not dirname:
        print('No directory chosen')
        return False

    if file_extension:
        raise NotADirectoryError('Provided path is not a directory. Please provide a directory')

    return True
