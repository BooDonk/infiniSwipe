from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivy.properties import ObjectProperty

from kivy.uix.camera import Camera
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2


class ContentNavigationDrawer(MDScrollView):
    screen_manaer = ObjectProperty()
    nav_drawer = ObjectProperty()


class Home(Screen):

    def toggle_text(self):
        additional_text = self.ids.additional_text
        button = self.ids.button
        if additional_text.opacity == 0:
            additional_text.opacity = 1
            button.text = "Stop"
            # Schedule the video capture function to run asynchronously
            self.capture = cv2.VideoCapture(0)
            Clock.schedule_interval(self.update, 1.0/33.0)
        else:
            additional_text.opacity = 0
            additional_text.height = 0  # Hide the text
            button.text = "Start"
            if hasattr(self, 'capture'):
                self.capture.release()  # Release the capture object
                Clock.unschedule(self.update)  # Stop the update function
           
    def update(self, *args):
         if hasattr(self, 'capture'):
            ret, frame = self.capture.read()
            if ret:
                frame = frame[ 120:120+250, 200:200+250, :]

                #Flip horizontally and convert image to texture
                buf = cv2.flip(frame,0).tostring()
                img_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt="bgr")
                img_texture.blit_buffer(buf, colorfmt="bgr" , bufferfmt="ubyte")

                cam = self.ids.cam
                cam.texture = img_texture

    
    
  
class Test(MDBoxLayout):
   pass

    

# had to rename the settings because it was interfering with kivy
class Set(Screen):
    pass

class About(Screen):
    pass

class InfiniSwipeApp(MDApp):
    def build(self):
     

        return Builder.load_file('infiniSwipe.kv')
    

if __name__ == "__main__":
    InfiniSwipeApp().run()
