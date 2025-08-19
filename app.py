# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.modalview import ModalView
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.spinner import Spinner
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.metrics import dp
import os
import sys

# Set dark background color for window
Window.clearcolor = get_color_from_hex('#1a1a1a')


# --- CHANGE: Added a function to find the path to resources ---
# This function ensures that the application can find images, whether it's
# running from a computer or as a final APK on a mobile device.
def get_resource_path(relative_path):
    """ Gets the absolute path to a resource, works for dev and for bundled app. """
    try:
        # In a bundled app (APK), the path is stored in sys._MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # When running normally, the path is relative to this file.
        # We need to go up two directories from app.py (src/elektrohelper) to the project root,
        # and then into the 'resources' directory.
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "resources"))
    
    return os.path.join(base_path, relative_path)


class ImageModal(ModalView):
    """Modal popup for enlarged image view"""
    
    def __init__(self, image_source, symbol_name, symbol_id, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (0.9, 0.8)
        self.background_color = [0.1, 0.1, 0.1, 0.95]
        
        # Main layout for modal
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        
        # Header with symbol info
        header_layout = BoxLayout(
            orientation='vertical', 
            size_hint_y=None, 
            height=dp(100),
            spacing=dp(5)
        )
        
        # Symbol number
        number_label = Label(
            text=f"#{symbol_id}",
            color=get_color_from_hex('#ff8c00'),
            font_size='18sp',
            bold=True,
            size_hint_y=None,
            height=dp(25)
        )
        
        # Symbol name
        name_label = Label(
            text=symbol_name,
            color=get_color_from_hex('#ffffff'),
            font_size='14sp',
            text_size=(None, None),
            halign='center',
            size_hint_y=None,
            height=dp(60)
        )
        name_label.bind(size=name_label.setter('text_size'))
        
        header_layout.add_widget(number_label)
        header_layout.add_widget(name_label)
        layout.add_widget(header_layout)
        
        # Enlarged image
        if os.path.exists(image_source):
            enlarged_image = Image(
                source=image_source,
                allow_stretch=True,
                keep_ratio=True
            )
        else:
            enlarged_image = Label(
                text="[size=72sp][font=DejaVuSans]📷[/font][/size]",
                markup=True,
                color=get_color_from_hex('#666666')
            )
        
        layout.add_widget(enlarged_image)
        
        # Close button
        close_button = Button(
            text="Zavrieť",
            size_hint_y=None,
            height=dp(50),
            background_color=get_color_from_hex('#ff8c00'),
            color=get_color_from_hex('#1a1a1a'),
            font_size='16sp',
            bold=True
        )
        close_button.bind(on_press=lambda x: self.dismiss())
        layout.add_widget(close_button)
        
        self.add_widget(layout)


class SymbolItem(BoxLayout):
    """Widget for individual symbols"""
    
    def __init__(self, symbol_id, symbol_name, **kwargs):
        super().__init__(**kwargs)
        self.symbol_id = symbol_id
        self.symbol_name = symbol_name
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(80)
        self.padding = [dp(15), dp(10), dp(15), dp(10)]
        self.spacing = dp(15)
        
        # Background for item
        with self.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(*get_color_from_hex('#2d2d2d'))
            self.rect = Rectangle(size=self.size, pos=self.pos)
        
        self.bind(size=self._update_rect, pos=self._update_rect)
        
        # Symbol image
        self.add_widget(self._create_image_widget(symbol_id))
        
        # Text section - make it clickable
        text_layout = BoxLayout(orientation='vertical', spacing=dp(2))
        
        # Number label
        number_label = Label(
            text=f"#{symbol_id}",
            color=get_color_from_hex('#ff8c00'),
            font_size='16sp',
            bold=True,
            size_hint_y=None,
            height=dp(20),
            halign='left',
            valign='middle'
        )
        number_label.bind(size=number_label.setter('text_size'))
        text_layout.add_widget(number_label)
        
        # Name label - clickable
        name_label = Button(
            text=symbol_name,
            color=get_color_from_hex('#ffffff'),
            background_color=(0, 0, 0, 0),  # Transparent background
            font_size='16sp',
            halign='left',
            valign='middle',
            text_size=(None, None)
        )
        name_label.bind(size=name_label.setter('text_size'))
        name_label.bind(on_press=self._show_enlarged_image)
        text_layout.add_widget(name_label)
        
        self.add_widget(text_layout)
    
    def _update_rect(self, instance, value):
        """Update background when size/position changes"""
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    
    def _create_image_widget(self, symbol_id):
        """Create widget for image"""
        # CHANGE: Use the new function to find the correct path
        image_path = get_resource_path(f"images/{symbol_id}.png")
        
        if os.path.exists(image_path):
            img = Image(
                source=image_path,
                size_hint=(None, None),
                size=(dp(64), dp(45)),
                allow_stretch=True,
                keep_ratio=True
            )
        else:
            # Placeholder if image doesn't exist
            img = Label(
                text="[size=24sp][font=DejaVuSans]📷[/font][/size]",
                markup=True,
                color=get_color_from_hex('#666666'),
                size_hint=(None, None),
                size=(dp(64), dp(45))
            )
        
        return img
    
    def _show_enlarged_image(self, instance):
        """Show enlarged image in modal"""
        # CHANGE: Use the new function to find the correct path
        image_path = get_resource_path(f"images/{self.symbol_id}.png")
        modal = ImageModal(image_path, self.symbol_name, self.symbol_id)
        modal.open()


class SymbolsTab(BoxLayout):
    """Tab for electrical symbols"""
    
    def __init__(self, symbols, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.symbols = symbols
        self.create_symbols_view()
    
    def create_symbols_view(self):
        """Create symbols scrollable view"""
        # ScrollView with content
        scroll = ScrollView(
            do_scroll_x=False,
            do_scroll_y=True,
            bar_width=dp(10),
            bar_color=get_color_from_hex('#ff8c00'),
            bar_inactive_color=get_color_from_hex('#666666'),
            effect_cls='ScrollEffect',
            scroll_type=['bars', 'content']
        )
        
        # Layout for all symbols
        symbols_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(5),
            padding=[dp(10), dp(10), dp(10), dp(10)],
            size_hint_y=None
        )
        symbols_layout.bind(minimum_height=symbols_layout.setter('height'))
        
        # Add all symbols
        for symbol_id, symbol_name in self.symbols.items():
            symbol_item = SymbolItem(symbol_id, symbol_name)
            symbols_layout.add_widget(symbol_item)
        
        scroll.add_widget(symbols_layout)
        self.add_widget(scroll)


class ResistorColorCodeTab(BoxLayout):
    """Tab for resistor color code calculator"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = dp(20)
        self.spacing = dp(15)
        self.create_resistor_view()
    
    def create_resistor_view(self):
        """Create resistor color code interface"""
        # Title
        title = Label(
            text="Farebný kód rezistorov",
            color=get_color_from_hex('#ff8c00'),
            font_size='20sp',
            bold=True,
            size_hint_y=None,
            height=dp(40)
        )
        self.add_widget(title)
        
        # Color options
        colors = {
            'Čierna': {'value': 0, 'hex': '#000000'},
            'Hnedá': {'value': 1, 'hex': '#8B4513'},
            'Červená': {'value': 2, 'hex': '#FF0000'},
            'Oranžová': {'value': 3, 'hex': '#FFA500'},
            'Žltá': {'value': 4, 'hex': '#FFFF00'},
            'Zelená': {'value': 5, 'hex': '#008000'},
            'Modrá': {'value': 6, 'hex': '#0000FF'},
            'Fialová': {'value': 7, 'hex': '#8B008B'},
            'Sivá': {'value': 8, 'hex': '#808080'},
            'Biela': {'value': 9, 'hex': '#FFFFFF'}
        }
        
        tolerance_colors = {
            'Hnedá': 1, 'Červená': 2, 'Zelená': 0.5, 'Modrá': 0.25,
            'Fialová': 0.1, 'Sivá': 0.05, 'Zlatá': 5, 'Strieborná': 10
        }
        
        # Color selection layout
        color_layout = GridLayout(cols=2, spacing=dp(10), size_hint_y=None, height=dp(200))
        
        # First digit
        color_layout.add_widget(Label(text="1. číslica:", color=get_color_from_hex('#ffffff'), font_size='14sp'))
        self.first_digit = Spinner(
            text='Čierna',
            values=list(colors.keys()),
            background_color=get_color_from_hex('#2d2d2d'),
            color=get_color_from_hex('#ffffff')
        )
        color_layout.add_widget(self.first_digit)
        
        # Second digit
        color_layout.add_widget(Label(text="2. číslica:", color=get_color_from_hex('#ffffff'), font_size='14sp'))
        self.second_digit = Spinner(
            text='Čierna',
            values=list(colors.keys()),
            background_color=get_color_from_hex('#2d2d2d'),
            color=get_color_from_hex('#ffffff')
        )
        color_layout.add_widget(self.second_digit)
        
        # Multiplier
        color_layout.add_widget(Label(text="Násobiteľ:", color=get_color_from_hex('#ffffff'), font_size='14sp'))
        self.multiplier = Spinner(
            text='Čierna',
            values=list(colors.keys()),
            background_color=get_color_from_hex('#2d2d2d'),
            color=get_color_from_hex('#ffffff')
        )
        color_layout.add_widget(self.multiplier)
        
        # Tolerance
        color_layout.add_widget(Label(text="Tolerancia:", color=get_color_from_hex('#ffffff'), font_size='14sp'))
        self.tolerance = Spinner(
            text='Zlatá',
            values=list(tolerance_colors.keys()),
            background_color=get_color_from_hex('#2d2d2d'),
            color=get_color_from_hex('#ffffff')
        )
        color_layout.add_widget(self.tolerance)
        
        self.add_widget(color_layout)
        
        # Calculate button
        calc_btn = Button(
            text="Vypočítať hodnotu",
            size_hint_y=None,
            height=dp(50),
            background_color=get_color_from_hex('#ff8c00'),
            color=get_color_from_hex('#1a1a1a'),
            font_size='16sp',
            bold=True
        )
        calc_btn.bind(on_press=self.calculate_resistor)
        self.add_widget(calc_btn)
        
        # Result
        self.resistor_result = Label(
            text="Vyberte farby a stlačte vypočítať",
            color=get_color_from_hex('#ffffff'),
            font_size='18sp',
            size_hint_y=None,
            height=dp(80),
            text_size=(None, None),
            halign='center'
        )
        self.resistor_result.bind(size=self.resistor_result.setter('text_size'))
        self.add_widget(self.resistor_result)
        
        # Quick reference
        ref_title = Label(
            text="Rýchly prehľad farieb:",
            color=get_color_from_hex('#ff8c00'),
            font_size='16sp',
            bold=True,
            size_hint_y=None,
            height=dp(30)
        )
        self.add_widget(ref_title)
        
        ref_text = """Čierna=0, Hnedá=1, Červená=2, Oranžová=3, Žltá=4
Zelená=5, Modrá=6, Fialová=7, Sivá=8, Biela=9
Tolerancia: Zlatá=±5%, Strieborná=±10%"""
        
        ref_label = Label(
            text=ref_text,
            color=get_color_from_hex('#ffffff'),
            font_size='12sp',
            text_size=(None, None),
            halign='left'
        )
        ref_label.bind(size=ref_label.setter('text_size'))
        self.add_widget(ref_label)
        
        # Store color values for calculation
        self.colors = colors
        self.tolerance_colors = tolerance_colors
    
    def calculate_resistor(self, instance):
        """Calculate resistor value from colors"""
        try:
            first = self.colors[self.first_digit.text]['value']
            second = self.colors[self.second_digit.text]['value']
            mult = self.colors[self.multiplier.text]['value']
            tol = self.tolerance_colors[self.tolerance.text]
            
            # Calculate resistance value
            resistance = (first * 10 + second) * (10 ** mult)
            
            # Format result
            if resistance >= 1000000:
                formatted = f"{resistance/1000000:.1f} MΩ"
            elif resistance >= 1000:
                formatted = f"{resistance/1000:.1f} kΩ"
            else:
                formatted = f"{resistance:.0f} Ω"
            
            self.resistor_result.text = f"Hodnota: {formatted}\nTolerancia: ±{tol}%"
            
        except Exception as e:
            self.resistor_result.text = f"Chyba: {str(e)}"


class PowerCalculatorTab(BoxLayout):
    """Tab for power and current calculations at different voltages"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = dp(20)
        self.spacing = dp(15)
        self.create_power_view()
    
    def create_power_view(self):
        """Create power calculator interface"""
        # Title
        title = Label(
            text="Výpočet výkonu a prúdu",
            color=get_color_from_hex('#ff8c00'),
            font_size='20sp',
            bold=True,
            size_hint_y=None,
            height=dp(40)
        )
        self.add_widget(title)
        
        # Input section
        input_layout = GridLayout(cols=2, spacing=dp(10), size_hint_y=None, height=dp(100))
        
        input_layout.add_widget(Label(text="Výkon (W):", color=get_color_from_hex('#ffffff'), font_size='14sp'))
        self.power_input = TextInput(
            hint_text="Zadajte výkon v W",
            multiline=False,
            font_size='16sp',
            background_color=get_color_from_hex('#2d2d2d'),
            foreground_color=get_color_from_hex('#ffffff')
        )
        input_layout.add_widget(self.power_input)
        
        input_layout.add_widget(Label(text="Napätie (V):", color=get_color_from_hex('#ffffff'), font_size='14sp'))
        self.voltage_calc_input = TextInput(
            hint_text="Napríklad: 230",
            multiline=False,
            font_size='16sp',
            background_color=get_color_from_hex('#2d2d2d'),
            foreground_color=get_color_from_hex('#ffffff')
        )
        input_layout.add_widget(self.voltage_calc_input)
        
        self.add_widget(input_layout)
        
        # Calculate button
        calc_btn = Button(
            text="Vypočítať prúd",
            size_hint_y=None,
            height=dp(50),
            background_color=get_color_from_hex('#ff8c00'),
            color=get_color_from_hex('#1a1a1a'),
            font_size='16sp',
            bold=True
        )
        calc_btn.bind(on_press=self.calculate_current)
        self.add_widget(calc_btn)
        
        # Multi-voltage button
        multi_btn = Button(
            text="Tabuľka pre bežné napätia",
            size_hint_y=None,
            height=dp(50),
            background_color=get_color_from_hex('#666666'),
            color=get_color_from_hex('#ffffff'),
            font_size='14sp'
        )
        multi_btn.bind(on_press=self.show_voltage_table)
        self.add_widget(multi_btn)
        
        # Result
        self.power_result = Label(
            text="Zadajte výkon a napätie pre výpočet prúdu",
            color=get_color_from_hex('#ffffff'),
            font_size='16sp',
            text_size=(None, None),
            halign='center'
        )
        self.power_result.bind(size=self.power_result.setter('text_size'))
        self.add_widget(self.power_result)
    
    def calculate_current(self, instance):
        """Calculate current from power and voltage"""
        try:
            power = float(self.power_input.text)
            voltage = float(self.voltage_calc_input.text)
            
            if voltage == 0:
                self.power_result.text = "Chyba: Napätie nemôže byť nula!"
                return
            
            current = power / voltage
            
            # Format current
            if current >= 1:
                current_str = f"{current:.2f} A"
            else:
                current_str = f"{current*1000:.0f} mA"
            
            self.power_result.text = f"Pre {power} W pri {voltage} V:\nPrúd = {current_str}"
            
        except ValueError:
            self.power_result.text = "Chyba: Zadajte platné číselné hodnoty!"
        except Exception as e:
            self.power_result.text = f"Chyba: {str(e)}"
    
    def show_voltage_table(self, instance):
        """Show table for common voltages"""
        try:
            power = float(self.power_input.text)
            
            voltages = [12, 24, 110, 230, 400]
            results = []
            
            for voltage in voltages:
                current = power / voltage
                if current >= 1:
                    current_str = f"{current:.2f} A"
                else:
                    current_str = f"{current*1000:.0f} mA"
                results.append(f"{voltage}V >> {current_str}")
            
            self.power_result.text = f"Pre {power} W:\n" + "\n".join(results)
            
        except ValueError:
            self.power_result.text = "Najprv zadajte výkon v W!"
        except Exception as e:
            self.power_result.text = f"Chyba: {str(e)}"


class WireTableTab(BoxLayout):
    """Tab for wire ampacity table"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = dp(20)
        self.spacing = dp(15)
        self.create_wire_view()
    
    def create_wire_view(self):
        """Create wire ampacity table interface"""
        # Title
        title = Label(
            text="Tabuľka istenia vodičov",
            color=get_color_from_hex('#ff8c00'),
            font_size='20sp',
            bold=True,
            size_hint_y=None,
            height=dp(40)
        )
        self.add_widget(title)
        
        # Subtitle
        subtitle = Label(
            text="Maximálny dovolený prúd pre Cu vodiče (30°C)",
            color=get_color_from_hex('#ffffff'),
            font_size='14sp',
            size_hint_y=None,
            height=dp(30)
        )
        self.add_widget(subtitle)
        
        # Wire data
        wire_data = [
            ("1.5", "16", "19"),
            ("2.5", "25", "27"),
            ("4", "35", "38"),
            ("6", "46", "50"),
            ("10", "63", "69"),
            ("16", "85", "92"),
            ("25", "112", "119"),
            ("35", "138", "147"),
            ("50", "171", "179"),
            ("70", "218", "229"),
            ("95", "266", "278"),
            ("120", "309", "321"),
            ("150", "357", "370"),
            ("185", "415", "430"),
            ("240", "488", "504"),
            ("300", "566", "583")
        ]
        
        # ScrollView for table
        scroll = ScrollView(
            do_scroll_x=False,
            do_scroll_y=True,
            bar_width=dp(8),
            bar_color=get_color_from_hex('#ff8c00')
        )
        
        # Table layout
        table_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(2),
            size_hint_y=None,
            padding=[dp(5), dp(5), dp(5), dp(5)]
        )
        table_layout.bind(minimum_height=table_layout.setter('height'))
        
        # Header
        header = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40))
        header.add_widget(Label(
            text="Prierez\n[mm²]",
            color=get_color_from_hex('#ff8c00'),
            font_size='14sp',
            bold=True,
            text_size=(None, None),
            halign='center'
        ))
        header.add_widget(Label(
            text="V zemi\n[A]",
            color=get_color_from_hex('#ff8c00'),
            font_size='14sp',
            bold=True,
            text_size=(None, None),
            halign='center'
        ))
        header.add_widget(Label(
            text="Vo vzduchu\n[A]",
            color=get_color_from_hex('#ff8c00'),
            font_size='14sp',
            bold=True,
            text_size=(None, None),
            halign='center'
        ))
        table_layout.add_widget(header)
        
        # Table rows
        for i, (cross_section, ground_current, air_current) in enumerate(wire_data):
            row_color = '#2d2d2d' if i % 2 == 0 else '#252525'
            row = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(35))
            
            with row.canvas.before:
                from kivy.graphics import Color, Rectangle
                Color(*get_color_from_hex(row_color))
                row.rect = Rectangle(size=row.size, pos=row.pos)
            
            def update_rect(instance, value):
                instance.rect.pos = instance.pos
                instance.rect.size = instance.size
            
            row.bind(size=update_rect, pos=update_rect)
            
            row.add_widget(Label(
                text=cross_section,
                color=get_color_from_hex('#ffffff'),
                font_size='14sp',
                halign='center'
            ))
            row.add_widget(Label(
                text=ground_current,
                color=get_color_from_hex('#ffffff'),
                font_size='14sp',
                halign='center'
            ))
            row.add_widget(Label(
                text=air_current,
                color=get_color_from_hex('#ffffff'),
                font_size='14sp',
                halign='center'
            ))
            
            table_layout.add_widget(row)
        
        scroll.add_widget(table_layout)
        self.add_widget(scroll)
        
        # Calculator section
        calc_title = Label(
            text="Výber vodiča:",
            color=get_color_from_hex('#ff8c00'),
            font_size='16sp',
            bold=True,
            size_hint_y=None,
            height=dp(30)
        )
        self.add_widget(calc_title)
        
        calc_layout = BoxLayout(orientation='horizontal', spacing=dp(10), size_hint_y=None, height=dp(50))
        
        self.current_input = TextInput(
            hint_text="Prúd (A)",
            multiline=False,
            font_size='16sp',
            background_color=get_color_from_hex('#2d2d2d'),
            foreground_color=get_color_from_hex('#ffffff'),
            size_hint_x=0.4
        )
        
        self.installation_type = Spinner(
            text='Vo vzduchu',
            values=['Vo vzduchu', 'V zemi'],
            size_hint_x=0.4,
            background_color=get_color_from_hex('#2d2d2d'),
            color=get_color_from_hex('#ffffff')
        )
        
        find_btn = Button(
            text="Nájsť",
            size_hint_x=0.2,
            background_color=get_color_from_hex('#ff8c00'),
            color=get_color_from_hex('#1a1a1a'),
            font_size='14sp',
            bold=True
        )
        find_btn.bind(on_press=self.find_wire)
        
        calc_layout.add_widget(self.current_input)
        calc_layout.add_widget(self.installation_type)
        calc_layout.add_widget(find_btn)
        self.add_widget(calc_layout)
        
        # Wire recommendation result
        self.wire_result = Label(
            text="Zadajte prúd pre odporúčanie vodiča",
            color=get_color_from_hex('#ffffff'),
            font_size='16sp',
            size_hint_y=None,
            height=dp(60),
            text_size=(None, None),
            halign='center'
        )
        self.wire_result.bind(size=self.wire_result.setter('text_size'))
        self.add_widget(self.wire_result)
        
        # Store wire data for lookup
        self.wire_data = wire_data
    
    def find_wire(self, instance):
        """Find appropriate wire for given current"""
        try:
            required_current = float(self.current_input.text)
            installation = self.installation_type.text
            
            # Determine which column to use (1=ground, 2=air)
            current_index = 1 if installation == 'V zemi' else 2
            
            recommended_wire = None
            for cross_section, ground_current, air_current in self.wire_data:
                max_current = float(ground_current) if current_index == 1 else float(air_current)
                if max_current >= required_current:
                    recommended_wire = cross_section
                    break
            
            if recommended_wire:
                self.wire_result.text = f"Pre prúd {required_current} A ({installation}):\nOdporúčaný prierez: {recommended_wire} mm²"
            else:
                self.wire_result.text = f"Pre prúd {required_current} A je potrebný\nvodič s priereezom > 300 mm²"
                
        except ValueError:
            self.wire_result.text = "Chyba: Zadajte platný prúd v A!"
        except Exception as e:
            self.wire_result.text = f"Chyba: {str(e)}"


class UnitConverterTab(BoxLayout):
    """Tab for unit conversion"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = dp(20)
        self.spacing = dp(15)
        self.create_converter_view()
    
    def create_converter_view(self):
        """Create unit converter interface"""
        # Title
        title = Label(
            text="Prevodník elektrických jednotiek",
            color=get_color_from_hex('#ff8c00'),
            font_size='20sp',
            bold=True,
            size_hint_y=None,
            height=dp(40)
        )
        self.add_widget(title)
        
        # Input section
        input_layout = BoxLayout(orientation='horizontal', spacing=dp(10), size_hint_y=None, height=dp(50))
        
        self.input_value = TextInput(
            hint_text="Zadajte hodnotu",
            multiline=False,
            font_size='16sp',
            background_color=get_color_from_hex('#2d2d2d'),
            foreground_color=get_color_from_hex('#ffffff'),
            size_hint_x=0.4
        )
        
        self.from_unit = Spinner(
            text='V',
            values=['V', 'kV', 'mV', 'A', 'mA', 'kA', 'W', 'kW', 'MW', 'Ω', 'kΩ', 'MΩ', 'Hz', 'kHz', 'MHz'],
            size_hint_x=0.25,
            background_color=get_color_from_hex('#2d2d2d'),
            color=get_color_from_hex('#ffffff')
        )
        
        arrow_label = Label(
            text=">>", 
            color=get_color_from_hex('#ff8c00'), 
            font_size='20sp', 
            bold=True,
            size_hint_x=0.1
        )
        
        self.to_unit = Spinner(
            text='mV',
            values=['V', 'kV', 'mV', 'A', 'mA', 'kA', 'W', 'kW', 'MW', 'Ω', 'kΩ', 'MΩ', 'Hz', 'kHz', 'MHz'],
            size_hint_x=0.25,
            background_color=get_color_from_hex('#2d2d2d'),
            color=get_color_from_hex('#ffffff')
        )
        
        input_layout.add_widget(self.input_value)
        input_layout.add_widget(self.from_unit)
        input_layout.add_widget(arrow_label)
        input_layout.add_widget(self.to_unit)
        self.add_widget(input_layout)
        
        # Convert button
        convert_btn = Button(
            text="Previesť",
            size_hint_y=None,
            height=dp(50),
            background_color=get_color_from_hex('#ff8c00'),
            color=get_color_from_hex('#1a1a1a'),
            font_size='16sp',
            bold=True
        )
        convert_btn.bind(on_press=self.convert_units)
        self.add_widget(convert_btn)
        
        # Result
        self.result_label = Label(
            text="Výsledok sa zobrazí tu",
            color=get_color_from_hex('#ffffff'),
            font_size='18sp',
            size_hint_y=None,
            height=dp(60)
        )
        self.add_widget(self.result_label)
        
        # Add conversion table
        self.add_conversion_table()
    
    def convert_units(self, instance):
        """Convert between units"""
        try:
            value = float(self.input_value.text)
            from_unit = self.from_unit.text
            to_unit = self.to_unit.text
            
            # Conversion factors to base units
            conversions = {
                'V': 1, 'kV': 1000, 'mV': 0.001,
                'A': 1, 'mA': 0.001, 'kA': 1000,
                'W': 1, 'kW': 1000, 'MW': 1000000,
                'Ω': 1, 'kΩ': 1000, 'MΩ': 1000000,
                'Hz': 1, 'kHz': 1000, 'MHz': 1000000
            }
            
            # Check if units are compatible
            voltage_units = ['V', 'kV', 'mV']
            current_units = ['A', 'mA', 'kA']
            power_units = ['W', 'kW', 'MW']
            resistance_units = ['Ω', 'kΩ', 'MΩ']
            frequency_units = ['Hz', 'kHz', 'MHz']
            
            unit_groups = [voltage_units, current_units, power_units, resistance_units, frequency_units]
            
            compatible = False
            for group in unit_groups:
                if from_unit in group and to_unit in group:
                    compatible = True
                    break
            
            if not compatible:
                self.result_label.text = "Chyba: Nekompatibilné jednotky!"
                return
            
            # Convert
            base_value = value * conversions[from_unit]
            result = base_value / conversions[to_unit]
            
            self.result_label.text = f"{value} {from_unit} = {result:.6g} {to_unit}"
            
        except ValueError:
            self.result_label.text = "Chyba: Zadajte platnú číselnou hodnotu!"
        except Exception as e:
            self.result_label.text = f"Chyba: {str(e)}"
    
    def add_conversion_table(self):
        """Add quick conversion reference table"""
        table_title = Label(
            text="Rýchly prehľad prevodov:",
            color=get_color_from_hex('#ff8c00'),
            font_size='16sp',
            bold=True,
            size_hint_y=None,
            height=dp(30)
        )
        self.add_widget(table_title)
        
        conversions_text = """1 kV = 1000 V = 1,000,000 mV
1 A = 1000 mA = 0.001 kA
1 kW = 1000 W = 0.001 MW
1 MΩ = 1000 kΩ = 1,000,000 Ω
1 MHz = 1000 kHz = 1,000,000 Hz"""
        
        table_label = Label(
            text=conversions_text,
            color=get_color_from_hex('#ffffff'),
            font_size='12sp',
            text_size=(None, None),
            halign='left'
        )
        table_label.bind(size=table_label.setter('text_size'))
        self.add_widget(table_label)


class OhmsLawTab(BoxLayout):
    """Tab for Ohm's law calculations"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = dp(20)
        self.spacing = dp(15)
        self.create_ohms_law_view()
    
    def create_ohms_law_view(self):
        """Create Ohm's law calculator interface"""
        # Title
        title = Label(
            text="Ohmov zákon - Kalkulátor",
            color=get_color_from_hex('#ff8c00'),
            font_size='20sp',
            bold=True,
            size_hint_y=None,
            height=dp(40)
        )
        self.add_widget(title)
        
        # Formula display
        formula_label = Label(
            text="U = I × R    |    P = U × I    |    P = I² × R    |    P = U² / R",
            color=get_color_from_hex('#ffffff'),
            font_size='14sp',
            size_hint_y=None,
            height=dp(30)
        )
        self.add_widget(formula_label)
        
        # Input fields
        inputs_layout = GridLayout(cols=2, spacing=dp(10), size_hint_y=None, height=dp(200))
        
        # Voltage input
        inputs_layout.add_widget(Label(text="Napätie (U) [V]:", color=get_color_from_hex('#ffffff'), font_size='14sp'))
        self.voltage_input = TextInput(
            hint_text="V",
            multiline=False,
            font_size='16sp',
            background_color=get_color_from_hex('#2d2d2d'),
            foreground_color=get_color_from_hex('#ffffff')
        )
        inputs_layout.add_widget(self.voltage_input)
        
        # Current input
        inputs_layout.add_widget(Label(text="Prúd (I) [A]:", color=get_color_from_hex('#ffffff'), font_size='14sp'))
        self.current_input = TextInput(
            hint_text="A",
            multiline=False,
            font_size='16sp',
            background_color=get_color_from_hex('#2d2d2d'),
            foreground_color=get_color_from_hex('#ffffff')
        )
        inputs_layout.add_widget(self.current_input)
        
        # Resistance input
        inputs_layout.add_widget(Label(text="Odpor (R) [Ω]:", color=get_color_from_hex('#ffffff'), font_size='14sp'))
        self.resistance_input = TextInput(
            hint_text="Ω",
            multiline=False,
            font_size='16sp',
            background_color=get_color_from_hex('#2d2d2d'),
            foreground_color=get_color_from_hex('#ffffff')
        )
        inputs_layout.add_widget(self.resistance_input)
        
        # Power input
        inputs_layout.add_widget(Label(text="Výkon (P) [W]:", color=get_color_from_hex('#ffffff'), font_size='14sp'))
        self.power_input = TextInput(
            hint_text="W",
            multiline=False,
            font_size='16sp',
            background_color=get_color_from_hex('#2d2d2d'),
            foreground_color=get_color_from_hex('#ffffff')
        )
        inputs_layout.add_widget(self.power_input)
        
        self.add_widget(inputs_layout)
        
        # Calculate button
        calc_btn = Button(
            text="Vypočítať",
            size_hint_y=None,
            height=dp(50),
            background_color=get_color_from_hex('#ff8c00'),
            color=get_color_from_hex('#1a1a1a'),
            font_size='16sp',
            bold=True
        )
        calc_btn.bind(on_press=self.calculate_ohms_law)
        self.add_widget(calc_btn)
        
        # Clear button
        clear_btn = Button(
            text="Vymazať všetko",
            size_hint_y=None,
            height=dp(40),
            background_color=get_color_from_hex('#666666'),
            color=get_color_from_hex('#ffffff'),
            font_size='14sp'
        )
        clear_btn.bind(on_press=self.clear_inputs)
        self.add_widget(clear_btn)
        
        # Results
        self.results_label = Label(
            text="Zadajte aspoň 2 hodnoty pre výpočet",
            color=get_color_from_hex('#ffffff'),
            font_size='16sp',
            text_size=(None, None),
            halign='center'
        )
        self.results_label.bind(size=self.results_label.setter('text_size'))
        self.add_widget(self.results_label)
    
    def calculate_ohms_law(self, instance):
        """Calculate missing values using Ohm's law"""
        try:
            # Get input values
            voltage = self.get_float_value(self.voltage_input.text)
            current = self.get_float_value(self.current_input.text)
            resistance = self.get_float_value(self.resistance_input.text)
            power = self.get_float_value(self.power_input.text)
            
            values = [voltage, current, resistance, power]
            known_count = sum(1 for v in values if v is not None)
            
            if known_count < 2:
                self.results_label.text = "Chyba: Zadajte aspoň 2 hodnoty!"
                return
            
            # --- Calculation Logic ---
            calc_values = {'U': voltage, 'I': current, 'R': resistance, 'P': power}
            
            for _ in range(2): 
                # U
                if calc_values['U'] is None:
                    if calc_values['I'] is not None and calc_values['R'] is not None:
                        calc_values['U'] = calc_values['I'] * calc_values['R']
                    elif calc_values['P'] is not None and calc_values['I'] is not None and calc_values['I'] != 0:
                        calc_values['U'] = calc_values['P'] / calc_values['I']
                    elif calc_values['P'] is not None and calc_values['R'] is not None and calc_values['P'] >= 0 and calc_values['R'] >= 0:
                        calc_values['U'] = (calc_values['P'] * calc_values['R']) ** 0.5
                
                # I
                if calc_values['I'] is None:
                    if calc_values['U'] is not None and calc_values['R'] is not None and calc_values['R'] != 0:
                        calc_values['I'] = calc_values['U'] / calc_values['R']
                    elif calc_values['P'] is not None and calc_values['U'] is not None and calc_values['U'] != 0:
                        calc_values['I'] = calc_values['P'] / calc_values['U']
                    elif calc_values['P'] is not None and calc_values['R'] is not None and calc_values['P'] >= 0 and calc_values['R'] > 0:
                        calc_values['I'] = (calc_values['P'] / calc_values['R']) ** 0.5

                # R
                if calc_values['R'] is None:
                    if calc_values['U'] is not None and calc_values['I'] is not None and calc_values['I'] != 0:
                        calc_values['R'] = calc_values['U'] / calc_values['I']
                    elif calc_values['P'] is not None and calc_values['I'] is not None and calc_values['I'] != 0:
                        calc_values['R'] = calc_values['P'] / (calc_values['I'] ** 2)
                    elif calc_values['P'] is not None and calc_values['U'] is not None and calc_values['P'] != 0:
                        calc_values['R'] = (calc_values['U'] ** 2) / calc_values['P']
                
                # P
                if calc_values['P'] is None:
                    if calc_values['U'] is not None and calc_values['I'] is not None:
                        calc_values['P'] = calc_values['U'] * calc_values['I']
                    elif calc_values['I'] is not None and calc_values['R'] is not None:
                        calc_values['P'] = (calc_values['I'] ** 2) * calc_values['R']
                    elif calc_values['U'] is not None and calc_values['R'] is not None and calc_values['R'] != 0:
                        calc_values['P'] = (calc_values['U'] ** 2) / calc_values['R']

            # --- Display Results ---
            results_text = []
            if calc_values['U'] is not None:
                self.voltage_input.text = f"{calc_values['U']:.3g}"
            if calc_values['I'] is not None:
                self.current_input.text = f"{calc_values['I']:.3g}"
            if calc_values['R'] is not None:
                self.resistance_input.text = f"{calc_values['R']:.3g}"
            if calc_values['P'] is not None:
                self.power_input.text = f"{calc_values['P']:.3g}"

            # Update results label after filling inputs
            final_known_count = sum(1 for v in calc_values.values() if v is not None)
            if final_known_count == 4:
                self.results_label.text = (f"Napätie: {calc_values['U']:.4g} V\n"
                                           f"Prúd: {calc_values['I']:.4g} A\n"
                                           f"Odpor: {calc_values['R']:.4g} Ω\n"
                                           f"Výkon: {calc_values['P']:.4g} W")
            else:
                self.results_label.text = "Nemožno vypočítať všetky hodnoty.\nSkontrolujte zadané vstupy."

        except (ValueError, TypeError):
            self.results_label.text = "Chyba: Zadajte platné číselné hodnoty!"
        except ZeroDivisionError:
            self.results_label.text = "Chyba: Delenie nulou! Skontrolujte vstupy."
        except Exception as e:
            self.results_label.text = f"Nastala neočakávaná chyba: {str(e)}"

    def get_float_value(self, text):
        """Convert text to float or return None"""
        if not text or text.strip() == "":
            return None
        try:
            return float(text.replace(',', '.'))
        except ValueError:
            return None
    
    def clear_inputs(self, instance):
        """Clear all input fields and results"""
        self.voltage_input.text = ""
        self.current_input.text = ""
        self.resistance_input.text = ""
        self.power_input.text = ""
        self.results_label.text = "Zadajte aspoň 2 hodnoty pre výpočet"


class ElectricalHelperApp(App):
    """Main application class"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Application window title
        self.title = "Elektrotechnický pomocník"
        self.symbols = {
            1: "Zásuvka (všeobecná značka)", 2: "Zásuvkové spojenie", 3: "Zásuvka zapojená z krabicovej rozvodky",
            4: "Zásuvka (priebežné zapojenie)", 5: "Dvojitá zásuvka", 6: "Zásuvka s nezameniteľnými kontaktmi",
            7: "Telefónna zásuvka", 8: "Anténna zásuvka", 9: "Žiarovkové svietidlo", 10: "Žiarovkové svietidlo nástenné",
            11: "Žiarovkové svietidlo so spínačom", 12: "Núdzové osvetlenie", 13: "Žiarovkový svetlomet",
            14: "Žiarivkové svietidlo", 15: "Žiarivkové svietidlo so žiarovkou", 16: "Halogénové svietidlo",
            17: "Halogénový svetlomet", 18: "Žiarovka, signálka", 19: "Spínač jednopólový č.1",
            20: "Spínač dvojpólový č.2", 21: "Spínač trojpólový č.3", 22: "Striedavý prepínač č.6",
            23: "Sériový prepínač č.5", 24: "Krížový prepínač č.7", 25: "Sériový prepínač striedavý č.5A",
            26: "Dvojitý prepínač striedavý č.5B", 27: "Spínač so signálkou", 28: "Koncový spínač",
            29: "Odstredivý spínač", 30: "Plávačkový spínač", 31: "Tlakový spínač", 32: "Časový spínač",
            33: "Tepelný spínač (termostat)", 34: "Okrúhla krabica", 35: "Krabica (rozvodná skriňa)",
            36: "Okrúhla odbočná alebo spoj", 37: "Svorka", 38: "Tlačidlový ovládač", 39: "Tlačidlový ovládač dvojitý",
            40: "Signálka", 41: "Tlačidlo so signálkou", 42: "Zvonček", 43: "Domový telefón s tlačidlom",
            44: "Domový telefón", 45: "Húkačka", 46: "Siréna", 47: "Reproduktor", 48: "Kamera", 49: "Mikrofón",
            50: "Spoločná anténa", 51: "Elektrický zámok", 52: "Tepelný spotrebič", 53: "Motor",
            54: "Zariadenie s elektrickým motorom", 55: "Zariadenie s motorom aj el. kúrením", 56: "Infražiarič",
            57: "Bojler", 58: "Ventilátor", 59: "Sušička", 60: "Práčka", 61: "Umývačka riadu", 63: "El. sporák",
            64: "Chladnička", 65: "Transformátor", 66: "Regulačný odpor", 67: "Kondenzátorová batéria",
            68: "Usmerňovač", 69: "Batéria", 70: "Zosilňovač", 71: "Záchytná tyč", 72: "Vodivé spojenie",
            73: "Skúšobná svorka", 74: "Skúšobná svorka v skriňke", 75: "Hromozvádzač", 76: "Iskrisko", 77: "Uzemnenie",
            78: "Doskový zemník", 79: "Tyčový zemník", 80: "Lúčový zemník", 81: "Uzemnenie", 82: "Bezšumová zem",
            83: "Uzemnenie ochranné", 84: "Spojenie s kostrou", 85: "Spojenie s kostrou", 86: "Ekvipotenciál",
            87: "Počet pólov, žíl", 88: "Vodič PEN", 89: "Stredný vodič N", 90: "Ochranný vodič PE",
            91: "Stúpacie vedenie", 92: "Vedenie v trubkách", 93: "Vedenie v izolátoroch", 94: "Vedenie na povrchu",
            95: "Vedenie pod omietkou", 96: "Vedenie v podlahe", 97: "Vedenie v podlahovej lište",
            98: "Vedenie v kanáli", 99: "Vedenie po rošte", 100: "Vedenie na podperách", 101: "Vedenie v zemi",
            102: "Vonkajšie vedenie na podperkách", 103: "Závesný kábel", 104: "Samonosný kábel",
            105: "Jednopólový istič (FA)", 106: "Dvojpólový istič (FA)", 107: "Trojfázový istič (FA)",
            108: "Poisky (FU)", 109: "Poistkový spínač", 110: "Poistkový odpojovač", 111: "Prerážka",
            112: "Prúdový chránič", 113: "Prepäťová ochrana", 114: "+ obmedzovacia impedancia",
            115: "Tepelná ochrana (R100 ap.)", 116: "Kontakt stýkača - spínací", 117: "Kontakt stýkača - rozpínací",
            118: "Cievka stýkača (KM)", 119: "Pomocný kontakt zapínací", 120: "Pomocný kontakt vypínací",
            121: "Spínač (SV)", 122: "Termostat (ST)", 123: "Relé (KR, KA)", 124: "Cievka relé (KR, KA)",
            125: "Odpojovač", 126: "Odpínač", 127: "Otočný spínač", 128: "Stýkací spínač", 129: "Odpojovač",
            130: "Odpínač", 131: "So spoždeným návratom", 132: "So spoždeným nábeihom", 133: "Termostat (ST)",
            134: "Tlakový spínač (SP)", 135: "Koncový spínač (SQ)", 136: "Koncový spínač (SQ)",
            137: "Pneumatické a hydraulické ovládanie", 138: "Ovládanie vačkou", 139: "Ovládanie elektromotorm",
            140: "Ovládanie membránou", 141: "Ovládanie plávačkoin (BC)", 142: "Ovládanie odstredivým regulátorom",
            143: "Ovládanie riadiacim kolesom", 144: "Ovládanie pákoui", 145: "Ovládanie špeciálnym kľúčom",
            146: "Ovládanie prúdením", 147: "Ovládanie nohou", 148: "EP ventil (YV)", 149: "Jednoduché",
            150: "Prepínací kontakt", 151: "Kontakt s predstihom", 152: "Kontakt so spoždením",
            153: "Vypínací kontakt s predstihom", 154: "Vypínací kontakt so spoždením", 155: "Tlačidlo zapínací (SB)",
            156: "Tlačidlo vypínací (SB)", 157: "Ťahový ovládač", 158: "Ťahový s vypínacím kontaktom",
            159: "Otočný ovládač (SA)", 160: "Otočný s vypínacím kontaktom", 161: "Motor striedavý",
            162: "Motor jednosmerný", 163: "Kotva jednosmerného motora", 164: "Vinutie jednosmerného motora",
            165: "Generátor", 166: "Dynamo", 167: "Cievka, vinutie", 168: "Transformátor (T)",
            169: "Vysielač teploty (BT)", 170: "Vysielač tlaku (BP)", 171: "Snímač otáčok (BP)",
            172: "Termoelektrický článok", 173: "Voltmeter (PU)", 174: "Ampérmeter (PA)", 175: "Wattmeter",
            176: "Frekvencmer", 177: "Otáčkomer", 178: "Bočník (RM)", 179: "Meraciý transformátor prúdu",
            180: "Elektrické hodiny", 181: "Počítadlo impulzov", 182: "Elektromer (ET)", 183: "Transformátor (VT)",
            184: "Dióda (VD)", 185: "Zenerová dióda (VHL)", 186: "LED dióda (HL)", 187: "Odpor", 188: "Potenciometer",
            189: "Trimmer", 190: "Kondenzátor", 191: "Elektrolytický kondenzátor", 192: "Transformovňa",
            193: "Usmerňovacia stanica", 194: "Zastrešená elektrická stanica", 195: "Zapúzdrená elektrická stanica",
            196: "Stožiarová transformovňa", 197: "Hromozvádzač", 198: "Vyfukovací hromozvádzač",
            199: "Ventilový hromozvádzač", 200: "Vákuový hromozvádzač", 201: "Výbojový hromozvádzač",
            202: "Stožiar drevený", 203: "Stožiar oceľový", 204: "Stožiar príhradový", 205: "Stožiar železobetónový",
            206: "Stožiar portálový", 207: "Stožiar s dvojitým závesom", 208: "Stožiar s kovovými reťazami",
            209: "Kotvenie stožiara pätkou", 210: "Kotvenie stožiara kotvou", 211: "Nástenná konzola priebežná",
            212: "Nástenná konzola odbočná", 213: "Upevnenie hákami na jednej strane",
            214: "Upevnenie konzoly na jednej strane", 215: "Tlmič kmitov", 216: "Kondenzátorová batéria",
            217: "Pupinačná cievka", 218: "Svietidlo", 219: "Rozhlas"
        }
    
    def build(self):
        """Build main interface with tabs"""
        main_layout = BoxLayout(orientation='vertical')
        
        header = BoxLayout(
            orientation='horizontal', size_hint_y=None, height=dp(80),
            padding=[dp(20), dp(15), dp(20), dp(15)]
        )
        
        with header.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(*get_color_from_hex('#1a1a1a'))
            header.rect = Rectangle(size=header.size, pos=header.pos)
        header.bind(size=self._update_header_rect, pos=self._update_header_rect)
        
        # Main application heading
        title_label = Label(
            text="Elektrotechnický pomocník",
            color=get_color_from_hex('#ff8c00'), font_size='22sp', bold=True,
            halign='center', valign='middle'
        )
        title_label.bind(size=title_label.setter('text_size'))
        header.add_widget(title_label)
        
        main_layout.add_widget(header)
        
        tab_panel = TabbedPanel(
            do_default_tab=False, background_color=get_color_from_hex('#1a1a1a'),
            border=[0, 0, 0, 0], tab_height=dp(50), tab_width=dp(120),
            tab_pos='top_mid', background_image=''
        )
        
        # --- IMPLEMENTATION OF ACTIVE TAB HIGHLIGHTING ---
        # Common properties for ALL tabs
        tab_item_props = {
            'background_normal': '',  # Disable the default image (important for showing the color)
            'background_down': '',    # Disable the default image for the active state
            'background_color': get_color_from_hex('#2d2d2d'), # Color of the INACTIVE tab
            'color': get_color_from_hex('#ffffff'),
            'font_size': '14sp'
        }

        # Color for the ACTIVE tab
        active_tab_color = get_color_from_hex('#ff8c00')
        
        # Creating individual tabs with color settings
        symbols_tab = TabbedPanelItem(text='Značky', **tab_item_props)
        symbols_tab.background_color_down = active_tab_color # Sets the color for the active state
        symbols_tab.add_widget(SymbolsTab(self.symbols))
        
        converter_tab = TabbedPanelItem(text='Prevodník', **tab_item_props)
        converter_tab.background_color_down = active_tab_color
        converter_tab.add_widget(UnitConverterTab())
        
        resistor_tab = TabbedPanelItem(text='Rezistory', **tab_item_props)
        resistor_tab.background_color_down = active_tab_color
        resistor_tab.add_widget(ResistorColorCodeTab())
        
        power_tab = TabbedPanelItem(text='Výkon', **tab_item_props)
        power_tab.background_color_down = active_tab_color
        power_tab.add_widget(PowerCalculatorTab())
        
        wire_tab = TabbedPanelItem(text='Vodiče', **tab_item_props)
        wire_tab.background_color_down = active_tab_color
        wire_tab.add_widget(WireTableTab())
        
        ohms_tab = TabbedPanelItem(text='Ohmov zákon', **tab_item_props)
        ohms_tab.background_color_down = active_tab_color
        ohms_tab.add_widget(OhmsLawTab())
        
        # Adding tabs to the panel
        tab_panel.add_widget(symbols_tab)
        tab_panel.add_widget(converter_tab)
        tab_panel.add_widget(resistor_tab)
        tab_panel.add_widget(power_tab)
        tab_panel.add_widget(wire_tab)
        tab_panel.add_widget(ohms_tab)
        
        tab_panel.default_tab = symbols_tab
        main_layout.add_widget(tab_panel)
        
        return main_layout
    
    def _update_header_rect(self, instance, value):
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size

if __name__ == '__main__':
    ElectricalHelperApp().run()
