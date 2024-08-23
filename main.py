from PIL import ImageDraw, Image, ImageFont
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.widget import MDWidget

class HomePage(MDWidget):
    Builder.load_file("kivy_files/home_page.kv")

class Go(MDWidget):
    Builder.load_file("kivy_files/go.kv")

    def create_sticker(self, output_path='sticker.png'):
        image_path=self.ids.file.text
        text=self.ids.text.text+""
        image = Image.open(image_path).convert("RGBA")
        image = image.resize((50,50), Image.Resampling.LANCZOS)
        txt = Image.new('RGBA', image.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(txt)
        font = ImageFont.load_default()
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        width, height = image.size
        x = (width - text_width) // 2
        y = height - text_height - 10
        draw.text((x, y), text, font=font, fill=(255,220, 10, 255))
        combined = Image.alpha_composite(image, txt)
        combined.save(output_path, format="PNG")
        toast(f"Sticker saved as {output_path}")

class MainApp(MDApp):
    title = "Sticker Maker"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            preview=True
        )

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.screen = MDScreen()
        self.home_page = HomePage()
        self.screen.add_widget(self.home_page)
        return self.screen

    def go(self):
        self.screen.clear_widgets()
        self.go = Go()
        self.screen.add_widget(self.go)

    def file_manager_open(self):
        self.file_manager.show('/')

    def select_path(self, path):
        self.exit_manager()
        self.go.ids.file.text = path
        toast(f"Selected: {path}")

    def exit_manager(self, *args):
        self.file_manager.close()


if __name__ == "__main__":
    MainApp().run()
