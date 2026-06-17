#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ==============================================================================
# Nazwa pliku: PyPhoto.py
# 
# Copyright (c) 2026 Daniel Kaliski
# Ten kod jest objęty licencją GNU GENERAL PUBLIC LICENSE GPL-3.0.
# Pełny tekst licencji znajduje się w pliku LICENSE lub na stronie:
# https://opensource.org/license/gpl-3.0
# ==============================================================================

import sys
import os

class DummyStream:
    def write(self, *args, **kwargs): pass
    def flush(self, *args, **kwargs): pass

if sys.stdout is None:
    sys.stdout = DummyStream()
if sys.stderr is None:
    sys.stderr = DummyStream()

try:
    if sys.platform == "win32":
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
        myappid = 'com.danielkaliski.pyphoto.1.0'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except Exception:
    pass

import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser, simpledialog
import tkinter.font as tkfont
from PIL import Image, ImageTk, ImageOps, ImageFilter, ImageEnhance, ImageDraw, ImageFont, ImageChops
from rembg import remove
import locale

TEXTS = {
    "pl": {
        "title": "PyPhoto - Image Editor",
        "menu_file": "Plik",
        "menu_edit": "Edycja",
        "menu_image": "Obraz",
        "menu_tools": "Narzędzia",
        "menu_shapes": "Kształty",
        "menu_filters": "Filtry",
        "menu_language": "Język",
        "active_tool": "Narzędzie:",
        "none": "Brak",
        "tools": "Narzędzia",
        "open": "Otwórz obraz...",
        "undo": "Cofnij (Undo)",
        "transform": "Transformacje:",
        "rotate": "Obróć o 90°",
        "flip_h": "Odbij w poziomie",
        "flip_v": "Odbij w pionie",
        "adjust": "Dopasowanie:",
        "brightness": "Jasność",
        "contrast": "Kontrast",
        "saturation": "Nasycenie",
        "sharpness": "Ostrość",
        "scale": "Skala warstwy",
        "interactive": "Narzędzia interaktywne:",
        "move": "Przesuń",
        "brush": "Pędzel",
        "fill": "Wypełnij",
        "text": "Tekst",
        "shape_rect": "Prostokąt",
        "shape_ellipse": "Elipsa",
        "shape_line": "Linia",
        "shape_triangle": "Trójkąt",
        "shape_rounded": "Zaokr. Prostokąt",
        "color": "Wybierz kolor",
        "size": "Grubość:",
        "font_size": "Wielkość:",
        "effects": "Filtry (na warstwie):",
        "effects_placeholder": "Wybierz filtr...",
        "bw": "Czarno-biały",
        "blur": "Rozmycie",
        "sharpen": "Wyostrz",
        "invert": "Negatyw",
        "emboss": "Płaskorzeźba",
        "edges": "Krawędzie",
        "contour": "Kontury",
        "smooth": "Wygładzenie",
        "posterize": "Plakatowanie",
        "solarize": "Solaryzacja",
        "remove_bg": "Usuń tło (AI)",
        "crop": "Kadrowanie:",
        "crop_on": "Aktywuj ramkę",
        "crop_off": "Wyłącz ramkę",
        "crop_apply": "Kadruj",
        "save": "Eksportuj obraz...",
        "layers": "WARSTWY",
        "layer_add": "Nowa",
        "layer_insert": "Wstaw",
        "layer_del": "Usuń",
        "mask_add": "Maska",
        "mask_del": "Maska",
        "mask_edit": "Maska",
        "img_edit": "Obraz",
        "blend": "Tryb mieszania:",
        "rename_title": "Zmiana nazwy",
        "rename_prompt": "Podaj nową nazwę warstwy:",
        "opacity": "Krycie:",
        "bg_layer": "Tło",
        "new_layer": "Warstwa",
        "help": "Wczytaj z menu: Plik > Otwórz",
        "width": "Szer:",
        "height": "Wys:",
        "err_open": "Nie udało się otworzyć:",
        "err_save": "Nie udało się zapisać:",
        "err_val": "Niepoprawne wymiary:",
        "err_dim": "Wymiary muszą być > 0",
        "msg_saved_title": "Zapisano",
        "msg_saved": "Obraz został pomyślnie zapisany.",
        "msg_err_title": "Błąd"
    },
    "en": {
        "title": "PyPhoto - Image Editor",
        "menu_file": "File",
        "menu_edit": "Edit",
        "menu_image": "Image",
        "menu_tools": "Tools",
        "menu_shapes": "Shapes",
        "menu_filters": "Filters",
        "menu_language": "Language",
        "active_tool": "Active tool:",
        "none": "None",
        "tools": "Tools",
        "open": "Open image...",
        "undo": "Undo",
        "transform": "Transformations:",
        "rotate": "Rotate 90°",
        "flip_h": "Flip Horizontally",
        "flip_v": "Flip Vertically",
        "adjust": "Layer Adjustments:",
        "brightness": "Brightness",
        "contrast": "Contrast",
        "saturation": "Saturation",
        "sharpness": "Sharpness",
        "scale": "Layer Scale",
        "interactive": "Interactive Tools:",
        "move": "Move",
        "brush": "Brush",
        "fill": "Fill",
        "text": "Text",
        "shape_rect": "Rectangle",
        "shape_ellipse": "Ellipse",
        "shape_line": "Line",
        "shape_triangle": "Triangle",
        "shape_rounded": "Rounded Rect",
        "color": "Select Color",
        "size": "Thickness:",
        "font_size": "Size:",
        "effects": "Filters:",
        "effects_placeholder": "Select filter...",
        "bw": "Black & White",
        "blur": "Blur",
        "sharpen": "Sharpen",
        "invert": "Invert",
        "emboss": "Emboss",
        "edges": "Find Edges",
        "contour": "Contour",
        "smooth": "Smooth",
        "posterize": "Posterize",
        "solarize": "Solarize",
        "remove_bg": "Remove BG (AI)",
        "crop": "Cropping:",
        "crop_on": "Activate Frame",
        "crop_off": "Deactivate Frame",
        "crop_apply": "Crop",
        "save": "Export Image...",
        "layers": "LAYERS",
        "layer_add": "Add",
        "layer_insert": "Insert",
        "layer_del": "Delete",
        "mask_add": "Mask",
        "mask_del": "Mask",
        "mask_edit": "Mask",
        "img_edit": "Image",
        "blend": "Blend Mode:",
        "rename_title": "Rename",
        "rename_prompt": "Enter new layer name:",
        "opacity": "Opacity:",
        "bg_layer": "Background",
        "new_layer": "Layer",
        "help": "Load from menu: File > Open",
        "width": "W:",
        "height": "H:",
        "err_open": "Failed to open:",
        "err_save": "Failed to save:",
        "err_val": "Invalid dimensions:",
        "err_dim": "Dimensions must be > 0",
        "msg_saved_title": "Saved",
        "msg_saved": "Image saved successfully.",
        "msg_err_title": "Error"
    }
}

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

def blend_layers(base, top, mode):
    if mode == "Normal": return Image.alpha_composite(base, top)
    base_rgb = base.convert("RGB")
    top_rgb = top.convert("RGB")
    
    if mode == "Multiply": blended = ImageChops.multiply(base_rgb, top_rgb)
    elif mode == "Screen": blended = ImageChops.screen(base_rgb, top_rgb)
    elif mode == "Add": blended = ImageChops.add(base_rgb, top_rgb)
    elif mode == "Difference": blended = ImageChops.difference(base_rgb, top_rgb)
    elif mode == "Darken": blended = ImageChops.darker(base_rgb, top_rgb)
    elif mode == "Lighten": blended = ImageChops.lighter(base_rgb, top_rgb)
    else: blended = top_rgb

    top_a = top.split()[3]
    final_rgb = Image.composite(blended, base_rgb, top_a)
    base_a = base.split()[3]
    final_a = ImageChops.screen(base_a, top_a)
    
    res = final_rgb.convert("RGBA")
    res.putalpha(final_a)
    return res

