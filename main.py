from kivy.app import App
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2
import pyzbar.pyzbar as pyzbar
import Stats
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
import opponent

# Plyer recive harm from enemy
def hp():
    if Stats.armor_player == 0:
        Stats.hp_player = Stats.hp_player - opponent.enemy.damage
    else:
        Stats.armor_player = Stats.armor_player - opponent.enemy.damage


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
        Clock.schedule_interval(self.bit, 1)

    # Give harm to opponent
    def on_press(self):

        # Verify if target is in ROI and make give harm
        if Stats.Bullet > 0:
            opponent.enemy.attac(Stats.damage_player)
            if Stats.x in range(Stats.posi[0], Stats.posi[0] + Stats.posi[1]):
                if Stats.y in range(Stats.posi[2], Stats.posi[2] + Stats.posi[3]):
                    opponent.enemy.attac(Stats.damage_player)
        gun()

    def bit(self, dt):
        if Stats.enemy_type != 0:
            hp()

    def update(self, dt):

        ret, img = self.capture.read()
        font = cv2.FONT_HERSHEY_PLAIN

        # Flip image if your camera make mirror effect
        img = cv2.flip(img, 1)

        # Determinate the With and Height
        width = int(img.shape[1])
        height = int(img.shape[0])

        # Add a coordinates of center to make the aim
        Stats.x = int(width / 2)
        Stats.y = int(height / 2)
        cv2.circle(img, (Stats.x, Stats.y), 5, (0, 0, 255), -1)

        # Add Bullet image at screen
        bullet_img = cv2.imread('bul.png')
        Bl_1 = cv2.addWeighted(img[height - 54:height, 0:Stats.Bullet_show, :], 0.1,
                               bullet_img[0:54, 0:Stats.Bullet_show, :], 1, 0)
        img[height - 54:height, 0:Stats.Bullet_show] = Bl_1

        # Add a HP bar image on screen
        hp_level_img = cv2.imread('hillpoint.png')
        HPL = cv2.addWeighted(img[height - 86:height - 54, 0:Stats.hp_player:], 1,
                              hp_level_img[0:32, 0:Stats.hp_player, :], 1, 0)
        img[height - 86:height - 54, 0:Stats.hp_player] = HPL
        #Add a enemy
        EnHp = cv2.addWeighted(img[height - 132:height - 100, 0:opponent.enemy.hp:], 1,
                              hp_level_img[0:32, 0:opponent.enemy.hp, :], 1, 0)
        img[height - 132:height - 100, 0:opponent.enemy.hp] = EnHp

        # Detect QR-code
        decodedObjects = pyzbar.decode(img)
        for obj in decodedObjects:
            cv2.putText(img, str(obj.data), (50, 50), font, 2,
                        (255, 0, 0), 3)
            Stats.Box(str(obj.data))
            Stats.posi = obj.rect

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
