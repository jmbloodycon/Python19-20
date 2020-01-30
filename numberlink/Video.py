import cv2
import os


def make_video():
    """Создает видео по пулу отрисованных карточек"""
    image_folder = 'tmp'
    video_name = 'video.avi'

    images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
    images.sort(key=lambda x: int(x[:-4]))
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape

    i_video = cv2.VideoWriter(video_name, 0, 1, (width, height))

    for image in images:
        i_video.write(cv2.imread(os.path.join(image_folder, image)))

    cv2.destroyAllWindows()
    i_video.release()