class PyPhoto(ctk.CTk):

    def pobierz_sciezke_zasobu(self, wzgledna_sciezka):
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
            sciezka_podstawowa = os.path.join(base_path, wzgledna_sciezka)
            if not os.path.exists(sciezka_podstawowa) and sys.platform == "darwin":
                sciezka_mac = os.path.join(os.path.dirname(base_path), "Resources", wzgledna_sciezka)
                if os.path.exists(sciezka_mac): return sciezka_mac
            return sciezka_podstawowa
        else:
            base_path = os.path.abspath(os.path.dirname(__file__))
            return os.path.join(base_path, wzgledna_sciezka)

    def zaladuj_ikony(self):
        self.icons = {}
        ikony_katalog = self.pobierz_sciezke_zasobu("ikony")
        
        if not os.path.exists(ikony_katalog):
            self.after(500, lambda: messagebox.showwarning("Brak folderu ikon", f"Nie znaleziono folderu 'ikony' w ścieżce:\n{ikony_katalog}"))
        
        def load_icon(name, size=(18, 18)):
            path = os.path.join(ikony_katalog, name)
            if os.path.exists(path):
                try:
                    img = Image.open(path).convert("RGBA")
                    r, g, b, a = img.split()
                    r = r.point(lambda _: 255)
                    g = g.point(lambda _: 255)
                    b = b.point(lambda _: 255)
                    white_img = Image.merge("RGBA", (r, g, b, a))
                    return ctk.CTkImage(light_image=white_img, dark_image=white_img, size=size)
                except Exception as e:
                    print(f"Nie można załadować {name}: {e}")
            return None

        self.icons["check"] = load_icon("check.png")
        self.icons["color"] = load_icon("palette.png")
        self.icons["crop"] = load_icon("crop.png")
        self.icons["layer_add"] = load_icon("add.png")
        self.icons["layer_insert"] = load_icon("add_photo_alternate.png")
        self.icons["layer_del"] = load_icon("delete.png")
        self.icons["up"] = load_icon("arrow_upward.png")
        self.icons["down"] = load_icon("arrow_downward.png")
        self.icons["vis_on"] = load_icon("visibility.png")
        self.icons["vis_off"] = load_icon("visibility_off.png")
        self.icons["edit"] = load_icon("edit.png")
        self.icons["image"] = load_icon("image.png")
        self.icons["mask"] = load_icon("layers.png")

    def __init__(self):
        super().__init__()
        
        self.lang = self.wykryj_jezyk()
        self.t = TEXTS[self.lang]
        
        self.zaladuj_ikony()

        self.title(self.t["title"])
        self.minsize(1100, 650)
        
        try:
            if sys.platform == "win32":
                icon_path = self.pobierz_sciezke_zasobu("icon.ico")
                if os.path.exists(icon_path):
                    self.iconbitmap(icon_path)
        except Exception:
            pass
        
        if sys.platform == "win32":
            self.after(0, lambda: self.state("zoomed"))
        elif sys.platform == "darwin":
            self.after(0, self.ustaw_pelen_ekran_mac)
        else:
            self.after(0, lambda: self.attributes("-zoomed", True))
            
        self.protocol("WM_DELETE_WINDOW", self.zamykanie_okna)

        self.warstwy = [] 
        self.aktywna_warstwa = -1
        self.doc_size = None 
        self.skompilowany_obraz = None 
        self.tk_obraz = None
        self.historia = []
        self.resize_timer = None
        self.aktywne_narzedzie = None
        self.rect_coords = None
        self.akcja_myszy = None
        self.last_x = 0
        self.last_y = 0
        self.current_color = "#ffffff" 
        self.draw_points = []
        self.temp_draw_id = None
        self.warstwa_podgladowa = None
        self.blokuj_podglad = False
        self.text_resize_started = False
        self.aktywny_ksztalt = self.t["shape_rect"]
        
        self.klucze_filtrow = ["bw", "blur", "sharpen", "invert", "emboss", "edges", "contour", "smooth", "posterize", "solarize"]

        szerokosc_paneli = 260

        self.grid_columnconfigure(0, minsize=szerokosc_paneli, weight=0)
        self.grid_columnconfigure(1, weight=1) 
        self.grid_columnconfigure(2, minsize=szerokosc_paneli, weight=0)
        self.grid_rowconfigure(0, weight=1)
        
        self.panel_lewy = ctk.CTkFrame(self, corner_radius=0, width=szerokosc_paneli)
        self.panel_lewy.grid(row=0, column=0, sticky="nsew")
        self.panel_lewy.grid_propagate(False)
        self.panel_lewy.pack_propagate(False)

        scroll_w = 240
        self.panel_narzedzi = ctk.CTkScrollableFrame(self.panel_lewy, fg_color="transparent", width=scroll_w)
        self.panel_narzedzi.pack(side="top", fill="both", expand=True, pady=(10, 0))
        self.uaktywnij_autoukrywanie_paska(self.panel_narzedzi)
        
        self.lbl_aktywne_narz = ctk.CTkLabel(self.panel_narzedzi, text=f"{self.t['active_tool']} {self.t['none']}", font=ctk.CTkFont(size=13, weight="bold"), text_color="#00ff00", wraplength=220)
        self.lbl_aktywne_narz.pack(pady=(0, 10))

        ramka_opcji = ctk.CTkFrame(self.panel_narzedzi, fg_color="transparent")
        ramka_opcji.pack(pady=5, padx=5, fill="x")
        
        self.btn_color = ctk.CTkButton(ramka_opcji, text=self.t["color"], image=self.icons.get("color"), height=32, corner_radius=6, command=self.wybierz_kolor, fg_color="transparent", border_width=1, border_color="white", text_color=self.current_color, hover_color="#333")
        self.btn_color.pack(fill="x", pady=5)
        
        ramka_grubosc = ctk.CTkFrame(ramka_opcji, fg_color="transparent")
        ramka_grubosc.pack(fill="x", pady=5)
        self.lbl_size = ctk.CTkLabel(ramka_grubosc, text=self.t["size"], width=80, anchor="w", font=ctk.CTkFont(size=13))
        self.lbl_size.pack(side="left", padx=(0, 2))
        self.slider_size = ctk.CTkSlider(ramka_grubosc, from_=1, to=100, button_color="#888", button_hover_color="#bbb")
        self.slider_size.set(5)
        self.slider_size.pack(side="right", expand=True, fill="x")
        
        ramka_czcionka_rodzina = ctk.CTkFrame(ramka_opcji, fg_color="transparent")
        ramka_czcionka_rodzina.pack(fill="x", pady=5)
        czcionki_systemowe = sorted([f for f in tkfont.families() if not f.startswith('@')])
        if not czcionki_systemowe: czcionki_systemowe = ["Arial"]
        self.combo_font = ctk.CTkComboBox(ramka_czcionka_rodzina, values=czcionki_systemowe, state="readonly", command=self.zmien_czcionke_tekstu, fg_color="#242424", border_color="gray50", text_color="white")
        self.combo_font.pack(expand=True, fill="x")
        self.combo_font.set("Arial" if "Arial" in czcionki_systemowe else czcionki_systemowe[0])

        ramka_czcionka = ctk.CTkFrame(ramka_opcji, fg_color="transparent")
        ramka_czcionka.pack(fill="x", pady=5)
        self.lbl_font_size = ctk.CTkLabel(ramka_czcionka, text=self.t["font_size"], width=80, anchor="w", font=ctk.CTkFont(size=13))
        self.lbl_font_size.pack(side="left", padx=(0, 2))
        self.slider_font_size = ctk.CTkSlider(ramka_czcionka, from_=10, to=300, button_color="#888", button_hover_color="#bbb", command=self.zmien_rozmiar_tekstu)
        self.slider_font_size.set(40)
        self.slider_font_size.pack(side="right", expand=True, fill="x")
        self.slider_font_size.bind("<ButtonRelease-1>", lambda e: self.zatwierdz_rozmiar_tekstu())

        ctk.CTkFrame(self.panel_narzedzi, height=2, fg_color="#333").pack(fill="x", pady=15)

        self.lbl_adjust = ctk.CTkLabel(self.panel_narzedzi, text=self.t["adjust"], font=ctk.CTkFont(size=14, weight="bold"))
        self.lbl_adjust.pack(pady=(0, 10))

        for nazwa, attr in [("brightness", "slider_brightness"), ("contrast", "slider_contrast"), ("saturation", "slider_saturation"), ("sharpness", "slider_sharpness"), ("scale", "slider_scale")]:
            ramka_suwaka = ctk.CTkFrame(self.panel_narzedzi, fg_color="transparent")
            ramka_suwaka.pack(fill="x", padx=5, pady=2)
            lbl = ctk.CTkLabel(ramka_suwaka, text=self.t[nazwa], width=80, anchor="w", font=ctk.CTkFont(size=13))
            lbl.pack(side="left", padx=(0, 5))
            if nazwa in ["brightness", "contrast"]:
                suwak = ctk.CTkSlider(ramka_suwaka, from_=0.1, to=2.0, command=self.podglad_suwakow)
            elif nazwa == "scale":
                suwak = ctk.CTkSlider(ramka_suwaka, from_=0.1, to=3.0, command=self.podglad_suwakow)
            else:
                suwak = ctk.CTkSlider(ramka_suwaka, from_=0.0, to=3.0, command=self.podglad_suwakow)
            suwak.set(1.0)
            suwak.pack(side="right", expand=True, fill="x")
            
            setattr(self, attr, suwak)
            setattr(self, f"lbl_{nazwa}", lbl)

        ctk.CTkFrame(self.panel_narzedzi, height=2, fg_color="#333").pack(fill="x", pady=15)

        self.lbl_kadrowanie = ctk.CTkLabel(self.panel_narzedzi, text=self.t["crop"], font=ctk.CTkFont(size=14, weight="bold"))
        self.lbl_kadrowanie.pack(pady=(0, 10))
        
        self.btn_crop = ctk.CTkButton(self.panel_narzedzi, text=self.t["crop_on"], image=self.icons.get("crop"), height=32, corner_radius=6, command=lambda: self.ustaw_narzedzie('crop'), fg_color="transparent", border_width=1, border_color="white", text_color="white", hover_color="#333")
        self.btn_crop.pack(pady=(5,5), padx=10, fill="x")
        
        self.ramka_px = ctk.CTkFrame(self.panel_narzedzi, fg_color="transparent")
        self.ramka_px.pack(pady=5, padx=5, fill="x")
        self.ramka_px.grid_columnconfigure(0, weight=1)
        self.ramka_px.grid_columnconfigure(1, weight=1)
        
        self.entry_x, self.lbl_x = self.stworz_pole_px(self.ramka_px, "X:", 0, 0)
        self.entry_y, self.lbl_y = self.stworz_pole_px(self.ramka_px, "Y:", 0, 1)
        self.entry_w, self.lbl_w = self.stworz_pole_px(self.ramka_px, self.t["width"], 1, 0)
        self.entry_h, self.lbl_h = self.stworz_pole_px(self.ramka_px, self.t["height"], 1, 1)
        
        self.btn_dokladne_crop = ctk.CTkButton(self.panel_narzedzi, text=self.t["crop_apply"], image=self.icons.get("check"), height=32, corner_radius=6, command=self.wykonaj_kadrowanie, fg_color="transparent", border_width=1, border_color="white", text_color="white", hover_color="#333")
        self.btn_dokladne_crop.pack(pady=5, padx=10, fill="x")

        self.panel_obrazu = ctk.CTkFrame(self)
        self.panel_obrazu.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.canvas = tk.Canvas(self.panel_obrazu, bg="gray25", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.text_label = ctk.CTkLabel(self.panel_obrazu, text=self.t["help"], font=ctk.CTkFont(size=14), text_color="gray70")
        self.canvas.create_window(0, 0, window=self.text_label, anchor="center", tags="help_text")

        self.canvas.bind("<Configure>", self.przy_zmianie_rozmiaru)
        self.canvas.bind("<ButtonPress-1>", self.on_canvas_press)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_canvas_release)

        self.panel_prawy = ctk.CTkFrame(self, corner_radius=0, width=szerokosc_paneli)
        self.panel_prawy.grid(row=0, column=2, sticky="nsew")
        self.panel_prawy.grid_propagate(False)
        self.panel_prawy.pack_propagate(False)

        scroll_prawy_w = 260

        self.lbl_layers_title = ctk.CTkLabel(self.panel_prawy, text=self.t["layers"], font=ctk.CTkFont(size=16, weight="bold"))
        self.lbl_layers_title.pack(pady=(15, 5))

        ramka_kontrolek_warstw = ctk.CTkFrame(self.panel_prawy, fg_color="transparent")
        ramka_kontrolek_warstw.pack(fill="x", padx=10, pady=2)
        
        self.btn_add_layer = ctk.CTkButton(ramka_kontrolek_warstw, text=self.t["layer_add"], image=self.icons.get("layer_add"), width=60, height=28, corner_radius=6, command=self.dodaj_pusta_warstwe, fg_color="transparent", border_width=1, border_color="white", text_color="white", hover_color="#333")
        self.btn_add_layer.pack(side="left", padx=2, expand=True)
        self.btn_insert_layer = ctk.CTkButton(ramka_kontrolek_warstw, text=self.t["layer_insert"], image=self.icons.get("layer_insert"), width=60, height=28, corner_radius=6, command=self.wstaw_obraz, fg_color="transparent", border_width=1, border_color="white", text_color="white", hover_color="#333")
        self.btn_insert_layer.pack(side="left", padx=2, expand=True)
        self.btn_del_layer = ctk.CTkButton(ramka_kontrolek_warstw, text=self.t["layer_del"], image=self.icons.get("layer_del"), width=60, height=28, corner_radius=6, command=self.usun_aktywna_warstwe, fg_color="transparent", border_width=1, border_color="white", text_color="white", hover_color="#333")
        self.btn_del_layer.pack(side="left", padx=2, expand=True)

        ramka_maski = ctk.CTkFrame(self.panel_prawy, fg_color="transparent")
        ramka_maski.pack(fill="x", padx=10, pady=2)
        self.btn_add_mask = ctk.CTkButton(ramka_maski, text=self.t["mask_add"], image=self.icons.get("layer_add"), width=60, height=28, corner_radius=6, command=self.dodaj_maske, fg_color="transparent", border_width=1, border_color="white", text_color="white", hover_color="#333")
        self.btn_add_mask.pack(side="left", padx=2, expand=True)
        self.btn_del_mask = ctk.CTkButton(ramka_maski, text=self.t["mask_del"], image=self.icons.get("layer_del"), width=60, height=28, corner_radius=6, command=self.usun_maske, fg_color="transparent", border_width=1, border_color="white", text_color="white", hover_color="#333")
        self.btn_del_mask.pack(side="left", padx=2, expand=True)

        ramka_strzalek = ctk.CTkFrame(self.panel_prawy, fg_color="transparent")
        ramka_strzalek.pack(pady=5)
        self.btn_up_layer = ctk.CTkButton(ramka_strzalek, text="", image=self.icons.get("up"), width=60, height=24, corner_radius=6, command=lambda: self.przesun_warstwe(-1), fg_color="transparent", border_width=1, border_color="white", text_color="white", hover_color="#333")
        self.btn_up_layer.pack(side="left", padx=5)
        self.btn_down_layer = ctk.CTkButton(ramka_strzalek, text="", image=self.icons.get("down"), width=60, height=24, corner_radius=6, command=lambda: self.przesun_warstwe(1), fg_color="transparent", border_width=1, border_color="white", text_color="white", hover_color="#333")
        self.btn_down_layer.pack(side="left", padx=5)

        self.lbl_blend = ctk.CTkLabel(self.panel_prawy, text=self.t["blend"])
        self.lbl_blend.pack(pady=(5, 0))
        self.combo_blend = ctk.CTkComboBox(self.panel_prawy, values=["Normal", "Multiply", "Screen", "Add", "Difference", "Darken", "Lighten"], state="readonly", corner_radius=6, fg_color="#242424", border_color="white", text_color="white", command=self.zmien_tryb_mieszania)
        self.combo_blend.pack(pady=(0, 5), padx=20, fill="x")

        self.lbl_opacity = ctk.CTkLabel(self.panel_prawy, text=self.t["opacity"])
        self.lbl_opacity.pack(pady=(5, 0))
        self.slider_opacity = ctk.CTkSlider(self.panel_prawy, from_=0.0, to=1.0, command=self.zmien_krycie_warstwy, button_color="#888", button_hover_color="#bbb")
        self.slider_opacity.set(1.0)
        self.slider_opacity.pack(pady=(0, 10), padx=20)

        self.panel_listy_warstw = ctk.CTkScrollableFrame(self.panel_prawy, fg_color="transparent", corner_radius=6, width=scroll_prawy_w)
        self.panel_listy_warstw.pack(fill="both", expand=True, padx=10, pady=5)
        self.uaktywnij_autoukrywanie_paska(self.panel_listy_warstw)

        self.bind("<Control-z>", lambda e: self.cofnij())
        self.bind("<Command-z>", lambda e: self.cofnij()) 
        self.bind("<Control-s>", lambda e: self.zapisz_obraz())
        self.bind("<Command-s>", lambda e: self.zapisz_obraz()) 
        self.bind("<Control-o>", lambda e: self.otworz_obraz())
        self.bind("<Command-o>", lambda e: self.otworz_obraz()) 
        self.bind("<Key>", self.obsloz_skroty_narzedzi)

        self.utworz_menu()

    def uaktywnij_autoukrywanie_paska(self, ramka_skrolowana):
        def sprawdz_pasek(event=None):
            try:
                canvas_h = ramka_skrolowana._parent_canvas.winfo_height()
                content_h = ramka_skrolowana._parent_frame.winfo_reqheight()
                if content_h <= canvas_h:
                    ramka_skrolowana._scrollbar.grid_forget()
                else:
                    ramka_skrolowana._scrollbar.grid(row=0, column=1, sticky="ns")
            except Exception:
                pass
                
        ramka_skrolowana._parent_canvas.bind("<Configure>", sprawdz_pasek, add="+")
        ramka_skrolowana._parent_frame.bind("<Configure>", sprawdz_pasek, add="+")
        self.after(100, sprawdz_pasek)

    def utworz_menu(self):
        if sys.platform == "win32":
            domyslna_czcionka_menu = tkfont.nametofont("TkMenuFont")
            domyslna_czcionka_menu.configure(size=11, family="Segoe UI")
            czcionka_menu = domyslna_czcionka_menu
        else:
            czcionka_menu = ("Arial", 14)
            
        self.option_add('*tearOff', False)
        
        menubar = tk.Menu(self, font=czcionka_menu)
        
        menu_plik = tk.Menu(menubar, font=czcionka_menu)
        menu_plik.add_command(label=self.t["open"], command=self.otworz_obraz)
        menu_plik.add_command(label=self.t["save"], command=self.zapisz_obraz)
        menubar.add_cascade(label=self.t.get("menu_file", "Plik"), menu=menu_plik)
        
        menu_edycja = tk.Menu(menubar, font=czcionka_menu)
        self.menu_edycja = menu_edycja
        menu_edycja.add_command(label=self.t["undo"], command=self.cofnij, state="disabled" if not self.historia else "normal")
        menubar.add_cascade(label=self.t.get("menu_edit", "Edycja"), menu=menu_edycja)
        
        menu_obraz = tk.Menu(menubar, font=czcionka_menu)
        menu_obraz.add_command(label=self.t["rotate"], command=self.obroc_obraz)
        menu_obraz.add_command(label=self.t["flip_h"], command=self.odbij_w_poziomie)
        menu_obraz.add_command(label=self.t["flip_v"], command=self.odbij_w_pionie)
        menu_obraz.add_separator()
        menu_obraz.add_command(label=self.t["remove_bg"], command=self.usun_tlo)
        menubar.add_cascade(label=self.t.get("menu_image", "Obraz"), menu=menu_obraz)
        
        menu_narzedzia = tk.Menu(menubar, font=czcionka_menu)
        menu_narzedzia.add_command(label=self.t["move"], command=lambda: self.ustaw_narzedzie('move'))
        menu_narzedzia.add_command(label=self.t["brush"], command=lambda: self.ustaw_narzedzie('brush'))
        menu_narzedzia.add_command(label=self.t["fill"], command=lambda: self.ustaw_narzedzie('fill'))
        menu_narzedzia.add_command(label=self.t["text"], command=lambda: self.ustaw_narzedzie('text'))
        
        menu_ksztalty = tk.Menu(menu_narzedzia, font=czcionka_menu)
        menu_ksztalty.add_command(label=self.t["shape_rect"], command=lambda: self.wybierz_ksztalt(self.t["shape_rect"]))
        menu_ksztalty.add_command(label=self.t["shape_ellipse"], command=lambda: self.wybierz_ksztalt(self.t["shape_ellipse"]))
        menu_ksztalty.add_command(label=self.t["shape_line"], command=lambda: self.wybierz_ksztalt(self.t["shape_line"]))
        menu_ksztalty.add_command(label=self.t["shape_triangle"], command=lambda: self.wybierz_ksztalt(self.t["shape_triangle"]))
        menu_ksztalty.add_command(label=self.t["shape_rounded"], command=lambda: self.wybierz_ksztalt(self.t["shape_rounded"]))
        menu_narzedzia.add_cascade(label=self.t.get("menu_shapes", "Kształty"), menu=menu_ksztalty)
        
        menubar.add_cascade(label=self.t.get("menu_tools", "Narzędzia"), menu=menu_narzedzia)
        
        menu_filtry = tk.Menu(menubar, font=czcionka_menu)
        for key in self.klucze_filtrow:
            menu_filtry.add_command(label=self.t[key], command=lambda k=key: self.zastosuj_wybrany_filtr(self.t[k]))
        menubar.add_cascade(label=self.t.get("menu_filters", "Filtry"), menu=menu_filtry)
        
        menu_jezyk = tk.Menu(menubar, font=czcionka_menu)
        menu_jezyk.add_command(label="Polski", command=lambda: self.ustaw_jezyk("pl"))
        menu_jezyk.add_command(label="English", command=lambda: self.ustaw_jezyk("en"))
        menubar.add_cascade(label=self.t.get("menu_language", "Język"), menu=menu_jezyk)
        
        self.config(menu=menubar)

    def wybierz_ksztalt(self, ksztalt):
        self.aktywny_ksztalt = ksztalt
        self.ustaw_narzedzie('shape')

    def wykryj_jezyk(self):
        try:
            if sys.platform == 'win32': 
                import ctypes
                if ctypes.windll.kernel32.GetUserDefaultUILanguage() == 1045: return "pl"
            else:
                j, _ = locale.getlocale()
                if j and 'pl' in j.lower(): return "pl"
        except: 
            pass
        return "pl"

    def ustaw_pelen_ekran_mac(self):
        w = self.winfo_screenwidth()
        h = self.winfo_screenheight()
        self.geometry(f"{w}x{h}+0+0")

    def get_draw_color(self):
        kolor_hex = self.current_color
        if self.aktywna_warstwa != -1 and self.warstwy[self.aktywna_warstwa].get('edycja_maski'):
            r, g, b = tuple(int(kolor_hex.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
            gray = int(r * 0.299 + g * 0.587 + b * 0.114)
            return f"#{gray:02x}{gray:02x}{gray:02x}"
        return kolor_hex

    def stworz_pole_px(self, rodzic, tekst, rzad, kolumna):
        ramka = ctk.CTkFrame(rodzic, fg_color="transparent")
        ramka.grid(row=rzad, column=kolumna, padx=1, pady=2, sticky="ew")
        lbl = ctk.CTkLabel(ramka, text=tekst, font=("Arial", 11))
        lbl.pack(side="left")
        entry = ctk.CTkEntry(ramka, height=28, width=45, corner_radius=4, font=("Arial", 11))
        entry.pack(side="left", padx=1, expand=True, fill="x")
        return entry, lbl

    def zamykanie_okna(self):
        self.destroy()

    def _update_text(self, widget_name, text_key):
        try:
            widget = getattr(self, widget_name)
            widget.configure(text=self.t[text_key])
        except Exception:
            pass 

    def ustaw_jezyk(self, kod):
        if self.lang == kod:
            return
            
        stare_t = self.t
        self.lang = kod
        self.t = TEXTS[self.lang]
        
        for w in self.warstwy:
            if w['nazwa'] == stare_t['brush']:
                w['nazwa'] = self.t['brush']
            elif w['nazwa'].startswith(stare_t['new_layer'] + " "):
                w['nazwa'] = w['nazwa'].replace(stare_t['new_layer'], self.t['new_layer'], 1)
        
        self.title(self.t["title"])
        
        self._update_text("lbl_aktywne_narz", "active_tool")
        self._update_text("btn_color", "color")
        self._update_text("lbl_size", "size")
        self._update_text("lbl_font_size", "font_size")
        self._update_text("lbl_adjust", "adjust")
        self._update_text("lbl_brightness", "brightness")
        self._update_text("lbl_contrast", "contrast")
        self._update_text("lbl_saturation", "saturation")
        self._update_text("lbl_sharpness", "sharpness")
        self._update_text("lbl_scale", "scale")
        self._update_text("lbl_kadrowanie", "crop")
        self._update_text("lbl_w", "width")
        self._update_text("lbl_h", "height")
        self._update_text("btn_dokladne_crop", "crop_apply")
        self._update_text("lbl_layers_title", "layers")
        self._update_text("btn_add_layer", "layer_add")
        self._update_text("btn_insert_layer", "layer_insert")
        self._update_text("btn_del_layer", "layer_del")
        self._update_text("btn_add_mask", "mask_add")
        self._update_text("btn_del_mask", "mask_del")
        self._update_text("lbl_blend", "blend")
        self._update_text("lbl_opacity", "opacity")
        self._update_text("text_label", "help")

        if self.aktywny_ksztalt in [stare_t[k] for k in ["shape_rect", "shape_ellipse", "shape_line", "shape_triangle", "shape_rounded"]]:
            shape_keys = ["shape_rect", "shape_ellipse", "shape_line", "shape_triangle", "shape_rounded"]
            for key in shape_keys:
                if self.aktywny_ksztalt == stare_t[key]:
                    self.aktywny_ksztalt = self.t[key]
                    break

        self.odswiez_panel_warstw()
        self.utworz_menu()
        
        temp_tool = self.aktywne_narzedzie
        self.aktywne_narzedzie = None
        self.ustaw_narzedzie(temp_tool) 

        if not self.warstwy: 
            self.canvas.delete("all")
            self.canvas.create_window(self.canvas.winfo_width()/2, self.canvas.winfo_height()/2, window=self.text_label, anchor="center", tags="help_text")

    def obsloz_skroty_narzedzi(self, event):
        if not self.warstwy: return
        if isinstance(self.focus_get(), (tk.Entry, ctk.CTkEntry)): return
        if not event.char: return
        char = event.char.lower()
        if char == 'v': self.ustaw_narzedzie('move')
        elif char == 'b': self.ustaw_narzedzie('brush')
        elif char == 't': self.ustaw_narzedzie('text')
        elif char == 'c': self.ustaw_narzedzie('crop')
        elif char == 'f': self.ustaw_narzedzie('fill')

    def wybierz_kolor(self):
        kolor = colorchooser.askcolor(color=self.current_color)[1]
        if kolor: 
            self.current_color = kolor
            self.btn_color.configure(text_color=kolor)
            if self.aktywna_warstwa != -1 and self.warstwy[self.aktywna_warstwa].get('is_text'):
                self.zapisz_stan_do_historii()
                fill_color = tuple(int(self.current_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)) + (255,)
                self.warstwy[self.aktywna_warstwa]['text_color'] = fill_color
                self.renderuj_warstwe_tekstu(self.aktywna_warstwa)
                self.komponuj_i_wyswietl()

    def aktualizuj_wymiary_w_polach(self, x=0, y=0, w=0, h=0):
        for entry, val in [(self.entry_x, str(x)), (self.entry_y, str(y)), (self.entry_w, str(w)), (self.entry_h, str(h))]:
            entry.delete(0, tk.END)
            entry.insert(0, val)

    def otworz_obraz(self):
        sciezka = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp *.webp")])
        if sciezka:
            try:
                img = Image.open(sciezka)
                if img.mode != "RGBA":
                    img = img.convert("RGBA")
                
                self.doc_size = img.size
                self.warstwy = []
                self.historia = []
                if hasattr(self, 'menu_edycja'):
                    self.menu_edycja.entryconfig(0, state="disabled")
                
                nazwa = os.path.basename(sciezka)[:15]
                self.dodaj_warstwe(img, nazwa, 0, 0)
                self.ustaw_aktywna_warstwe(0)
                
            except Exception as e:
                messagebox.showerror(self.t["msg_err_title"], f"{self.t['err_open']} {e}")

    def wstaw_obraz(self):
        if not self.doc_size:
            self.otworz_obraz()
            return
            
        sciezka = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp *.webp")])
        if sciezka:
            try:
                img = Image.open(sciezka)
                if img.mode != "RGBA":
                    img = img.convert("RGBA")
                
                self.zatwierdz_podglad()
                self.zapisz_stan_do_historii()
                
                x = (self.doc_size[0] - img.width) // 2
                y = (self.doc_size[1] - img.height) // 2
                nazwa = os.path.basename(sciezka)[:12]
                
                idx = self.aktywna_warstwa + 1 if self.aktywna_warstwa != -1 else 0
                self.warstwy.insert(idx, {'nazwa': nazwa, 'obraz': img, 'widoczna': True, 'krycie': 1.0, 'tryb': 'Normal', 'maska': None, 'edycja_maski': False, 'offset_x': x, 'offset_y': y})
                self.ustaw_aktywna_warstwe(idx)
            except Exception as e:
                messagebox.showerror(self.t["msg_err_title"], f"{self.t['err_open']} {e}")

    def dodaj_warstwe(self, obraz, nazwa, off_x=0, off_y=0):
        self.warstwy.append({'nazwa': nazwa, 'obraz': obraz, 'widoczna': True, 'krycie': 1.0, 'tryb': 'Normal', 'maska': None, 'edycja_maski': False, 'offset_x': off_x, 'offset_y': off_y})
        self.odswiez_panel_warstw()
        self.komponuj_i_wyswietl()

    def dodaj_pusta_warstwe(self):
        if not self.doc_size: return
        self.zatwierdz_podglad()
        self.zapisz_stan_do_historii()
        pusta = Image.new("RGBA", self.doc_size, (0, 0, 0, 0))
        nazwa = f"{self.t['new_layer']} {len(self.warstwy)}"
        
        idx = self.aktywna_warstwa + 1 if self.aktywna_warstwa != -1 else 0
        self.warstwy.insert(idx, {'nazwa': nazwa, 'obraz': pusta, 'widoczna': True, 'krycie': 1.0, 'tryb': 'Normal', 'maska': None, 'edycja_maski': False, 'offset_x': 0, 'offset_y': 0})
        self.ustaw_aktywna_warstwe(idx)

    def usun_aktywna_warstwe(self):
        if len(self.warstwy) <= 1: return 
        self.zatwierdz_podglad()
        self.zapisz_stan_do_historii()
        del self.warstwy[self.aktywna_warstwa]
        self.ustaw_aktywna_warstwe(max(0, self.aktywna_warstwa - 1))

    def dodaj_maske(self):
        if self.aktywna_warstwa == -1: return
        w = self.warstwy[self.aktywna_warstwa]
        if w.get('maska') is None:
            self.zatwierdz_podglad()
            self.zapisz_stan_do_historii()
            w['maska'] = Image.new("L", w['obraz'].size, 255)
            w['edycja_maski'] = True
            self.odswiez_panel_warstw()
            self.komponuj_i_wyswietl()

    def usun_maske(self):
        if self.aktywna_warstwa == -1: return
        w = self.warstwy[self.aktywna_warstwa]
        if w.get('maska') is not None:
            self.zatwierdz_podglad()
            self.zapisz_stan_do_historii()
            w['maska'] = None
            w['edycja_maski'] = False
            self.odswiez_panel_warstw()
            self.komponuj_i_wyswietl()

    def przelacz_edycje_maski(self, idx):
        self.zatwierdz_podglad()
        w = self.warstwy[idx]
        if w.get('maska') is not None:
            w['edycja_maski'] = not w.get('edycja_maski', False)
            self.odswiez_panel_warstw()

    def przesun_warstwe(self, kierunek):
        idx = self.aktywna_warstwa
        nowy_idx = idx - kierunek
        if 0 <= nowy_idx < len(self.warstwy):
            self.zatwierdz_podglad()
            self.zapisz_stan_do_historii()
            self.warstwy[idx], self.warstwy[nowy_idx] = self.warstwy[nowy_idx], self.warstwy[idx]
            self.ustaw_aktywna_warstwe(nowy_idx)

    def ustaw_aktywna_warstwe(self, index):
        self.zatwierdz_podglad()
        self.aktywna_warstwa = index
        if 0 <= index < len(self.warstwy):
            self.slider_opacity.set(self.warstwy[index]['krycie'])
            self.combo_blend.set(self.warstwy[index].get('tryb', 'Normal'))
            
            if self.warstwy[index].get('is_text'):
                self.slider_font_size.set(self.warstwy[index]['text_size'])
                if 'text_font' in self.warstwy[index]:
                    self.combo_font.set(self.warstwy[index]['text_font'])
                
        self.odswiez_panel_warstw()
        self.resetuj_suwaki()
        self.komponuj_i_wyswietl()

    def zmien_nazwe_warstwy(self, idx):
        self.zatwierdz_podglad()
        nowa_nazwa = simpledialog.askstring(self.t["rename_title"], self.t["rename_prompt"], initialvalue=self.warstwy[idx]['nazwa'])
        if nowa_nazwa:
            self.warstwy[idx]['nazwa'] = nowa_nazwa
            self.odswiez_panel_warstw()

    def zmien_krycie_warstwy(self, wartosc):
        if self.aktywna_warstwa != -1:
            self.warstwy[self.aktywna_warstwa]['krycie'] = wartosc
            self.komponuj_i_wyswietl()

    def zmien_tryb_mieszania(self, wartosc):
        if self.aktywna_warstwa != -1:
            self.warstwy[self.aktywna_warstwa]['tryb'] = wartosc
            self.komponuj_i_wyswietl()

    def przelacz_widocznosc(self, index):
        self.zatwierdz_podglad()
        self.warstwy[index]['widoczna'] = not self.warstwy[index]['widoczna']
        self.odswiez_panel_warstw()
        self.komponuj_i_wyswietl()

    def odswiez_panel_warstw(self):
        for widget in self.panel_listy_warstw.winfo_children():
            widget.destroy()

        for i in reversed(range(len(self.warstwy))):
            w = self.warstwy[i]
            
            is_active = (i == self.aktywna_warstwa)
            
            kolor_tla = "#333333" if is_active else "transparent"
            kolor_hover = "#444444" if is_active else "#333"
            grubosc_ramki = 2 if is_active else 1
            
            ramka = ctk.CTkFrame(self.panel_listy_warstw, fg_color=kolor_tla, corner_radius=6)
            ramka.pack(fill="x", pady=3, padx=2)
            
            ikona = self.icons.get("vis_on") if w['widoczna'] else self.icons.get("vis_off")
            btn_vis = ctk.CTkButton(ramka, text="", image=ikona, width=30, fg_color="transparent", border_width=1, border_color="white", text_color="white", hover_color=kolor_hover, command=lambda idx=i: self.przelacz_widocznosc(idx))
            btn_vis.pack(side="left", padx=5, pady=5)
            
            btn_name = ctk.CTkButton(ramka, text=w['nazwa'], fg_color="transparent", border_width=grubosc_ramki, border_color="white", text_color="white", hover_color=kolor_hover, anchor="w", command=lambda idx=i: self.ustaw_aktywna_warstwe(idx))
            btn_name.pack(side="left", fill="x", expand=True, padx=5, pady=5)
            
            if w.get('maska') is not None:
                tekst_maski = self.t["mask_edit"] if w.get('edycja_maski') else self.t["img_edit"]
                ikona_maski = self.icons.get("mask") if w.get('edycja_maski') else self.icons.get("image")
                btn_mask_toggle = ctk.CTkButton(ramka, text=tekst_maski, image=ikona_maski, width=50, fg_color="transparent", border_width=1, border_color="white", text_color="white", hover_color=kolor_hover, command=lambda idx=i: self.przelacz_edycje_maski(idx))
                btn_mask_toggle.pack(side="left", padx=2, pady=5)
            
            btn_rename = ctk.CTkButton(ramka, text="", image=self.icons.get("edit"), width=25, fg_color="transparent", border_width=1, border_color="white", hover_color=kolor_hover, command=lambda idx=i: self.zmien_nazwe_warstwy(idx))
            btn_rename.pack(side="right", padx=2, pady=5)

    def komponuj_i_wyswietl(self):
        if not self.warstwy or not self.doc_size:
            self.canvas.delete("all")
            return

        kompozyt = Image.new("RGBA", self.doc_size, (0, 0, 0, 0))

        for i, w in enumerate(self.warstwy):
            if w['widoczna']:
                img = w['obraz']
                if i == self.aktywna_warstwa and self.warstwa_podgladowa is not None:
                    img = self.warstwa_podgladowa
                
                img = img.copy()
                
                temp = Image.new("RGBA", self.doc_size, (0, 0, 0, 0))
                temp.paste(img, (w.get('offset_x', 0), w.get('offset_y', 0)))
                
                if w['krycie'] < 1.0:
                    alpha = temp.split()[3]
                    alpha = alpha.point(lambda p: int(p * w['krycie']))
                    temp.putalpha(alpha)
                    
                if w.get('maska') is not None:
                    m_temp = Image.new("L", self.doc_size, 0)
                    m_temp.paste(w['maska'], (w.get('offset_x', 0), w.get('offset_y', 0)))
                    alpha = temp.split()[3]
                    nowa_maska = ImageChops.multiply(alpha, m_temp)
                    temp.putalpha(nowa_maska)
                    
                tryb = w.get('tryb', 'Normal')
                kompozyt = blend_layers(kompozyt, temp, tryb)

        self.skompilowany_obraz = kompozyt
        self.wyrenderuj_na_plotnie(self.skompilowany_obraz)

    def wyrenderuj_na_plotnie(self, obraz):
        self.update_idletasks()
        okno_szer = self.canvas.winfo_width()
        okno_wys = self.canvas.winfo_height()
        
        if okno_szer < 10 or okno_wys < 10: okno_szer, okno_wys = 800, 600

        display_img = obraz.copy()
        img_szer, img_wys = display_img.size
        ratio = min(okno_szer / img_szer, okno_wys / img_wys)
        self.display_width = int(img_szer * ratio)
        self.display_height = int(img_wys * ratio)
        
        display_img = display_img.resize((self.display_width, self.display_height), Image.Resampling.LANCZOS)
        self.tk_obraz = ImageTk.PhotoImage(display_img)
        
        self.canvas.delete("all")
        self.canvas_img_x_offset = (okno_szer - self.display_width) // 2
        self.canvas_img_y_offset = (okno_wys - self.display_height) // 2
        self.canvas.create_image(self.canvas_img_x_offset, self.canvas_img_y_offset, image=self.tk_obraz, anchor="nw")
        
        self.aktualizuj_wymiary_w_polach(w=self.doc_size[0], h=self.doc_size[1])

    def zatwierdz_podglad(self):
        if self.warstwa_podgladowa is not None and self.aktywna_warstwa != -1:
            self.zapisz_stan_do_historii()
            w = self.warstwy[self.aktywna_warstwa]
            w['obraz'] = self.warstwa_podgladowa
            self.warstwa_podgladowa = None
            
            if w.get('is_text') and not w.get('edycja_maski'):
                w.pop('is_text', None)
            
            self.blokuj_podglad = True
            if hasattr(self, 'slider_brightness'): self.slider_brightness.set(1.0)
            if hasattr(self, 'slider_contrast'): self.slider_contrast.set(1.0)
            if hasattr(self, 'slider_saturation'): self.slider_saturation.set(1.0)
            if hasattr(self, 'slider_sharpness'): self.slider_sharpness.set(1.0)
            if hasattr(self, 'slider_scale'): self.slider_scale.set(1.0)
            self.blokuj_podglad = False
            self.komponuj_i_wyswietl()

    def zapisz_stan_do_historii(self):
        if len(self.historia) >= 8: self.historia.pop(0)
        kopia_warstw = []
        for w in self.warstwy:
            kopia = {
                'nazwa': w['nazwa'],
                'widoczna': w['widoczna'],
                'krycie': w['krycie'],
                'tryb': w.get('tryb', 'Normal'),
                'edycja_maski': w.get('edycja_maski', False),
                'obraz': w['obraz'].copy() if w.get('obraz') else None,
                'maska': w['maska'].copy() if w.get('maska') else None,
                'offset_x': w.get('offset_x', 0),
                'offset_y': w.get('offset_y', 0)
            }
            if w.get('is_text'):
                kopia['is_text'] = True
                kopia['text_content'] = w.get('text_content')
                kopia['text_x'] = w.get('text_x')
                kopia['text_y'] = w.get('text_y')
                kopia['text_color'] = w.get('text_color')
                kopia['text_size'] = w.get('text_size')
                kopia['text_font'] = w.get('text_font')
            kopia_warstw.append(kopia)
            
        self.historia.append((self.doc_size, self.aktywna_warstwa, kopia_warstw))
        if hasattr(self, 'menu_edycja'):
            self.menu_edycja.entryconfig(0, state="normal")

    def cofnij(self):
        self.warstwa_podgladowa = None
        self.blokuj_podglad = True
        if hasattr(self, 'slider_scale'): self.slider_scale.set(1.0)
        if hasattr(self, 'slider_brightness'): self.slider_brightness.set(1.0)
        self.blokuj_podglad = False
        
        if self.historia:
            stan = self.historia.pop()
            self.doc_size, self.aktywna_warstwa, warstwy = stan
            self.warstwy = warstwy
            if not self.historia and hasattr(self, 'menu_edycja'): 
                self.menu_edycja.entryconfig(0, state="disabled")
            self.resetuj_suwaki()
            
            temp_tool = self.aktywne_narzedzie
            self.aktywne_narzedzie = None
            self.ustaw_narzedzie(temp_tool) 
            
            self.odswiez_panel_warstw()
            self.komponuj_i_wyswietl()

    def podglad_suwakow(self, value=None):
        if getattr(self, 'blokuj_podglad', False): return
        if self.aktywna_warstwa == -1: return
        if self.aktywne_narzedzie: self.ustaw_narzedzie(None)
        
        if self.warstwy[self.aktywna_warstwa].get('edycja_maski'): return 

        img = self.warstwy[self.aktywna_warstwa]['obraz'].copy()
        b, c = self.slider_brightness.get(), self.slider_contrast.get()
        s, sh = self.slider_saturation.get(), self.slider_sharpness.get()
        sc = getattr(self, 'slider_scale', None)
        sc_val = sc.get() if sc else 1.0

        rgb = img.convert("RGB")
        if b != 1.0: rgb = ImageEnhance.Brightness(rgb).enhance(b)
        if c != 1.0: rgb = ImageEnhance.Contrast(rgb).enhance(c)
        if s != 1.0: rgb = ImageEnhance.Color(rgb).enhance(s)
        if sh != 1.0: rgb = ImageEnhance.Sharpness(rgb).enhance(sh)
        rgb.putalpha(img.getchannel('A'))
        
        if sc_val != 1.0:
            new_w = max(1, int(img.width * sc_val))
            new_h = max(1, int(img.height * sc_val))
            scaled = rgb.resize((new_w, new_h), Image.Resampling.LANCZOS)
            rgb = scaled
            
        self.warstwa_podgladowa = rgb
        self.komponuj_i_wyswietl()

    def resetuj_suwaki(self):
        self.blokuj_podglad = True
        self.warstwa_podgladowa = None
        if hasattr(self, 'slider_brightness'): self.slider_brightness.set(1.0)
        if hasattr(self, 'slider_contrast'): self.slider_contrast.set(1.0)
        if hasattr(self, 'slider_saturation'): self.slider_saturation.set(1.0)
        if hasattr(self, 'slider_sharpness'): self.slider_sharpness.set(1.0)
        if hasattr(self, 'slider_scale'): self.slider_scale.set(1.0)
        self.blokuj_podglad = False

    def nałoż_filtr(self, filter_type):
        if self.aktywna_warstwa == -1: return
        w = self.warstwy[self.aktywna_warstwa]
        
        if w.get('is_text') and not w.get('edycja_maski'):
            w.pop('is_text', None)
            
        self.zatwierdz_podglad()
        self.zapisz_stan_do_historii()
        
        img = w['obraz']
        if img.mode != "RGBA": img = img.convert("RGBA")
            
        r, g, b, a = img.split()
        rgb = Image.merge("RGB", (r, g, b))
        
        if filter_type == "grayscale": rgb = ImageOps.grayscale(rgb).convert("RGB")
        elif filter_type == "invert": rgb = ImageOps.invert(rgb)
        elif filter_type == "posterize": rgb = ImageOps.posterize(rgb, 3)
        elif filter_type == "solarize": rgb = ImageOps.solarize(rgb, 128)
        else: rgb = rgb.filter(filter_type)
        
        r2, g2, b2 = rgb.split()
        w['obraz'] = Image.merge("RGBA", (r2, g2, b2, a))
        self.komponuj_i_wyswietl()

    def filtr_szary(self): self.nałoż_filtr("grayscale")
    def filtr_rozmycie(self): self.nałoż_filtr(ImageFilter.GaussianBlur(radius=3))
    def filtr_wyostrzenie(self): self.nałoż_filtr(ImageFilter.SHARPEN)
    def filtr_negatyw(self): self.nałoż_filtr("invert")
    def filtr_plaskorzezba(self): self.nałoż_filtr(ImageFilter.EMBOSS)
    def filtr_krawedzie(self): self.nałoż_filtr(ImageFilter.FIND_EDGES)
    def filtr_kontury(self): self.nałoż_filtr(ImageFilter.CONTOUR)
    def filtr_wygladzenie(self): self.nałoż_filtr(ImageFilter.SMOOTH_MORE)
    def filtr_plakatowanie(self): self.nałoż_filtr("posterize")
    def filtr_solaryzacja(self): self.nałoż_filtr("solarize")
    
    def zastosuj_wybrany_filtr(self, w):
        if self.aktywna_warstwa == -1:
            return
            
        k = next((key for key in self.klucze_filtrow if self.t[key] == w), None)
        if k == "bw": self.filtr_szary()
        elif k == "blur": self.filtr_rozmycie()
        elif k == "sharpen": self.filtr_wyostrzenie()
        elif k == "invert": self.filtr_negatyw()
        elif k == "emboss": self.filtr_plaskorzezba()
        elif k == "edges": self.filtr_krawedzie()
        elif k == "contour": self.filtr_kontury()
        elif k == "smooth": self.filtr_wygladzenie()
        elif k == "posterize": self.filtr_plakatowanie()
        elif k == "solarize": self.filtr_solaryzacja()
        
        self.canvas.focus_set()

    def obroc_obraz(self):
        if not self.warstwy: return
        self.zatwierdz_podglad()
        self.zapisz_stan_do_historii()
        
        for w in self.warstwy:
            if w.get('is_text'): w.pop('is_text', None)
            
            old_img_w = w['obraz'].width
            w['obraz'] = w['obraz'].rotate(-90, expand=True)
            if w.get('maska') is not None:
                w['maska'] = w['maska'].rotate(-90, expand=True)
            
            old_x = w.get('offset_x', 0)
            old_y = w.get('offset_y', 0)
            w['offset_x'] = old_y
            w['offset_y'] = self.doc_size[0] - old_x - old_img_w
                
        self.doc_size = (self.doc_size[1], self.doc_size[0])
        self.komponuj_i_wyswietl()

    def odbij_w_poziomie(self):
        if self.aktywna_warstwa == -1: return
        self.zatwierdz_podglad()
        self.zapisz_stan_do_historii()
        w = self.warstwy[self.aktywna_warstwa]
        if w.get('is_text'): w.pop('is_text', None)
        
        w['obraz'] = ImageOps.mirror(w['obraz'])
        if w.get('maska') is not None:
            w['maska'] = ImageOps.mirror(w['maska'])
        self.komponuj_i_wyswietl()

    def odbij_w_pionie(self):
        if self.aktywna_warstwa == -1: return
        self.zatwierdz_podglad()
        self.zapisz_stan_do_historii()
        w = self.warstwy[self.aktywna_warstwa]
        if w.get('is_text'): w.pop('is_text', None)
        
        w['obraz'] = ImageOps.flip(w['obraz'])
        if w.get('maska') is not None:
            w['maska'] = ImageOps.flip(w['maska'])
        self.komponuj_i_wyswietl()

    def usun_tlo(self):
        if self.aktywna_warstwa == -1: return
        w = self.warstwy[self.aktywna_warstwa]
        if w.get('edycja_maski'): return
        
        try:
            self.zatwierdz_podglad()
            self.zapisz_stan_do_historii()
            self.config(cursor="watch")
            self.update()
            
            if w.get('is_text'): w.pop('is_text', None)
            
            wynik = remove(w['obraz'])
            if wynik.mode != "RGBA": wynik = wynik.convert("RGBA")
            w['obraz'] = wynik
            
            self.komponuj_i_wyswietl()
        except Exception as e:
            messagebox.showerror(self.t["msg_err_title"], f"Błąd AI: {e}")
        finally:
            self.config(cursor="")

    def wykonaj_kadrowanie(self):
        if not self.warstwy: return
        try:
            self.zatwierdz_podglad()
            if self.rect_coords and self.aktywne_narzedzie == 'crop':
                x1, y1, x2, y2 = self.rect_coords
                rx1, ry1 = self.canvas_to_image_coords(min(x1, x2), min(y1, y2))
                rx2, ry2 = self.canvas_to_image_coords(max(x1, x2), max(y1, y2))
                
                cx1, cy1 = max(0, rx1), max(0, ry1)
                cx2, cy2 = min(self.doc_size[0], rx2), min(self.doc_size[1], ry2)
                
                w_new, h_new = cx2 - cx1, cy2 - cy1
                if w_new <= 0 or h_new <= 0: return
                offset_x_change, offset_y_change = cx1, cy1
            else:
                x, y = int(self.entry_x.get()), int(self.entry_y.get())
                w, h = int(self.entry_w.get()), int(self.entry_h.get())
                img_w, img_h = self.doc_size

                if w <= 0 or h <= 0: raise ValueError(self.t["err_dim"])
                x, y = max(0, x), max(0, y)
                w, h = min(w, img_w - x), min(h, img_h - y)
                
                w_new, h_new = w, h
                offset_x_change, offset_y_change = x, y

            self.zapisz_stan_do_historii()
            
            for warstwa in self.warstwy: 
                warstwa['offset_x'] -= offset_x_change
                warstwa['offset_y'] -= offset_y_change
                
            self.doc_size = (w_new, h_new)
            
            self.ustaw_narzedzie(None)
            self.komponuj_i_wyswietl()
            
        except ValueError as e:
            messagebox.showerror(self.t["err_val"], f"{self.t['err_val']} {e}")
        except Exception as e:
            messagebox.showerror(self.t["msg_err_title"], f"Błąd kadrowania: {e}")

    def canvas_to_image_coords(self, c_x, c_y):
        if not self.doc_size: return 0, 0
        rel_x = c_x - self.canvas_img_x_offset
        rel_y = c_y - self.canvas_img_y_offset
        r_x = self.doc_size[0] / self.display_width
        r_y = self.doc_size[1] / self.display_height
        return int(rel_x * r_x), int(rel_y * r_y)

    def zastosuj_rysowanie(self, typ, end_x=None, end_y=None):
        self.zatwierdz_podglad()
        
        w = None
        is_mask = False
        if self.aktywna_warstwa != -1 and self.warstwy:
            w = self.warstwy[self.aktywna_warstwa]
            is_mask = w.get('edycja_maski', False)
            
        if typ == 'brush':
            self.zapisz_stan_do_historii()
            
            if w and is_mask and w.get('maska') is not None:
                if w.get('is_text'): w.pop('is_text', None)
                img = w['maska']
                r, g, b = tuple(int(self.current_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
                fill_color = int(r * 0.299 + g * 0.587 + b * 0.114)
                
                draw = ImageDraw.Draw(img)
                rozmiar = int(self.slider_size.get())
                ox = w.get('offset_x', 0)
                oy = w.get('offset_y', 0)

                if len(self.draw_points) == 1:
                    px, py = self.draw_points[0]
                    rx, ry = self.canvas_to_image_coords(px, py)
                    draw.ellipse([rx - ox - rozmiar//2, ry - oy - rozmiar//2, rx - ox + rozmiar//2, ry - oy + rozmiar//2], fill=fill_color)
                elif len(self.draw_points) > 1:
                    real_pts = []
                    for px, py in self.draw_points:
                        rx, ry = self.canvas_to_image_coords(px, py)
                        real_pts.append((rx - ox, ry - oy))
                    draw.line(real_pts, fill=fill_color, width=rozmiar, joint="curve")

            elif w and w['nazwa'] == self.t["brush"] and not is_mask:
                if w.get('is_text'): w.pop('is_text', None)
                img = w['obraz']
                fill_color = tuple(int(self.current_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)) + (255,)
                
                draw = ImageDraw.Draw(img)
                rozmiar = int(self.slider_size.get())
                ox = w.get('offset_x', 0)
                oy = w.get('offset_y', 0)

                if len(self.draw_points) == 1:
                    px, py = self.draw_points[0]
                    rx, ry = self.canvas_to_image_coords(px, py)
                    draw.ellipse([rx - ox - rozmiar//2, ry - oy - rozmiar//2, rx - ox + rozmiar//2, ry - oy + rozmiar//2], fill=fill_color)
                elif len(self.draw_points) > 1:
                    real_pts = []
                    for px, py in self.draw_points:
                        rx, ry = self.canvas_to_image_coords(px, py)
                        real_pts.append((rx - ox, ry - oy))
                    draw.line(real_pts, fill=fill_color, width=rozmiar, joint="curve")
            
            else:
                img = Image.new("RGBA", self.doc_size, (0, 0, 0, 0))
                draw = ImageDraw.Draw(img)
                rozmiar = int(self.slider_size.get())
                fill_color = tuple(int(self.current_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)) + (255,)
                
                if len(self.draw_points) == 1:
                    px, py = self.draw_points[0]
                    rx, ry = self.canvas_to_image_coords(px, py)
                    draw.ellipse([rx - rozmiar//2, ry - rozmiar//2, rx + rozmiar//2, ry + rozmiar//2], fill=fill_color)
                elif len(self.draw_points) > 1:
                    real_pts = [self.canvas_to_image_coords(px, py) for px, py in self.draw_points]
                    draw.line(real_pts, fill=fill_color, width=rozmiar, joint="curve")
                
                nazwa = self.t["brush"]
                idx = self.aktywna_warstwa + 1 if self.aktywna_warstwa != -1 else 0
                
                self.warstwy.insert(idx, {
                    'nazwa': nazwa, 
                    'obraz': img,
                    'widoczna': True, 
                    'krycie': 1.0, 
                    'tryb': 'Normal', 
                    'maska': None, 
                    'edycja_maski': False, 
                    'offset_x': 0, 
                    'offset_y': 0
                })
                
                self.ustaw_aktywna_warstwe(idx)
                
        elif typ == 'shape' and end_x and end_y:
            rx1, ry1 = self.canvas_to_image_coords(self.last_x, self.last_y)
            rx2, ry2 = self.canvas_to_image_coords(end_x, end_y)
            shape_type = self.aktywny_ksztalt
            rozmiar = int(self.slider_size.get())
            fill_color = tuple(int(self.current_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)) + (255,)
            
            sw = abs(rx2 - rx1)
            sh = abs(ry2 - ry1)
            ox = min(rx1, rx2)
            oy = min(ry1, ry2)
            
            if sw < 2 and sh < 2: 
                if self.temp_draw_id: self.canvas.delete(self.temp_draw_id)
                return

            self.zapisz_stan_do_historii()

            pad = rozmiar + 2
            img = Image.new("RGBA", (sw + 2*pad, sh + 2*pad), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            box = [pad, pad, sw + pad, sh + pad]
            
            if shape_type == self.t["shape_rect"]:
                draw.rectangle(box, outline=fill_color, width=rozmiar)
            elif shape_type == self.t["shape_ellipse"]:
                draw.ellipse(box, outline=fill_color, width=rozmiar)
            elif shape_type == self.t["shape_line"]:
                x1 = (rx1 - ox) + pad
                y1 = (ry1 - oy) + pad
                x2 = (rx2 - ox) + pad
                y2 = (ry2 - oy) + pad
                draw.line([x1, y1, x2, y2], fill=fill_color, width=rozmiar, joint="curve")
            elif shape_type == self.t["shape_triangle"]:
                pts = [(pad, sh + pad), (sw//2 + pad, pad), (sw + pad, sh + pad)]
                draw.polygon(pts, outline=fill_color, width=rozmiar)
            elif shape_type == self.t["shape_rounded"]:
                radius = min(sw, sh) // 5
                draw.rounded_rectangle(box, radius=radius, outline=fill_color, width=rozmiar)
                
            if self.temp_draw_id: self.canvas.delete(self.temp_draw_id)
            
            nazwa = f"K: {shape_type[:5]}"
            idx = self.aktywna_warstwa + 1 if self.aktywna_warstwa != -1 else 0
            
            self.warstwy.insert(idx, {
                'nazwa': nazwa, 
                'obraz': img,
                'widoczna': True, 
                'krycie': 1.0, 
                'tryb': 'Normal', 
                'maska': None, 
                'edycja_maski': False, 
                'offset_x': ox - pad, 
                'offset_y': oy - pad
            })
            
            self.ustaw_aktywna_warstwe(idx)
            self.ustaw_narzedzie('move')
            
        self.komponuj_i_wyswietl()

    def zastosuj_wypelnienie(self, x, y):
        if self.aktywna_warstwa == -1: return
        self.zatwierdz_podglad()
        self.zapisz_stan_do_historii()
        
        w = self.warstwy[self.aktywna_warstwa]
        
        if not w.get('edycja_maski') and w.get('is_text'): w.pop('is_text', None)
        
        layer_x = x - w.get('offset_x', 0)
        layer_y = y - w.get('offset_y', 0)
        
        is_mask = w.get('edycja_maski', False)
        if is_mask and w.get('maska') is not None:
            img = w['maska']
            r, g, b = tuple(int(self.current_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
            fill_color = int(r * 0.299 + g * 0.587 + b * 0.114)
        else:
            img = w['obraz']
            fill_color = tuple(int(self.current_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)) + (255,)

        ImageDraw.floodfill(img, (layer_x, layer_y), fill_color)
        self.komponuj_i_wyswietl()

    def zmien_czcionke_tekstu(self, wartosc):
        if self.aktywna_warstwa != -1 and self.warstwy[self.aktywna_warstwa].get('is_text'):
            self.zapisz_stan_do_historii()
            self.warstwy[self.aktywna_warstwa]['text_font'] = wartosc
            self.renderuj_warstwe_tekstu(self.aktywna_warstwa)
            self.komponuj_i_wyswietl()

    def zmien_rozmiar_tekstu(self, wartosc):
        if self.aktywna_warstwa != -1 and self.warstwy[self.aktywna_warstwa].get('is_text'):
            if not getattr(self, 'text_resize_started', False):
                self.zapisz_stan_do_historii()
                self.text_resize_started = True
            self.warstwy[self.aktywna_warstwa]['text_size'] = int(wartosc)
            self.renderuj_warstwe_tekstu(self.aktywna_warstwa)
            self.komponuj_i_wyswietl()

    def zatwierdz_rozmiar_tekstu(self):
        self.text_resize_started = False

    def renderuj_warstwe_tekstu(self, idx):
        w = self.warstwy[idx]
        if not w.get('is_text'): return
        
        pusta = Image.new("RGBA", self.doc_size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(pusta)
        
        font_name = w.get('text_font', 'Arial')
        font = None
        
        try_paths = [
            font_name,
            font_name + ".ttf", 
            font_name + ".ttc", 
            font_name.lower() + ".ttf",
            font_name.replace(" ", "") + ".ttf",
            font_name.replace(" ", "") + ".ttc"
        ]
        
        base_dirs = [""]
        if sys.platform == "darwin":
            base_dirs += ["/Library/Fonts/", "/System/Library/Fonts/", "/System/Library/Fonts/Supplemental/", os.path.expanduser("~/Library/Fonts/")]
        elif sys.platform == "win32":
            base_dirs += ["C:\\Windows\\Fonts\\"]
        else:
            base_dirs += ["/usr/share/fonts/truetype/", "/usr/share/fonts/"]
            
        for p in try_paths:
            for bd in base_dirs:
                try:
                    font = ImageFont.truetype(os.path.join(bd, p), size=w['text_size'])
                    break
                except: pass
            if font: break
                
        if not font:
            try: font = ImageFont.truetype("arial.ttf", size=w['text_size'])
            except: 
                try: font = ImageFont.truetype("Arial.ttf", size=w['text_size'])
                except: font = ImageFont.load_default()
        
        draw.text((w['text_x'], w['text_y']), w['text_content'], fill=w['text_color'], font=font)
        w['obraz'] = pusta

    def wstaw_tekst(self, x, y):
        tekst = simpledialog.askstring("Tekst", "Wpisz tekst:")
        if not tekst: return self.ustaw_narzedzie('text')
        
        self.zatwierdz_podglad()
        self.zapisz_stan_do_historii()
        
        rx, ry = self.canvas_to_image_coords(x, y)
        nazwa = f"T: {tekst[:8]}"
        idx = self.aktywna_warstwa + 1 if self.aktywna_warstwa != -1 else 0
        fill_color = tuple(int(self.current_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)) + (255,)
        rozmiar_czcionki = int(self.slider_font_size.get())
        wybrana_czcionka = self.combo_font.get()
        
        self.warstwy.insert(idx, {
            'nazwa': nazwa, 
            'obraz': Image.new("RGBA", self.doc_size, (0, 0, 0, 0)),
            'widoczna': True, 
            'krycie': 1.0, 
            'tryb': 'Normal', 
            'maska': None, 
            'edycja_maski': False, 
            'offset_x': 0, 
            'offset_y': 0,
            'is_text': True,
            'text_content': tekst,
            'text_x': rx,
            'text_y': ry,
            'text_color': fill_color,
            'text_size': rozmiar_czcionki,
            'text_font': wybrana_czcionka
        })
        
        self.renderuj_warstwe_tekstu(idx)
        self.ustaw_aktywna_warstwe(idx)
        self.ustaw_narzedzie('move')
        self.komponuj_i_wyswietl()

    def on_canvas_press(self, event):
        if not self.aktywne_narzedzie or not self.doc_size: return
        
        if self.aktywna_warstwa == -1 and self.aktywne_narzedzie in ['move', 'fill']: 
            return
            
        self.zatwierdz_podglad()
        x, y = event.x, event.y
        self.last_x, self.last_y = x, y

        if self.aktywne_narzedzie == 'move':
            self.zapisz_stan_do_historii()
            self.move_start_x = x
            self.move_start_y = y
            w = self.warstwy[self.aktywna_warstwa]
            self.move_start_offset_x = w.get('offset_x', 0)
            self.move_start_offset_y = w.get('offset_y', 0)
        elif self.aktywne_narzedzie == 'crop':
            if not self.rect_coords: 
                self.akcja_myszy = 'draw'
                self.rect_coords = [x, y, x, y]
            else:
                x1, y1, x2, y2 = self.rect_coords
                xm, xx = min(x1, x2), max(x1, x2)
                ym, yx = min(y1, y2), max(y1, y2)
                self.rect_coords = [xm, ym, xx, yx]
                
                t = 15
                if abs(x - xm) < t and abs(y - ym) < t: self.akcja_myszy = 'resize_tl'
                elif abs(x - xx) < t and abs(y - ym) < t: self.akcja_myszy = 'resize_tr'
                elif abs(x - xm) < t and abs(y - yx) < t: self.akcja_myszy = 'resize_bl'
                elif abs(x - xx) < t and abs(y - yx) < t: self.akcja_myszy = 'resize_br'
                elif xm < x < xx and ym < y < yx: self.akcja_myszy = 'move'
                else: 
                    self.akcja_myszy = 'draw'
                    self.rect_coords = [x, y, x, y]
            self.rysuj_ramke_na_plotnie()
        elif self.aktywne_narzedzie == 'brush': 
            self.draw_points = [(x, y)]
        elif self.aktywne_narzedzie == 'fill':
            rx, ry = self.canvas_to_image_coords(x, y)
            self.zastosuj_wypelnienie(rx, ry)
        elif self.aktywne_narzedzie == 'text': 
            self.wstaw_tekst(x, y)
        elif self.aktywne_narzedzie == 'shape': 
            shape_type = self.aktywny_ksztalt
            color = self.get_draw_color()
            width = int(self.slider_size.get())
            if shape_type == self.t["shape_rect"] or shape_type == self.t["shape_rounded"]:
                self.temp_draw_id = self.canvas.create_rectangle(x,y,x,y, outline=color, width=width)
            elif shape_type == self.t["shape_ellipse"]:
                self.temp_draw_id = self.canvas.create_oval(x,y,x,y, outline=color, width=width)
            elif shape_type == self.t["shape_line"]:
                self.temp_draw_id = self.canvas.create_line(x,y,x,y, fill=color, width=width, capstyle=tk.ROUND)
            elif shape_type == self.t["shape_triangle"]:
                self.temp_draw_id = self.canvas.create_polygon(x,y,x,y,x,y, outline=color, fill="", width=width)

    def on_canvas_drag(self, event):
        if not self.aktywne_narzedzie or not self.doc_size: return
        
        if self.aktywna_warstwa == -1 and self.aktywne_narzedzie in ['move']: 
            return
            
        x, y = event.x, event.y
        
        if self.aktywne_narzedzie == 'move':
            dx = x - self.move_start_x
            dy = y - self.move_start_y
            r_x = self.doc_size[0] / self.display_width
            r_y = self.doc_size[1] / self.display_height
            
            self.warstwy[self.aktywna_warstwa]['offset_x'] = self.move_start_offset_x + int(dx * r_x)
            self.warstwy[self.aktywna_warstwa]['offset_y'] = self.move_start_offset_y + int(dy * r_y)
            self.komponuj_i_wyswietl()
            
        elif self.aktywne_narzedzie == 'crop' and self.akcja_myszy:
            dx, dy = x - self.last_x, y - self.last_y
            if self.akcja_myszy == 'draw': 
                self.rect_coords[2], self.rect_coords[3] = x, y
            elif self.akcja_myszy == 'move':
                self.rect_coords[0] += dx
                self.rect_coords[1] += dy
                self.rect_coords[2] += dx
                self.rect_coords[3] += dy
            elif self.akcja_myszy == 'resize_tl': 
                self.rect_coords[0], self.rect_coords[1] = x, y
            elif self.akcja_myszy == 'resize_tr': 
                self.rect_coords[2], self.rect_coords[1] = x, y
            elif self.akcja_myszy == 'resize_bl': 
                self.rect_coords[0], self.rect_coords[3] = x, y
            elif self.akcja_myszy == 'resize_br': 
                self.rect_coords[2], self.rect_coords[3] = x, y
            
            self.last_x, self.last_y = x, y
            self.rysuj_ramke_na_plotnie()
        elif self.aktywne_narzedzie == 'brush':
            self.canvas.create_line(self.last_x, self.last_y, x, y, fill=self.get_draw_color(), width=self.slider_size.get(), capstyle=tk.ROUND, smooth=True)
            self.draw_points.append((x, y))
            self.last_x, self.last_y = x, y
        elif self.aktywne_narzedzie == 'shape' and self.temp_draw_id:
            shape_type = self.aktywny_ksztalt
            if shape_type == self.t["shape_triangle"]:
                self.canvas.coords(self.temp_draw_id, self.last_x, y, (self.last_x + x)/2, self.last_y, x, y)
            else:
                self.canvas.coords(self.temp_draw_id, self.last_x, self.last_y, x, y)

    def on_canvas_release(self, event):
        if not self.aktywne_narzedzie or not self.doc_size: return
        if self.aktywne_narzedzie == 'brush': self.zastosuj_rysowanie('brush')
        elif self.aktywne_narzedzie == 'shape': self.zastosuj_rysowanie('shape', event.x, event.y)

    def rysuj_ramke_na_plotnie(self):
        self.canvas.delete("crop_element")
        if not self.rect_coords: return
        x1, y1, x2, y2 = self.rect_coords
        self.canvas.create_rectangle(x1, y1, x2, y2, outline='#00ff00', width=2, dash=(5,5), tags="crop_element")
        r, k = 6, '#00ff00'
        for px, py in [(x1,y1), (x2,y1), (x1,y2), (x2,y2)]: 
            self.canvas.create_oval(px-r, py-r, px+r, py+r, fill=k, tags="crop_element")

    def ustaw_narzedzie(self, narzedzie):
        if not self.warstwy and narzedzie not in [None, 'crop']: return
        self.zatwierdz_podglad()
        self.canvas.delete("crop_element"); self.rect_coords = None; self.canvas.config(cursor="")
        
        if self.aktywne_narzedzie == narzedzie:
            self.aktywne_narzedzie = None
            nazwa = self.t["none"]
        else:
            self.aktywne_narzedzie = narzedzie
            if narzedzie == 'crop': self.canvas.config(cursor="cross"); nazwa = self.t["crop_on"]
            elif narzedzie == 'brush': self.canvas.config(cursor="pencil"); nazwa = self.t["brush"]
            elif narzedzie == 'fill': self.canvas.config(cursor="tcross"); nazwa = self.t["fill"]
            elif narzedzie == 'text': self.canvas.config(cursor="xterm"); nazwa = self.t["text"]
            elif narzedzie == 'shape': self.canvas.config(cursor="crosshair"); nazwa = self.aktywny_ksztalt
            elif narzedzie == 'move': self.canvas.config(cursor="fleur"); nazwa = self.t["move"]
            else: nazwa = self.t["none"]
            
        self.lbl_aktywne_narz.configure(text=f"{self.t['active_tool']} {nazwa}")
        
        if self.aktywne_narzedzie == 'crop':
            self.btn_crop.configure(text=self.t["crop_off"], border_width=2)
        else:
            self.btn_crop.configure(text=self.t["crop_on"], border_width=1)

    def przy_zmianie_rozmiaru(self, event):
        self.canvas.coords("help_text", event.width / 2, event.height / 2)
        if self.warstwy:
            if self.resize_timer: self.after_cancel(self.resize_timer)
            self.resize_timer = self.after(150, lambda: self.ustaw_narzedzie('crop') if self.aktywne_narzedzie == 'crop' else self.komponuj_i_wyswietl())

    def zapisz_obraz(self, event=None):
        self.zatwierdz_podglad()
        if not self.skompilowany_obraz: return
        sciezka = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg")])
        if sciezka:
            try:
                zapisz_img = self.skompilowany_obraz
                if sciezka.lower().endswith((".jpg", ".jpeg")):
                    tlo = Image.new("RGB", zapisz_img.size, (255, 255, 255))
                    tlo.paste(zapisz_img, mask=zapisz_img.split()[3]) 
                    zapisz_img = tlo
                zapisz_img.save(sciezka)
                messagebox.showinfo(self.t["msg_saved_title"], self.t["msg_saved"])
            except Exception as e:
                messagebox.showerror(self.t["msg_err_title"], f"{self.t['err_save']} {e}")

if __name__ == "__main__":
    aplikacja = PyPhoto()
    aplikacja.mainloop()