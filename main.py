from kivy.app import App
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
import Stats
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
import opponent


def hp():
    if opponent.armor == 0:
        opponent.hp = opponent.hp - 10
    else:
        opponent.armor = opponent.armor - 10


def gun():
    if Stats.Bullet > 0:
        Stats.Bullet = Stats.Bullet - 1
        Stats.T_Bullet = Stats.T_Bullet - 1
        Stats.Bullet_show = Stats.Bullet * 20


class KivyCamera(ButtonBehavior, Image):
    def __init__(self, capture, fps, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.capture = capture
        Clock.schedule_interval(self.update, 1.0 / fps)

    # Give harm to opponent

    def on_press(self):
        if Stats.x in range(Stats.posi[0], Stats.posi[0] + Stats.posi[1]):
            if Stats.y in range(Stats.posi[2], Stats.posi[2] + Stats.posi[3]):
                if Stats.Bullet > 0:
                    hp()
        gun()

    def update(self,dt):

        ret, img = self.capture.read()
        font = cv2.FONT_HERSHEY_PLAIN

        # Flip image if your camera make mirror effect
        img = cv2.flip(img, 1)

        # Determinate the With and Height
        width = int(img.shape[1])
        height = int(img.shape[0])

        # Add a coordinates of center to make
        Stats.x = int(width / 2)
        Stats.y = int(height / 2)
        cv2.circle(img, (Stats.x, Stats.y), 5, (0, 0, 255), -1)

        # Add Bullet image at screen
        bullet_img = cv2.imread('bul.png')
        Bl_1 = cv2.addWeighted(img[height - 54:height, 0:Stats.Bullet_show, :], 0.1,
                               bullet_img[0:54, 0:Stats.Bullet_show, :], 1, 0)
        img[height - 54:height, 0:Stats.Bullet_show] = Bl_1

        # Add a HP line image on screen
        hp_level_img = cv2.imread('hillpoint.png')
        HPL = cv2.addWeighted(img[height - 86:height - 54, 0:Stats.hp_player:], 1,
                              hp_level_img[0:32, 0:Stats.hp_player, :], 1, 0)
        img[height - 86:height - 54, 0:Stats.hp_player] = HPL

        # Use QR Code as HP and Armor Box
        decodedObjects = pyzbar.decode(img)
        for obj in decodedObjects:
            cv2.putText(img, str(obj.data), (50, 50), font, 2,
                        (255, 0, 0), 3)
            Stats.Box(str(obj.data))

        if ret:
            # convert it to texture
            buf1 = cv2.flip(img, 0)
            buf = buf1.tostring()
            image_texture = Texture.create(
                size=(img.shape[1], img.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            # display image from the texture
            self.texture = image_texture


class CamApp(App):
    def build(self):
        # Simple screen
        self.capture = cv2.VideoCapture(0)
        self.my_camera = KivyCamera(capture=self.capture, fps=30)
        bl = BoxLayout(orientation='horizontal', spacing='10')
        bl.add_widget(self.my_camera)

        # VR screen
        # self.capure2 = cv2.VideoCapture(0)
        # self.my_camera2 = KivyCamera(capture=self.capture, fps=30)
        # bl.add_widget(self.my_camera2)

        return bl

    def on_stop(self):
        self.capture.release()


if __name__ == '__main__':
    CamApp().run()
