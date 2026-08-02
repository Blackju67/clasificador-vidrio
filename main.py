import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

class GlassFuzzyApp(App):
    def build(self):
        root = BoxLayout(orientation='vertical', padding=15, spacing=10)
        title = Label(text="Clasificador de Tipo de Vidrio", font_size='20sp', bold=True, size_hint=(1, None), height=40)
        root.add_widget(title)

        scroll = ScrollView(size_hint=(1, 1))
        grid = GridLayout(cols=2, spacing=10, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))

        self.inputs = {}
        campos = [
            ("1. Refracción (1.511-1.534)", "ref", "1.518"),
            ("2. Sodio (10.73-17.38)", "sod", "13.2"),
            ("3. Magnesio (0-4.49)", "mag", "3.6"),
            ("4. Aluminio (0.34-3.5)", "al", "1.2"),
            ("5. Silicio (69.81-75.41)", "sil", "72.5"),
            ("6. Potasio (0-6.21)", "p", "0.5"),
            ("7. Calcio (5.43-16.19)", "ca", "8.5"),
            ("8. Bario (0-3.15)", "ba", "0.0"),
            ("9. Hierro (0-0.51)", "h", "0.1")
        ]

        for label_text, key, default_val in campos:
            lbl = Label(text=label_text, font_size='14sp', size_hint_y=None, height=40)
            txt = TextInput(text=default_val, input_filter='float', multiline=False, size_hint_y=None, height=40)
            self.inputs[key] = txt
            grid.add_widget(lbl)
            grid.add_widget(txt)

        scroll.add_widget(grid)
        root.add_widget(scroll)

        btn_calc = Button(text="CLASIFICAR VIDRIO", font_size='16sp', bold=True, size_hint=(1, None), height=50)
        btn_calc.bind(on_press=self.evaluar_sistema_difuso)
        root.add_widget(btn_calc)

        self.lbl_resultado = Label(text="Ingrese los datos y presione Clasificar", font_size='15sp', bold=True, size_hint=(1, None), height=70)
        root.add_widget(self.lbl_resultado)
        return root

    def trapmf(self, x, abcd):
        a, b, c, d = abcd
        if x <= a or x >= d: return 0.0
        elif a < x < b: return (x - a) / (b - a + 1e-6)
        elif b <= x <= c: return 1.0
        elif c < x < d: return (d - x) / (d - c + 1e-6)
        return 0.0

    def trimf(self, x, abc):
        a, b, c = abc
        if x <= a or x >= c: return 0.0
        elif a < x <= b: return (x - a) / (b - a + 1e-6)
        elif b < x < c: return (c - x) / (c - b + 1e-6)
        return 0.0

    def evaluar_sistema_difuso(self, instance):
        try:
            val_ref, val_sod, val_mag = float(self.inputs['ref'].text), float(self.inputs['sod'].text), float(self.inputs['mag'].text)
            val_al, val_sil, val_p = float(self.inputs['al'].text), float(self.inputs['sil'].text), float(self.inputs['p'].text)
            val_ca, val_ba, val_h = float(self.inputs['ca'].text), float(self.inputs['ba'].text), float(self.inputs['h'].text)
        except ValueError:
            self.lbl_resultado.text = "Error: Ingrese valores numéricos válidos."
            return

        ref_n_baja, ref_n_medio, ref_n_alta = self.trapmf(val_ref, [1.511, 1.511, 1.516, 1.52]), self.trimf(val_ref, [1.516, 1.52, 1.529]), self.trapmf(val_ref, [1.52, 1.529, 1.534, 1.534])
        sod_n_bajo, sod_n_medio, sod_n_alto = self.trapmf(val_sod, [10.73, 10.73, 12.71, 13.479]), self.trimf(val_sod, [12.71, 13.479, 14.606]), self.trapmf(val_sod, [13.479, 14.606, 17.38, 17.38])
        mag_n_bajo, mag_n_medio, mag_n_alto = self.trapmf(val_mag, [0, 0, 0.116, 2.014]), self.trimf(val_mag, [0.116, 2.014, 3.54]), self.trapmf(val_mag, [2.014, 3.54, 4.49, 4.49])
        al_n_bajo, al_n_medio, al_n_alto = self.trapmf(val_al, [0.34, 0.34, 1.109, 1.686]), self.trimf(val_al, [1.109, 1.686, 2.796]), self.trapmf(val_al, [1.686, 2.796, 3.5, 3.5])
        sil_n_bajo, sil_n_medio, sil_n_alto = self.trapmf(val_sil, [69.81, 69.81, 70.402, 72.446]), self.trimf(val_sil, [70.402, 72.446, 73.335]), self.trapmf(val_sil, [72.446, 73.335, 75.41, 75.41])
        p_n_bajo, p_n_medio, p_n_alto = self.trapmf(val_p, [0, 0, 0.344, 1.839]), self.trimf(val_p, [0.344, 1.839, 5.766]), self.trapmf(val_p, [1.839, 5.766, 6.21, 6.21])
        ca_n_bajo, ca_n_medio, ca_n_alto = self.trapmf(val_ca, [5.43, 5.43, 8.076, 9.269]), self.trimf(val_ca, [8.076, 9.269, 11.846]), self.trapmf(val_ca, [9.269, 11.846, 16.19, 16.19])
        ba_n_bajo, ba_n_medio, ba_n_alto = self.trapmf(val_ba, [0, 0, 0.061, 1.623]), self.trimf(val_ba, [0.061, 1.623, 3.015]), self.trapmf(val_ba, [1.623, 3.015, 3.15, 3.15])
        h_n_bajo, h_n_medio, h_n_alto = self.trapmf(val_h, [0, 0, 0.012, 0.212]), self.trimf(val_h, [0.012, 0.212, 0.43]), self.trapmf(val_h, [0.212, 0.43, 0.51, 0.51])

        act = {1: 0.0, 2: 0.0, 3: 0.0, 4: 0.0, 5: 0.0, 6: 0.0}
        act[4] = max(act[4], min(sod_n_bajo, mag_n_bajo), min(sod_n_medio, mag_n_bajo), min(sod_n_bajo, mag_n_medio))
        act[5] = max(act[5], min(sod_n_alto, mag_n_bajo, al_n_bajo), min(sod_n_medio, mag_n_medio), min(ref_n_baja, sod_n_alto, mag_n_medio, sil_n_medio), min(ref_n_medio, sod_n_alto, mag_n_medio, sil_n_medio), min(sod_n_alto, mag_n_medio, sil_n_alto), min(mag_n_bajo, p_n_bajo, ba_n_medio))
        act[6] = max(act[6], min(sod_n_alto, mag_n_bajo, al_n_medio), min(sod_n_alto, mag_n_bajo, al_n_alto), min(sod_n_alto, mag_n_medio, sil_n_bajo), min(ref_n_alta, sod_n_medio, mag_n_alto, p_n_bajo, ca_n_bajo, ba_n_bajo, h_n_bajo), min(sod_n_bajo, mag_n_alto, ba_n_medio), min(sod_n_medio, mag_n_alto, ba_n_medio), min(sod_n_alto, mag_n_alto, ba_n_medio), min(sod_n_bajo, ba_n_alto), min(sod_n_medio, al_n_bajo, ba_n_alto), min(sod_n_medio, al_n_medio, ba_n_alto), min(sod_n_medio, al_n_alto, ba_n_alto), min(sod_n_alto, ba_n_alto))
        act[1] = max(act[1], min(ref_n_baja, sod_n_bajo, mag_n_alto, ca_n_bajo, ba_n_bajo), min(ref_n_medio, sod_n_bajo, mag_n_alto, sil_n_medio, ca_n_bajo, ba_n_bajo), min(ref_n_medio, sod_n_bajo, mag_n_alto, sil_n_alto, ca_n_bajo, ba_n_bajo), min(ref_n_medio, sod_n_medio, mag_n_alto, p_n_bajo, ca_n_bajo, ba_n_bajo, h_n_bajo), min(ref_n_baja, sod_n_medio, mag_n_alto, sil_n_alto, p_n_bajo, ca_n_bajo, ba_n_bajo, h_n_medio), min(ref_n_medio, sod_n_medio, mag_n_alto, sil_n_alto, p_n_bajo, ca_n_bajo, ba_n_bajo, h_n_medio), min(sod_n_alto, mag_n_alto, ca_n_bajo, ba_n_bajo), min(mag_n_alto, sil_n_bajo, ca_n_medio, ba_n_bajo, h_n_bajo), min(ref_n_baja, sod_n_bajo, mag_n_alto, al_n_bajo, sil_n_medio, ca_n_medio, ba_n_bajo, h_n_bajo), min(ref_n_medio, sod_n_bajo, mag_n_alto, sil_n_medio, p_n_bajo, ca_n_medio, ba_n_bajo, h_n_bajo), min(ref_n_medio, sod_n_bajo, mag_n_alto, al_n_bajo, sil_n_medio, p_n_medio, ca_n_medio, ba_n_bajo, h_n_bajo), min(ref_n_baja, sod_n_medio, mag_n_alto, sil_n_medio, p_n_medio, ca_n_medio, ba_n_bajo, h_n_bajo), min(ref_n_medio, sod_n_medio, mag_n_alto, sil_n_medio, p_n_bajo, ca_n_medio, ba_n_bajo, h_n_bajo), min(ref_n_medio, sod_n_medio, mag_n_alto, sil_n_medio, p_n_medio, ca_n_medio, ba_n_bajo, h_n_bajo), min(ref_n_alta, sod_n_medio, mag_n_alto, sil_n_medio, ca_n_medio, ba_n_bajo, h_n_bajo))
        act[2] = max(act[2], min(ref_n_alta, sod_n_bajo, mag_n_alto, ca_n_bajo, ba_n_bajo), min(sod_n_medio, mag_n_alto, sil_n_bajo, p_n_bajo, ca_n_bajo, ba_n_bajo, h_n_medio), min(sod_n_medio, mag_n_alto, p_n_bajo, ca_n_bajo, ba_n_bajo, h_n_alto), min(sod_n_medio, mag_n_alto, p_n_medio, ca_n_bajo, ba_n_bajo), min(ref_n_medio, sod_n_bajo, mag_n_alto, al_n_medio, sil_n_medio, p_n_medio, ca_n_medio, ba_n_bajo, h_n_bajo), min(ref_n_alta, sod_n_bajo, mag_n_alto, sil_n_medio, ca_n_medio, ba_n_bajo, h_n_bajo), min(ref_n_alta, sod_n_alto, mag_n_alto, ca_n_medio, ba_n_bajo), min(mag_n_alto, ca_n_alto, ba_n_bajo))
        act[3] = max(act[3], min(ref_n_baja, sod_n_medio, mag_n_alto, al_n_bajo, p_n_bajo, ca_n_bajo, ba_n_bajo, h_n_bajo), min(ref_n_baja, sod_n_medio, mag_n_alto, al_n_medio, p_n_bajo, ca_n_bajo, ba_n_bajo, h_n_bajo), min(sod_n_medio, mag_n_alto, sil_n_medio, p_n_bajo, ca_n_bajo, ba_n_bajo, h_n_medio), min(ref_n_baja, sod_n_bajo, mag_n_alto, al_n_medio, sil_n_medio, ca_n_medio, ba_n_bajo, h_n_bajo), min(ref_n_baja, sod_n_medio, mag_n_alto, sil_n_medio, p_n_bajo, ca_n_bajo, ba_n_bajo, h_n_bajo))

        dic_tipos = {1: "Ventanas edificio (flotado)", 2: "Ventanas edificio (no flotado)", 3: "Ventanas de vehículos", 4: "Envases", 5: "Vajillas", 6: "Faros de vehículos"}
        tipo_seleccionado = max(act, key=act.get)
        max_valor = act[tipo_seleccionado]

        if max_valor > 0:
            self.lbl_resultado.text = f"Resultado: Tipo {tipo_seleccionado}\n{dic_tipos[tipo_seleccionado]}\n(Activación: {max_valor:.2f})"
        else:
            self.lbl_resultado.text = "Resultado: Indeterminado\nNo se activó ninguna regla difusa."

if __name__ == '__main__':
    GlassFuzzyApp().run()
