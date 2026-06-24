#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ==============================================================================
# Nazwa pliku: PyPhoto.py
# 
# Copyright (c) 2026 Daniel Kaliski
# Ten kod jest objęty licencją GNU GENERAL PUBLIC LICENSE GPL-3.0.
# ==============================================================================

import sys
import os
import math
import base64
from io import BytesIO

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
        "new": "Nowy obraz...",
        "new_w": "Szerokość (px):",
        "new_h": "Wysokość (px):",
        "toggle_grid": "Pokaż / Ukryj siatkę",
        "bg_color": "Kolor tła",
        "transparent_bg": "Przezroczyste tło",
        "ok": "OK",
        "cancel": "Anuluj",
        "open": "Otwórz obraz...",
        "save": "Eksportuj obraz...",
        "export_svg": "Eksportuj do SVG...",
        "close": "Zamknij",
        "undo": "Cofnij (Undo)",
        "transform": "Transformacje:",
        "rotate": "Obróć o 90°",
        "flip_h": "Odbij w poziomie",
        "flip_v": "Odbij w pionie",
        "adjust": "Dopasowanie:",
        "exposure": "Ekspozycja",
        "white_balance": "Temperatura",
        "brightness": "Jasność",
        "contrast": "Kontrast",
        "saturation": "Nasycenie",
        "sharpness": "Ostrość",
        "scale": "Powiększ",
        "interactive": "Narzędzia interaktywne:",
        "move": "Zaznacz",
        "node": "Edycja węzłów",
        "pen": "Pióro Wektorowe",
        "fill": "Wypełnij",
        "text": "Tekst",
        "shape_rect": "Prostokąt",
        "shape_ellipse": "Elipsa",
        "shape_line": "Linia",
        "shape_triangle": "Trójkąt",
        "shape_rounded": "Zaokr. Prostokąt",
        "shape_curve": "Krzywa (Bézier)",
        "color_outline": "Kolor linii",
        "color_fill": "Kolor tła",
        "no_fill": "Brak",
        "size": "Grubość:",
        "roundness": "Zaokrąglenie rogów",
        "bulge": "Krzywizna boków",
        "select_font": "Wybierz czcionkę:",
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
        "crop_on": "Kadruj",
        "crop_off": "Anuluj kadrowanie",
        "crop_apply": "Zastosuj",
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
        "help": "Wczytaj z menu: Plik > Otwórz, lub Plik > Nowy",
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
        "new": "New Image...",
        "new_w": "Width (px):",
        "new_h": "Height (px):",
        "toggle_grid": "Toggle Grid",
        "bg_color": "Background Color",
        "transparent_bg": "Transparent Background",
        "ok": "OK",
        "cancel": "Cancel",
        "open": "Open image...",
        "save": "Export Image...",
        "export_svg": "Export to SVG...",
        "close": "Close",
        "undo": "Undo",
        "transform": "Transformations:",
        "rotate": "Rotate 90°",
        "flip_h": "Flip Horizontally",
        "flip_v": "Flip Vertically",
        "adjust": "Layer Adjustments:",
        "exposure": "Exposure",
        "white_balance": "Temperature",
        "brightness": "Brightness",
        "contrast": "Contrast",
        "saturation": "Saturation",
        "sharpness": "Sharpness",
        "scale": "Zoom",
        "interactive": "Interactive Tools:",
        "move": "Select",
        "node": "Node Editing",
        "pen": "Pen Tool",
        "fill": "Fill",
        "text": "Text",
        "shape_rect": "Rectangle",
        "shape_ellipse": "Ellipse",
        "shape_line": "Line",
        "shape_triangle": "Triangle",
        "shape_rounded": "Rounded Rect",
        "shape_curve": "Curve (Bezier)",
        "color_outline": "Line Color",
        "color_fill": "Fill Color",
        "no_fill": "None",
        "size": "Thickness:",
        "roundness": "Corner Radius",
        "bulge": "Side Curvature",
        "select_font": "Select font:",
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
        "crop_on": "Crop",
        "crop_off": "Cancel Crop",
        "crop_apply": "Apply",
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
        "help": "Load from menu: File > Open, or File > New",
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

class MockEvent:
    def __init__(self, x, y):
        self.x = x
        self.y = y

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
        self.tk_icons = {}
        ikony_katalog = self.pobierz_sciezke_zasobu("ikony")
        
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
                except Exception: pass
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

        try:
            dpi = self.winfo_fpixels('1i')
            skala = dpi / 96.0
            menu_icon_size = int(24 * skala)
        except Exception:
            menu_icon_size = 24

        def load_tk_icon(names, size=None):
            if size is None:
                size = (menu_icon_size, menu_icon_size)
                
            if isinstance(names, str): names = [names]
            for name in names:
                path = os.path.join(ikony_katalog, name)
                if os.path.exists(path):
                    try:
                        img = Image.open(path).convert("RGBA")
                        img = img.resize(size, Image.Resampling.LANCZOS)
                        r, g, b, a = img.split()
                        
                        r = r.point(lambda _: 0)
                        g = g.point(lambda _: 0)
                        b = b.point(lambda _: 0)
                        
                        white_img = Image.merge("RGBA", (r, g, b, a))
                        return ImageTk.PhotoImage(white_img)
                    except Exception: pass
            return None

        self.tk_icons["new"] = load_tk_icon(["add_box.png", "add.png"])
        self.tk_icons["open"] = load_tk_icon(["folder_open.png", "folder.png", "open.png"])
        self.tk_icons["save"] = load_tk_icon(["save.png", "download.png"])
        self.tk_icons["close"] = load_tk_icon(["close.png", "exit.png", "cancel.png"])
        self.tk_icons["undo"] = load_tk_icon(["undo.png", "history.png"])
        self.tk_icons["rotate"] = load_tk_icon(["rotate_right.png", "rotate.png"])
        self.tk_icons["flip_h"] = load_tk_icon(["flip_h.png", "swap_horiz.png"])
        self.tk_icons["flip_v"] = load_tk_icon(["flip_v.png", "swap_vert.png"])
        self.tk_icons["remove_bg"] = load_tk_icon(["auto_fix_high.png", "magic.png", "remove_bg.png"])
        self.tk_icons["move"] = load_tk_icon(["near_me.png", "pan_tool.png", "arrows.png", "open_with.png"])
        self.tk_icons["edit"] = load_tk_icon(["edit.png", "create.png"])
        self.tk_icons["node"] = load_tk_icon(["node-2.png"])  
        self.tk_icons["pen"] = load_tk_icon(["pen.png"])
        self.tk_icons["fill"] = load_tk_icon(["format_color_fill.png", "fill.png", "palette.png"])
        self.tk_icons["text"] = load_tk_icon(["text_fields.png", "title.png", "text.png"])
        self.tk_icons["shape_rect"] = load_tk_icon(["crop_square.png", "rectangle.png"])
        self.tk_icons["shape_ellipse"] = load_tk_icon(["radio_button_unchecked.png", "ellipse.png", "circle.png"])
        self.tk_icons["shape_line"] = load_tk_icon(["remove.png", "line.png"])
        self.tk_icons["shape_triangle"] = load_tk_icon(["change_history.png", "triangle.png"])
        self.tk_icons["shape_rounded"] = load_tk_icon(["crop_din.png", "rounded_rect.png"])
        self.tk_icons["shape_curve"] = load_tk_icon(["gesture.png", "line.png"])
        self.tk_icons["bw"] = load_tk_icon(["filter_b_and_w.png", "bw.png"])
        self.tk_icons["blur"] = load_tk_icon(["blur_on.png", "blur.png"])
        self.tk_icons["sharpen"] = load_tk_icon(["details.png", "sharpen.png"])
        self.tk_icons["invert"] = load_tk_icon(["invert_colors.png", "invert.png"])
        self.tk_icons["emboss"] = load_tk_icon(["texture.png", "emboss.png"])
        self.tk_icons["edges"] = load_tk_icon(["polyline.png", "edges.png"])
        self.tk_icons["contour"] = load_tk_icon(["gesture.png", "contour.png"])
        self.tk_icons["smooth"] = load_tk_icon(["blur_linear.png", "smooth.png"])
        self.tk_icons["posterize"] = load_tk_icon(["photo_filter.png", "posterize.png"])
        self.tk_icons["solarize"] = load_tk_icon(["wb_sunny.png", "solarize.png"])
        self.tk_icons["lang_pl"] = load_tk_icon(["translate.png", "language.png"])
        self.tk_icons["lang_en"] = load_tk_icon(["public.png", "language.png"])

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
        
        self.color_outline = "#ffffff" 
        self.color_fill = None
        
        self.pen_points = []
        
        self.warstwa_podgladowa = None
        self.blokuj_podglad = False
        self.text_resize_started = False
        self.live_edit_started = False
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
        
        ramka_kolorow = ctk.CTkFrame(ramka_opcji, fg_color="transparent")
        ramka_kolorow.pack(fill="x", pady=5)
        
        self.btn_color_outline = ctk.CTkButton(ramka_kolorow, text=self.t["color_outline"], image=self.icons.get("color"), height=32, corner_radius=6, command=self.wybierz_kolor_linii, fg_color="transparent", border_width=1, border_color=self.color_outline, text_color=self.color_outline, hover_color="#333")
        self.btn_color_outline.pack(fill="x", pady=(0, 5))
        
        ramka_fill = ctk.CTkFrame(ramka_kolorow, fg_color="transparent")
        ramka_fill.pack(fill="x")
        
        fill_text = self.t["color_fill"] if self.color_fill else self.t["color_fill"] + f" ({self.t['no_fill']})"
        fill_border = self.color_fill if self.color_fill else "gray50"
        fill_text_color = self.color_fill if self.color_fill else "gray50"
        
        self.btn_color_fill = ctk.CTkButton(ramka_fill, text=fill_text, image=self.icons.get("color"), height=32, corner_radius=6, command=self.wybierz_kolor_tla, fg_color="transparent", border_width=1, border_color=fill_border, text_color=fill_text_color, hover_color="#333")
        self.btn_color_fill.pack(side="left", expand=True, fill="x", padx=(0, 2))
        
        self.btn_no_fill = ctk.CTkButton(ramka_fill, text="X", width=32, height=32, corner_radius=6, command=self.usun_kolor_tla, fg_color="transparent", border_width=1, border_color="#aa0000", text_color="#aa0000", hover_color="#550000")
       
        self.lbl_size = ctk.CTkLabel(self.panel_narzedzi, text=self.t.get("size", "Grubość:"), anchor="w")
        self.lbl_size.pack(fill="x", padx=15, pady=(15, 0))
        self.slider_size = ctk.CTkSlider(self.panel_narzedzi, from_=1, to=100, command=self.aktualizuj_wlasciwosci_obiektu)
        self.slider_size.set(5)
        self.slider_size.pack(fill="x", padx=10, pady=0)

        self.lbl_roundness = ctk.CTkLabel(self.panel_narzedzi, text=self.t.get("roundness", "Zaokrąglenie rogów:"), anchor="w")
        self.lbl_roundness.pack(fill="x", padx=15, pady=(5, 0))
        self.slider_roundness = ctk.CTkSlider(self.panel_narzedzi, from_=0, to=200, command=self.aktualizuj_wlasciwosci_obiektu)
        self.slider_roundness.set(0)
        self.slider_roundness.pack(fill="x", padx=10, pady=0)

        self.lbl_bulge = ctk.CTkLabel(self.panel_narzedzi, text=self.t.get("bulge", "Krzywizna boków:"), anchor="w")
        self.lbl_bulge.pack(fill="x", padx=15, pady=(5, 0))
        self.slider_bulge = ctk.CTkSlider(self.panel_narzedzi, from_=-100, to=100, command=self.aktualizuj_wlasciwosci_obiektu)
        self.slider_bulge.set(0)
        self.slider_bulge.pack(fill="x", padx=10, pady=(0, 10))
        
        self.lbl_select_font = ctk.CTkLabel(self.panel_narzedzi, text=self.t.get("select_font", "Wybierz czcionkę:"), anchor="w", font=ctk.CTkFont(size=13, weight="bold"))
        self.lbl_select_font.pack(fill="x", padx=15, pady=(10, 2))
        
        self.czcionka_var = tk.StringVar(value="Arial")
        czcionki_systemowe = sorted([f for f in tkfont.families() if not f.startswith('@')])
        if not czcionki_systemowe: czcionki_systemowe = ["Arial", "Courier", "Times New Roman", "Comic Sans MS", "Impact"]
        
        self.combo_font = ctk.CTkComboBox(self.panel_narzedzi, variable=self.czcionka_var, values=czcionki_systemowe, command=self.zmien_czcionke_tekstu)
        self.combo_font.pack(fill="x", padx=10, pady=(0, 5))
        
        ramka_czcionka_rozmiar = ctk.CTkFrame(self.panel_narzedzi, fg_color="transparent")
        ramka_czcionka_rozmiar.pack(fill="x", padx=10, pady=5)
        self.lbl_font_size = ctk.CTkLabel(ramka_czcionka_rozmiar, text=self.t["font_size"], width=60, anchor="w", font=ctk.CTkFont(size=13))
        self.lbl_font_size.pack(side="left", padx=(5, 2))
        self.slider_font_size = ctk.CTkSlider(ramka_czcionka_rozmiar, from_=10, to=300, button_color="#888", button_hover_color="#bbb", command=self.zmien_rozmiar_tekstu)
        self.slider_font_size.set(40)
        self.slider_font_size.pack(side="right", expand=True, fill="x")
        self.slider_font_size.bind("<ButtonRelease-1>", lambda e: self.zatwierdz_rozmiar_tekstu())

        ctk.CTkFrame(self.panel_narzedzi, height=2, fg_color="#333").pack(fill="x", pady=15)

        self.lbl_adjust = ctk.CTkLabel(self.panel_narzedzi, text=self.t["adjust"], font=ctk.CTkFont(size=14, weight="bold"))
        self.lbl_adjust.pack(pady=(0, 10))

        suwaki_konfig = [
            ("exposure", "slider_exposure", -3.0, 3.0, 0.0),
            ("brightness", "slider_brightness", 0.1, 2.0, 1.0),
            ("contrast", "slider_contrast", 0.1, 2.0, 1.0),
            ("saturation", "slider_saturation", 0.0, 3.0, 1.0),
            ("white_balance", "slider_white_balance", -100, 100, 0.0),
            ("sharpness", "slider_sharpness", 0.0, 3.0, 1.0),
            ("scale", "slider_scale", 0.1, 3.0, 1.0)
        ]

        for nazwa, attr, min_v, max_v, domyslna in suwaki_konfig:
            ramka_suwaka = ctk.CTkFrame(self.panel_narzedzi, fg_color="transparent")
            ramka_suwaka.pack(fill="x", padx=5, pady=2)
            lbl = ctk.CTkLabel(ramka_suwaka, text=self.t[nazwa], width=80, anchor="w", font=ctk.CTkFont(size=13))
            lbl.pack(side="left", padx=(0, 5))
            
            suwak = ctk.CTkSlider(ramka_suwaka, from_=min_v, to=max_v, command=self.podglad_suwakow)
            suwak.set(domyslna)
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
        self.canvas.bind("<Double-Button-1>", self.on_canvas_double_click)
        self.canvas.bind("<Motion>", self.pokaz_celownik)
        self.canvas.bind("<Leave>", lambda e: self.canvas.delete("pen_cursor"))
        
        self.canvas.bind("<Button-2>", self.zakoncz_narzedzie)
        self.canvas.bind("<Button-3>", self.zakoncz_narzedzie)

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

        self.przypisz_skroty()
        self.utworz_menu()

    def przypisz_skroty(self):
        def sprawdz_focus_i_wykonaj(akcja, arg=None):
            focus_widget = self.focus_get()
            if isinstance(focus_widget, (tk.Entry, ctk.CTkEntry)): return
            if akcja == 'narzedzie':
                if not self.warstwy and arg not in [None, 'crop']: return
                self.ustaw_narzedzie(arg)
            elif akcja == 'cofnij': self.cofnij()
            elif akcja == 'zapisz': self.zapisz_obraz()
            elif akcja == 'otworz': self.otworz_obraz()
            elif akcja == 'nowy': self.nowy_obraz()
            elif akcja == 'siatka': self.przelacz_siatke()

        self.bind_all("<Key-v>", lambda e: sprawdz_focus_i_wykonaj('narzedzie', 'move'))
        self.bind_all("<Key-V>", lambda e: sprawdz_focus_i_wykonaj('narzedzie', 'move'))
        self.bind_all("<Key-n>", lambda e: sprawdz_focus_i_wykonaj('narzedzie', 'node'))
        self.bind_all("<Key-N>", lambda e: sprawdz_focus_i_wykonaj('narzedzie', 'node'))
        self.bind_all("<Key-p>", lambda e: sprawdz_focus_i_wykonaj('narzedzie', 'pen'))
        self.bind_all("<Key-P>", lambda e: sprawdz_focus_i_wykonaj('narzedzie', 'pen'))
        self.bind_all("<Key-t>", lambda e: sprawdz_focus_i_wykonaj('narzedzie', 'text'))
        self.bind_all("<Key-T>", lambda e: sprawdz_focus_i_wykonaj('narzedzie', 'text'))
        self.bind_all("<Key-c>", lambda e: sprawdz_focus_i_wykonaj('narzedzie', 'crop'))
        self.bind_all("<Key-C>", lambda e: sprawdz_focus_i_wykonaj('narzedzie', 'crop'))
        self.bind_all("<Key-f>", lambda e: sprawdz_focus_i_wykonaj('narzedzie', 'fill'))
        self.bind_all("<Key-F>", lambda e: sprawdz_focus_i_wykonaj('narzedzie', 'fill'))
        
        self.bind_all("<Control-z>", lambda e: sprawdz_focus_i_wykonaj('cofnij'))
        self.bind_all("<Control-Z>", lambda e: sprawdz_focus_i_wykonaj('cofnij'))
        self.bind_all("<Command-z>", lambda e: sprawdz_focus_i_wykonaj('cofnij'))
        self.bind_all("<Command-Z>", lambda e: sprawdz_focus_i_wykonaj('cofnij'))
        
        self.bind_all("<Control-s>", lambda e: sprawdz_focus_i_wykonaj('zapisz'))
        self.bind_all("<Control-S>", lambda e: sprawdz_focus_i_wykonaj('zapisz'))
        self.bind_all("<Command-s>", lambda e: sprawdz_focus_i_wykonaj('zapisz'))
        self.bind_all("<Command-S>", lambda e: sprawdz_focus_i_wykonaj('zapisz'))
        
        self.bind_all("<Control-o>", lambda e: sprawdz_focus_i_wykonaj('otworz'))
        self.bind_all("<Control-O>", lambda e: sprawdz_focus_i_wykonaj('otworz'))
        self.bind_all("<Command-o>", lambda e: sprawdz_focus_i_wykonaj('otworz'))
        self.bind_all("<Command-O>", lambda e: sprawdz_focus_i_wykonaj('otworz'))
        
        self.bind_all("<Control-n>", lambda e: sprawdz_focus_i_wykonaj('nowy'))
        self.bind_all("<Control-N>", lambda e: sprawdz_focus_i_wykonaj('nowy'))
        self.bind_all("<Command-n>", lambda e: sprawdz_focus_i_wykonaj('nowy'))
        self.bind_all("<Command-N>", lambda e: sprawdz_focus_i_wykonaj('nowy'))
        
        self.bind_all("<Control-g>", lambda e: sprawdz_focus_i_wykonaj('siatka'))
        self.bind_all("<Command-g>", lambda e: sprawdz_focus_i_wykonaj('siatka'))
        
        self.bind_all("<Return>", self.zakoncz_narzedzie)
        self.bind_all("<Escape>", self.zakoncz_narzedzie)

    def uaktywnij_autoukrywanie_paska(self, ramka_skrolowana):
        def sprawdz_pasek(event=None):
            try:
                canvas_h = ramka_skrolowana._parent_canvas.winfo_height()
                content_h = ramka_skrolowana._parent_frame.winfo_reqheight()
                if content_h <= canvas_h:
                    ramka_skrolowana._scrollbar.grid_forget()
                else:
                    ramka_skrolowana._scrollbar.grid(row=0, column=1, sticky="ns")
            except Exception: pass
        ramka_skrolowana._parent_canvas.bind("<Configure>", sprawdz_pasek, add="+")
        ramka_skrolowana._parent_frame.bind("<Configure>", sprawdz_pasek, add="+")
        self.after(100, sprawdz_pasek)

    def odswiez_pola_kadrowania(self):
        if not self.rect_coords or not self.doc_size: return
        rx1, ry1 = self.canvas_to_image_coords(min(self.rect_coords[0], self.rect_coords[2]), min(self.rect_coords[1], self.rect_coords[3]))
        rx2, ry2 = self.canvas_to_image_coords(max(self.rect_coords[0], self.rect_coords[2]), max(self.rect_coords[1], self.rect_coords[3]))
        cx1, cy1 = max(0, rx1), max(0, ry1)
        cx2, cy2 = min(self.doc_size[0], rx2), min(self.doc_size[1], ry2)
        self.aktualizuj_wymiary_w_polach(cx1, cy1, max(0, cx2 - cx1), max(0, cy2 - cy1))

    def utworz_menu(self):
        if sys.platform == "win32":
            domyslna_czcionka_menu = tkfont.nametofont("TkMenuFont")
            domyslna_czcionka_menu.configure(size=11, family="Segoe UI")
            czcionka_menu = domyslna_czcionka_menu
        else:
            czcionka_menu = ("Arial", 14)
            
        self.option_add('*tearOff', False)
        menubar = tk.Menu(self, font=czcionka_menu)
        
        def add_icon_cmd(menu_parent, label_text, cmd, icon_key=None, state="normal"):
            kw = {"label": label_text, "command": cmd, "state": state}
            if icon_key and self.tk_icons.get(icon_key):
                kw["image"] = self.tk_icons[icon_key]
                kw["compound"] = "left"
            menu_parent.add_command(**kw)
        
        menu_plik = tk.Menu(menubar, font=czcionka_menu)
        add_icon_cmd(menu_plik, self.t.get("new", "Nowy obraz..."), self.nowy_obraz, "new")
        add_icon_cmd(menu_plik, self.t["open"], self.otworz_obraz, "open")
        add_icon_cmd(menu_plik, self.t["save"], self.zapisz_obraz, "save")
        add_icon_cmd(menu_plik, self.t.get("export_svg", "Eksportuj do SVG..."), self.eksportuj_do_svg, "save")
        menu_plik.add_separator()
        add_icon_cmd(menu_plik, self.t["close"], self.zamykanie_okna, "close")
        menubar.add_cascade(label=self.t.get("menu_file", "Plik"), menu=menu_plik)
        
        menu_edycja = tk.Menu(menubar, font=czcionka_menu)
        self.menu_edycja = menu_edycja
        add_icon_cmd(menu_edycja, self.t["undo"], self.cofnij, "undo", state="disabled" if not self.historia else "normal")
        menubar.add_cascade(label=self.t.get("menu_edit", "Edycja"), menu=menu_edycja)
        
        menu_obraz = tk.Menu(menubar, font=czcionka_menu)
        add_icon_cmd(menu_obraz, self.t["rotate"], self.obroc_obraz, "rotate")
        add_icon_cmd(menu_obraz, self.t["flip_h"], self.odbij_w_poziomie, "flip_h")
        add_icon_cmd(menu_obraz, self.t["flip_v"], self.odbij_w_pionie, "flip_v")
        menu_obraz.add_separator()
        add_icon_cmd(menu_obraz, self.t.get("toggle_grid", "Pokaż / Ukryj siatkę"), self.przelacz_siatke) 
        add_icon_cmd(menu_obraz, self.t["remove_bg"], self.usun_tlo, "remove_bg")
        menubar.add_cascade(label=self.t.get("menu_image", "Obraz"), menu=menu_obraz)
        
        menu_narzedzia = tk.Menu(menubar, font=czcionka_menu)
        add_icon_cmd(menu_narzedzia, self.t["move"], lambda: self.ustaw_narzedzie('move'), "move")
        add_icon_cmd(menu_narzedzia, self.t.get("node", "Edycja węzłów"), lambda: self.ustaw_narzedzie('node'), "node")
        add_icon_cmd(menu_narzedzia, self.t["pen"], lambda: self.ustaw_narzedzie('pen'), "pen")
        add_icon_cmd(menu_narzedzia, self.t["fill"], lambda: self.ustaw_narzedzie('fill'), "fill")
        add_icon_cmd(menu_narzedzia, self.t["text"], lambda: self.ustaw_narzedzie('text'), "text")
        
        menu_ksztalty = tk.Menu(menu_narzedzia, font=czcionka_menu)
        add_icon_cmd(menu_ksztalty, self.t["shape_rect"], lambda: self.wybierz_ksztalt(self.t["shape_rect"]), "shape_rect")
        add_icon_cmd(menu_ksztalty, self.t["shape_ellipse"], lambda: self.wybierz_ksztalt(self.t["shape_ellipse"]), "shape_ellipse")
        add_icon_cmd(menu_ksztalty, self.t["shape_line"], lambda: self.wybierz_ksztalt(self.t["shape_line"]), "shape_line")
        add_icon_cmd(menu_ksztalty, self.t["shape_triangle"], lambda: self.wybierz_ksztalt(self.t["shape_triangle"]), "shape_triangle")
        add_icon_cmd(menu_ksztalty, self.t["shape_rounded"], lambda: self.wybierz_ksztalt(self.t["shape_rounded"]), "shape_rounded")
        add_icon_cmd(menu_ksztalty, self.t["shape_curve"], lambda: self.wybierz_ksztalt(self.t["shape_curve"]), "shape_curve")
        menu_narzedzia.add_cascade(label=self.t.get("menu_shapes", "Kształty"), menu=menu_ksztalty)
        menubar.add_cascade(label=self.t.get("menu_tools", "Narzędzia"), menu=menu_narzedzia)
        
        menu_filtry = tk.Menu(menubar, font=czcionka_menu)
        for key in self.klucze_filtrow:
            add_icon_cmd(menu_filtry, self.t[key], lambda k=key: self.zastosuj_wybrany_filtr(self.t[k]), key)
        menubar.add_cascade(label=self.t.get("menu_filters", "Filtry"), menu=menu_filtry)

        menu_jezyk = tk.Menu(menubar, font=czcionka_menu)
        add_icon_cmd(menu_jezyk, "Polski", lambda: self.ustaw_jezyk("pl"), "lang_pl")
        add_icon_cmd(menu_jezyk, "English", lambda: self.ustaw_jezyk("en"), "lang_en")
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
        except: pass
        return "pl"

    def ustaw_pelen_ekran_mac(self):
        w = self.winfo_screenwidth()
        h = self.winfo_screenheight()
        self.geometry(f"{w}x{h}+0+0")

    def get_draw_color(self):
        kolor_hex = self.color_outline
        if self.aktywna_warstwa != -1 and self.warstwy[self.aktywna_warstwa].get('edycja_maski'):
            r, g, b = tuple(int(kolor_hex.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
            gray = int(r * 0.299 + g * 0.587 + b * 0.114)
            return f"#{gray:02x}{gray:02x}{gray:02x}"
        return kolor_hex

    def dystans(self, p1, p2):
        return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
        
    def point_to_segment_dist(self, px, py, x1, y1, x2, y2):
        l2 = (x1 - x2)**2 + (y1 - y2)**2
        if l2 == 0: return self.dystans((px, py), (x1, y1))
        t = max(0, min(1, ((px - x1) * (x2 - x1) + (py - y1) * (y2 - y1)) / l2))
        proj_x = x1 + t * (x2 - x1)
        proj_y = y1 + t * (y2 - y1)
        return self.dystans((px, py), (proj_x, proj_y))
    
    def get_grid_step(self):
        if not self.doc_size: return 100
        r_x = self.display_width / self.doc_size[0]
        if r_x > 3: return 10
        elif r_x > 1.2: return 50
        elif r_x < 0.3: return 500
        return 100

    def snap_to_grid(self, rx, ry):
        if not getattr(self, 'widoczna_siatka', False):
            return rx, ry
        step = self.get_grid_step()
        return round(rx / step) * step, round(ry / step) * step

    def get_snapped_coords(self, c_x, c_y):
        rx, ry = self.canvas_to_image_coords(c_x, c_y)
        snap_node = self.znajdz_najblizszy_wezel(rx, ry)
        if snap_node: return snap_node
        return self.snap_to_grid(rx, ry)
        
    def znajdz_najblizszy_wezel(self, rx, ry):
        prog = 15
        najlepszy = None
        min_d = prog
        for w in self.warstwy:
            if not w['widoczna'] or not w.get('is_object'): continue
            ox, oy = w.get('offset_x', 0), w.get('offset_y', 0)
            pts = []
            if w['obj_typ'] == 'shape':
                if len(w['obj_pts']) == 6:
                    x1, y1, x2, y2, cx, cy = w['obj_pts']
                    pts = [(x1,y1), (x2,y2), (cx,cy)]
                else:
                    x1, y1, x2, y2 = w['obj_pts']
                    pts = [(x1,y1), (x2,y1), (x2,y2), (x1,y2)]
                    if w.get('shape_type') in [self.t.get("shape_line", ""), "Linia", "Line"]:
                        pts = [(x1,y1), (x2,y2)]
                    elif w.get('shape_type') in [self.t.get("shape_triangle", ""), "Trójkąt", "Triangle"]:
                        min_x, max_x, min_y, max_y = min(x1, x2), max(x1, x2), min(y1, y2), max(y1, y2)
                        pts = [(min_x, max_y), (min_x+(max_x-min_x)/2, min_y), (max_x, max_y)]
            elif w['obj_typ'] == 'pen':
                pts = w['obj_pts']
            
            for px, py in pts:
                d = self.dystans((rx, ry), (px+ox, py+oy))
                if d < min_d:
                    min_d = d
                    najlepszy = (px+ox, py+oy)
        return najlepszy

    def pokaz_celownik(self, event):
        self.canvas.delete("pen_cursor")
        if not self.aktywne_narzedzie in ['pen', 'shape']: return
        
        ex, ey = event.x, event.y
        rx, ry = self.canvas_to_image_coords(ex, ey)
        
        is_closing = False
        if self.aktywne_narzedzie == 'pen' and hasattr(self, 'pen_points') and len(self.pen_points) > 2:
            px, py = self.pen_points[0]
            if self.dystans((rx, ry), (px, py)) < 15:
                rx, ry = px, py
                is_closing = True
                
        if not is_closing:
            rx, ry = self.get_snapped_coords(ex, ey)
            
        ex, ey = self.image_to_canvas_coords(rx, ry)
        
        if self.aktywne_narzedzie == 'pen' and hasattr(self, 'pen_points') and self.pen_points:
            px, py = self.image_to_canvas_coords(*self.pen_points[-1])
            self.canvas.create_line(px, py, ex, ey, fill=self.color_outline, width=self.slider_size.get(), dash=(4,4), tags="pen_cursor")
            if is_closing:
                r_close = max(4, int(self.slider_size.get()/2))
                self.canvas.create_oval(ex - r_close - 4, ey - r_close - 4, ex + r_close + 4, ey + r_close + 4, outline="red", width=2, tags="pen_cursor")
        
        r = int(self.slider_size.get() / 2 * (self.display_width / self.doc_size[0] if self.doc_size else 1))
        r = max(1, r)
        self.canvas.create_oval(ex - r, ey - r, ex + r, ey + r, outline="white", tags="pen_cursor")
        self.canvas.create_oval(ex - r - 1, ey - r - 1, ex + r + 1, ey + r + 1, outline="black", tags="pen_cursor")

    def aktualizuj_grubosc_live(self, wartosc):
        ex = self.winfo_pointerx() - self.canvas.winfo_rootx()
        ey = self.winfo_pointery() - self.canvas.winfo_rooty()
        self.pokaz_celownik(MockEvent(ex, ey))
        if self.aktywna_warstwa != -1:
            w = self.warstwy[self.aktywna_warstwa]
            if w.get('is_object') and w.get('obj_typ') in ['shape', 'pen']:
                if not getattr(self, 'live_edit_started', False):
                    self.zapisz_stan_do_historii()
                    self.live_edit_started = True
                w['obj_size'] = int(wartosc)
                self.narysuj_obiekt(w)
                self.komponuj_i_wyswietl()

    def zapisz_koniec_zmiany_live(self):
        self.live_edit_started = False

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
            if widget_name == "btn_color_fill":
                txt = self.t[text_key] if self.color_fill else f"{self.t[text_key]} ({self.t['no_fill']})"
                widget.configure(text=txt)
            else:
                widget.configure(text=self.t[text_key])
        except Exception: pass 

    def przelacz_jezyk(self):
        self.ustaw_jezyk("en" if self.lang == "pl" else "pl")

    def ustaw_jezyk(self, kod):
        if self.lang == kod: return
        stare_t = self.t
        self.lang = kod
        self.t = TEXTS[self.lang]
        
        for w in self.warstwy:
            if w['nazwa'].startswith(stare_t['new_layer'] + " "):
                w['nazwa'] = w['nazwa'].replace(stare_t['new_layer'], self.t['new_layer'], 1)
        self.title(self.t["title"])
        
        elementy = [
            ("lbl_aktywne_narz", "active_tool"), ("btn_color_outline", "color_outline"),
            ("btn_color_fill", "color_fill"), ("lbl_size", "size"), ("lbl_select_font", "select_font"),
            ("lbl_font_size", "font_size"), ("lbl_adjust", "adjust"), ("lbl_brightness", "brightness"),
            ("lbl_contrast", "contrast"), ("lbl_saturation", "saturation"), ("lbl_sharpness", "sharpness"),
            ("lbl_scale", "scale"), ("lbl_exposure", "exposure"), ("lbl_white_balance", "white_balance"),
            ("lbl_kadrowanie", "crop"), ("lbl_w", "width"), ("lbl_h", "height"),
            ("btn_dokladne_crop", "crop_apply"), ("lbl_layers_title", "layers"), ("btn_add_layer", "layer_add"),
            ("btn_insert_layer", "layer_insert"), ("btn_del_layer", "layer_del"), ("btn_add_mask", "mask_add"),
            ("btn_del_mask", "mask_del"), ("lbl_blend", "blend"), ("lbl_opacity", "opacity"), ("text_label", "help")
        ]
        for w_name, t_key in elementy:
            self._update_text(w_name, t_key)

        for key in ["shape_rect", "shape_ellipse", "shape_line", "shape_triangle", "shape_rounded"]:
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

    def get_rgba(self, hex_color):
        if not hex_color: return None
        return tuple(int(hex_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)) + (255,)

    def zmien_czcionke_tekstu(self, wybor):
        if self.aktywna_warstwa != -1:
            w = self.warstwy[self.aktywna_warstwa]
            if w.get('is_text'):
                self.zapisz_stan_do_historii()
                w['text_font'] = wybor
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
            font_name, font_name + ".ttf", font_name + ".ttc", 
            font_name.lower() + ".ttf", font_name.replace(" ", "") + ".ttf", font_name.replace(" ", "") + ".ttc"
        ]
        base_dirs = [""]
        if sys.platform == "darwin": base_dirs += ["/Library/Fonts/", "/System/Library/Fonts/", "/System/Library/Fonts/Supplemental/", os.path.expanduser("~/Library/Fonts/")]
        elif sys.platform == "win32": base_dirs += ["C:\\Windows\\Fonts\\"]
        else: base_dirs += ["/usr/share/fonts/truetype/", "/usr/share/fonts/"]
            
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
        fill_color = self.get_rgba(self.color_outline)
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

    def narysuj_obiekt(self, w):
        ss = 3 
        w_doc, h_doc = self.doc_size
        pts = w['obj_pts']
        rozmiar = w['obj_size']
        typ = w['obj_typ']
        
        roundness = w.get('obj_roundness', 0) * ss
        bulge = w.get('obj_bulge', 0.0)
        
        if not pts:
            w['obraz'] = Image.new("RGBA", self.doc_size, (0, 0, 0, 0))
            return
            
        if typ == 'shape':
            if len(pts) == 6:
                x_coords = [pts[0], pts[2], pts[4]]
                y_coords = [pts[1], pts[3], pts[5]]
            else:
                x_coords = [pts[0], pts[2]]
                y_coords = [pts[1], pts[3]]
        elif typ == 'pen':
            x_coords = [p[0] for p in pts]
            y_coords = [p[1] for p in pts]
            
        margin = rozmiar + 5
        if bulge != 0.0:
            margin += math.hypot(max(x_coords)-min(x_coords), max(y_coords)-min(y_coords)) * abs(bulge)
            
        min_x = max(0, int(math.floor(min(x_coords) - margin)))
        min_y = max(0, int(math.floor(min(y_coords) - margin)))
        max_x = min(w_doc, int(math.ceil(max(x_coords) + margin)))
        max_y = min(h_doc, int(math.ceil(max(y_coords) + margin)))
        
        box_w = max_x - min_x
        box_h = max_y - min_y
        
        if box_w <= 0 or box_h <= 0:
            w['obraz'] = Image.new("RGBA", self.doc_size, (0, 0, 0, 0))
            return
            
        pusta_ss = Image.new("RGBA", (box_w * ss, box_h * ss), (0, 0, 0, 0))
        draw = ImageDraw.Draw(pusta_ss)
        
        def loc_p(x, y):
            return ((x - min_x) * ss, (y - min_y) * ss)
            
        outline_color = w['obj_color']
        fill_color = w.get('obj_fill_color')
        rozmiar_ss = rozmiar * ss
        
        def get_bulged_poly(pts_list):
            out_pts = []
            n = len(pts_list)
            for i in range(n):
                p1 = pts_list[i]
                p2 = pts_list[(i+1)%n]
                dx, dy = p2[0]-p1[0], p2[1]-p1[1]
                length = math.hypot(dx, dy)
                if length == 0: continue
                mx, my = (p1[0]+p2[0])/2, (p1[1]+p2[1])/2
                nx, ny = -dy/length, dx/length
                cx = mx + nx * bulge * length * 0.5
                cy = my + ny * bulge * length * 0.5
                steps = max(10, int(length/10))
                for j in range(steps):
                    t = j / steps
                    x = (1-t)**2 * p1[0] + 2*(1-t)*t * cx + t**2 * p2[0]
                    y = (1-t)**2 * p1[1] + 2*(1-t)*t * cy + t**2 * p2[1]
                    out_pts.append((x, y))
            return out_pts
        
        if typ == 'shape':
            shape_type = w['shape_type']
            if len(pts) == 6:
                px1, py1 = loc_p(pts[0], pts[1])
                px2, py2 = loc_p(pts[2], pts[3])
                pcx, pcy = loc_p(pts[4], pts[5])
            else:
                px1, py1 = loc_p(pts[0], pts[1])
                px2, py2 = loc_p(pts[2], pts[3])
                
            if shape_type in [self.t.get("shape_line", ""), "Linia", "Line"]:
                if bulge != 0.0:
                    dx, dy = px2-px1, py2-py1
                    length = math.hypot(dx, dy)
                    if length > 0:
                        nx, ny = -dy/length, dx/length
                        cx = (px1+px2)/2 + nx * bulge * length * 0.5
                        cy = (py1+py2)/2 + ny * bulge * length * 0.5
                        curve_pts = []
                        steps = max(20, int(length/5))
                        for i in range(steps + 1):
                            t = i / steps
                            x = (1-t)**2 * px1 + 2*(1-t)*t * cx + t**2 * px2
                            y = (1-t)**2 * py1 + 2*(1-t)*t * cy + t**2 * py2
                            curve_pts.append((x, y))
                        draw.line(curve_pts, fill=outline_color, width=rozmiar_ss, joint="curve")
                else:
                    draw.line([px1, py1, px2, py2], fill=outline_color, width=rozmiar_ss, joint="curve")
                    
            elif shape_type in [self.t.get("shape_rect", ""), "Prostokąt", "Rectangle", self.t.get("shape_rounded", ""), "Zaokr. Prostokąt", "Rounded Rect"]:
                bx1, by1, bx2, by2 = min(px1, px2), min(py1, py2), max(px1, px2), max(py1, py2)
                rad = roundness
                
                if shape_type in [self.t.get("shape_rounded", ""), "Zaokr. Prostokąt", "Rounded Rect"]:
                    rad = max(rad, min(abs(bx2-bx1), abs(by2-by1)) // 5)
                    
                max_rad = min(abs(bx2-bx1), abs(by2-by1)) / 2
                rad = int(max(0, min(rad, max_rad)))
                
                if bulge != 0.0:
                    poly = [(bx1, by1), (bx2, by1), (bx2, by2), (bx1, by2)]
                    b_pts = get_bulged_poly(poly)
                    if fill_color: draw.polygon(b_pts, fill=fill_color)
                    draw.line(b_pts + [b_pts[0]], fill=outline_color, width=rozmiar_ss, joint="curve")
                elif rad > 0:
                    draw.rounded_rectangle([bx1, by1, bx2, by2], radius=rad, outline=outline_color, fill=fill_color, width=rozmiar_ss)
                else:
                    draw.rectangle([bx1, by1, bx2, by2], outline=outline_color, fill=fill_color, width=rozmiar_ss)

            elif shape_type in [self.t.get("shape_triangle", ""), "Trójkąt", "Triangle"]:
                bx1, by1, bx2, by2 = min(px1, px2), min(py1, py2), max(px1, px2), max(py1, py2)
                w_t, h_t = bx2 - bx1, by2 - by1
                t_pts = [(bx1, by1+h_t), (bx1+w_t/2, by1), (bx2, by1+h_t)]
                if bulge != 0.0:
                    b_pts = get_bulged_poly(t_pts)
                    if fill_color: draw.polygon(b_pts, fill=fill_color)
                    draw.line(b_pts + [b_pts[0]], fill=outline_color, width=rozmiar_ss, joint="curve")
                else:
                    if fill_color: draw.polygon(t_pts, fill=fill_color)
                    draw.line(t_pts + [t_pts[0]], fill=outline_color, width=rozmiar_ss, joint="curve")
                    
            elif shape_type in [self.t.get("shape_curve", ""), "Krzywa (Bézier)", "Curve (Bezier)"]:
                curve_pts = []
                steps = max(60, int(math.hypot(px2-px1, py2-py1) / 10))
                for i in range(steps + 1):
                    t = i / steps
                    x = (1 - t)**2 * px1 + 2 * (1 - t) * t * pcx + t**2 * px2
                    y = (1 - t)**2 * py1 + 2 * (1 - t) * t * pcy + t**2 * py2
                    curve_pts.append((x, y))
                draw.line(curve_pts, fill=outline_color, width=rozmiar_ss, joint="curve")
                
            elif shape_type in [self.t.get("shape_ellipse", ""), "Elipsa", "Ellipse"]:
                bbox = [min(px1, px2), min(py1, py2), max(px1, px2), max(py1, py2)]
                draw.ellipse(bbox, outline=outline_color, fill=fill_color, width=rozmiar_ss)
                
        elif typ == 'pen':
            loc_pts = [loc_p(p[0], p[1]) for p in pts]
            is_closed = w.get('is_closed', False)
            if len(loc_pts) == 1:
                cx, cy = loc_pts[0]
                draw.ellipse([cx - rozmiar_ss//2, cy - rozmiar_ss//2, cx + rozmiar_ss//2, cy + rozmiar_ss//2], fill=outline_color)
            elif len(loc_pts) > 1:
                if is_closed and fill_color and len(loc_pts) > 2:
                    draw.polygon(loc_pts, fill=fill_color)
                draw.line(loc_pts, fill=outline_color, width=rozmiar_ss, joint="curve")
                
        rendered_box = pusta_ss.resize((box_w, box_h), Image.Resampling.LANCZOS)
        pusta = Image.new("RGBA", self.doc_size, (0, 0, 0, 0))
        pusta.paste(rendered_box, (min_x, min_y))
        w['obraz'] = pusta
        
    def wybierz_kolor_linii(self):
        kolor = colorchooser.askcolor(color=self.color_outline)[1]
        if kolor: 
            self.color_outline = kolor
            self.btn_color_outline.configure(text_color=kolor, border_color=kolor)
            if self.aktywna_warstwa != -1:
                w = self.warstwy[self.aktywna_warstwa]
                if w.get('is_text'):
                    self.zapisz_stan_do_historii()
                    w['text_color'] = self.get_rgba(kolor)
                    self.renderuj_warstwe_tekstu(self.aktywna_warstwa)
                    self.komponuj_i_wyswietl()
                elif w.get('is_object'):
                    self.zapisz_stan_do_historii()
                    w['obj_color'] = self.get_rgba(kolor)
                    self.narysuj_obiekt(w)
                    self.komponuj_i_wyswietl()

    def wybierz_kolor_tla(self):
        init_color = self.color_fill if self.color_fill else "#ffffff"
        kolor = colorchooser.askcolor(color=init_color)[1]
        if kolor:
            self.color_fill = kolor
            self.btn_color_fill.configure(text=self.t["color_fill"], text_color=kolor, border_color=kolor)
            if self.aktywna_warstwa != -1:
                w = self.warstwy[self.aktywna_warstwa]
                if w.get('is_object') and w.get('obj_typ') in ['shape', 'pen']:
                    self.zapisz_stan_do_historii()
                    w['obj_fill_color'] = self.get_rgba(kolor)
                    self.narysuj_obiekt(w)
                    self.komponuj_i_wyswietl()

    def usun_kolor_tla(self):
        self.color_fill = None
        self.btn_color_fill.configure(text=self.t["color_fill"] + f" ({self.t['no_fill']})", text_color="gray50", border_color="gray50")
        if self.aktywna_warstwa != -1:
            w = self.warstwy[self.aktywna_warstwa]
            if w.get('is_object') and w.get('obj_typ') in ['shape', 'pen']:
                self.zapisz_stan_do_historii()
                w['obj_fill_color'] = None
                self.narysuj_obiekt(w)
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
                
    def nowy_obraz(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title(self.t.get("new", "Nowy obraz..."))
        dialog.geometry("320x360")
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()
        
        dialog.update_idletasks()
        x = self.winfo_rootx() + (self.winfo_width() // 2) - (320 // 2)
        y = self.winfo_rooty() + (self.winfo_height() // 2) - (360 // 2)
        dialog.geometry(f"+{x}+{y}")

        wynik = {}

        ctk.CTkLabel(dialog, text=self.t.get("new_w", "Szerokość (px):")).pack(pady=(15, 0))
        entry_w = ctk.CTkEntry(dialog, justify="center")
        entry_w.insert(0, "800")
        entry_w.pack(pady=5)

        ctk.CTkLabel(dialog, text=self.t.get("new_h", "Wysokość (px):")).pack(pady=(10, 0))
        entry_h = ctk.CTkEntry(dialog, justify="center")
        entry_h.insert(0, "600")
        entry_h.pack(pady=5)

        kolor_tla_hex = ["#ffffff"]

        def wybierz_kolor():
            k = colorchooser.askcolor(color=kolor_tla_hex[0])[1]
            if k:
                kolor_tla_hex[0] = k
                btn_color.configure(fg_color=k, text_color="black" if sum(int(k.lstrip('#')[i:i+2], 16) for i in (0,2,4)) > 382 else "white")
                var_trans.set(False)

        def toggle_trans():
            if var_trans.get():
                btn_color.configure(state="disabled")
            else:
                btn_color.configure(state="normal")

        ctk.CTkLabel(dialog, text=self.t.get("bg_color", "Kolor tła:")).pack(pady=(10, 0))
        btn_color = ctk.CTkButton(dialog, text=self.t.get("bg_color", "Kolor tła"), fg_color="#ffffff", text_color="black", hover_color="#dddddd", command=wybierz_kolor)
        btn_color.pack(pady=5)

        var_trans = tk.BooleanVar(value=False)
        chk_trans = ctk.CTkCheckBox(dialog, text=self.t.get("transparent_bg", "Przezroczyste tło"), variable=var_trans, command=toggle_trans)
        chk_trans.pack(pady=10)

        def zamknij_i_zapisz():
            try:
                w_val = int(entry_w.get())
                h_val = int(entry_h.get())
                if w_val <= 0 or h_val <= 0: raise ValueError
                wynik['w'] = w_val
                wynik['h'] = h_val
                if var_trans.get():
                    wynik['bg'] = (0, 0, 0, 0)
                else:
                    k = kolor_tla_hex[0]
                    r, g, b = tuple(int(k.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
                    wynik['bg'] = (r, g, b, 255)
                dialog.destroy()
            except ValueError:
                messagebox.showerror(self.t["msg_err_title"], self.t["err_val"])

        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack(pady=15)
        ctk.CTkButton(btn_frame, text=self.t.get("ok", "OK"), width=100, command=zamknij_i_zapisz).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text=self.t.get("cancel", "Anuluj"), width=100, command=dialog.destroy, fg_color="#555555", hover_color="#333333").pack(side="right", padx=10)

        self.wait_window(dialog)

        if 'w' in wynik:
            self.doc_size = (wynik['w'], wynik['h'])
            self.warstwy = []
            self.historia = []
            if hasattr(self, 'menu_edycja'):
                self.menu_edycja.entryconfig(0, state="disabled")
                
            tlo = Image.new("RGBA", (wynik['w'], wynik['h']), wynik['bg'])
            self.dodaj_warstwe(tlo, self.t.get("bg_layer", "Tło"), 0, 0)
            self.ustaw_aktywna_warstwe(0)
            self.ustaw_narzedzie(None)

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
        nazwa = f"{self.t.get('new_layer', 'Warstwa')} {len(self.warstwy)}"
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
            w = self.warstwy[index]
            self.slider_opacity.set(w['krycie'])
            self.combo_blend.set(w.get('tryb', 'Normal'))
            
            if w.get('is_object') and w.get('obj_size'):
                self.slider_size.set(w['obj_size'])
                if w.get('obj_color'):
                    r, g, b, a = w['obj_color']
                    hex_out = f"#{r:02x}{g:02x}{b:02x}"
                    self.color_outline = hex_out
                    self.btn_color_outline.configure(text_color=hex_out, border_color=hex_out)
                
                if w.get('obj_typ') in ['shape', 'pen']:
                    if w.get('obj_fill_color'):
                        r, g, b, a = w['obj_fill_color']
                        hex_fill = f"#{r:02x}{g:02x}{b:02x}"
                        self.color_fill = hex_fill
                        self.btn_color_fill.configure(text=self.t["color_fill"], text_color=hex_fill, border_color=hex_fill)
                    else:
                        self.color_fill = None
                        self.btn_color_fill.configure(text=self.t["color_fill"] + f" ({self.t['no_fill']})", text_color="gray50", border_color="gray50")

            if w.get('is_text'):
                self.slider_font_size.set(w['text_size'])
                if 'text_font' in w:
                    self.combo_font.set(w['text_font'])
                if w.get('text_color'):
                    r, g, b, a = w['text_color']
                    hex_out = f"#{r:02x}{g:02x}{b:02x}"
                    self.color_outline = hex_out
                    self.btn_color_outline.configure(text_color=hex_out, border_color=hex_out)
                
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

    def rysuj_ramke_zaznaczenia(self):
        self.canvas.delete("sel_element")
        if self.aktywne_narzedzie != 'move' or self.aktywna_warstwa == -1: return
        w = self.warstwy[self.aktywna_warstwa]
        if not w['widoczna']: return
        
        ox, oy = w.get('offset_x', 0), w.get('offset_y', 0)
        
        if w.get('is_object') and w['obj_typ'] == 'shape':
            pts = w['obj_pts']
            if len(pts) == 6:
                x1, y1, x2, y2, cx, cy = pts
                min_x, max_x = min(x1, x2, cx), max(x1, x2, cx)
                min_y, max_y = min(y1, y2, cy), max(y1, y2, cy)
            else:
                x1, y1, x2, y2 = pts
                min_x, max_x = min(x1, x2), max(x1, x2)
                min_y, max_y = min(y1, y2), max(y1, y2)
                
            r = w['obj_size'] / 2
            x1 = min_x + ox - r
            y1 = min_y + oy - r
            x2 = max_x + ox + r
            y2 = max_y + oy + r
            
        elif w.get('is_object') and w['obj_typ'] == 'pen':
            pts = w['obj_pts']
            if not pts: return
            r = w['obj_size'] / 2
            x1 = min(p[0] for p in pts) + ox - r
            y1 = min(p[1] for p in pts) + oy - r
            x2 = max(p[0] for p in pts) + ox + r
            y2 = max(p[1] for p in pts) + oy + r
        elif w.get('is_text'):
            x1, y1 = w['text_x'] + ox, w['text_y'] + oy
            approx_w = len(w['text_content']) * (w['text_size'] * 0.6)
            approx_h = w['text_size'] * 1.2
            x2, y2 = x1 + approx_w, y1 + approx_h
        else:
            bbox = w['obraz'].getbbox()
            if bbox:
                bx1, by1, bx2, by2 = bbox
                x1, y1 = bx1 + ox, by1 + oy
                x2, y2 = bx2 + ox, by2 + oy
            else:
                x1, y1 = ox, oy
                x2, y2 = ox + w['obraz'].width, oy + w['obraz'].height
            
        cx1, cy1 = self.image_to_canvas_coords(min(x1, x2), min(y1, y2))
        cx2, cy2 = self.image_to_canvas_coords(max(x1, x2), max(y1, y2))
        
        self.canvas.create_rectangle(cx1, cy1, cx2, cy2, outline='#00aaff', width=2, dash=(4,4), tags="sel_element")
        
        if (w.get('is_object') and w['obj_typ'] in ['shape', 'pen']) or w.get('is_text'):
            r = 5
            k = '#00aaff'
            handles = [
                (cx1, cy1), (cx2, cy1), (cx1, cy2), (cx2, cy2),
                ((cx1+cx2)/2, cy1), ((cx1+cx2)/2, cy2),
                (cx1, (cy1+cy2)/2), (cx2, (cy1+cy2)/2)
            ]
            for px, py in handles:
                self.canvas.create_oval(px-r, py-r, px+r, py+r, fill='white', outline=k, width=2, tags="sel_element")
                
    def rysuj_wezly_zaznaczenia(self):
        self.canvas.delete("node_element")
        if self.aktywne_narzedzie != 'node' or self.aktywna_warstwa == -1: return
        w = self.warstwy[self.aktywna_warstwa]
        if not w['widoczna'] or not w.get('is_object'): return
        
        ox, oy = w.get('offset_x', 0), w.get('offset_y', 0)
        
        if w['obj_typ'] == 'shape':
            pts = w['obj_pts']
            if w.get('shape_type') in [self.t.get("shape_curve", ""), "Krzywa (Bézier)", "Curve (Bezier)"]:
                x1, y1, x2, y2, cx, cy = pts
                self.canvas.create_line(self.image_to_canvas_coords(x1+ox, y1+oy), self.image_to_canvas_coords(cx+ox, cy+oy), fill="#ff5555", dash=(2,2), tags="node_element")
                self.canvas.create_line(self.image_to_canvas_coords(x2+ox, y2+oy), self.image_to_canvas_coords(cx+ox, cy+oy), fill="#ff5555", dash=(2,2), tags="node_element")
                
                for i in [0, 2, 4]:
                    cx_c, cy_c = self.image_to_canvas_coords(pts[i] + ox, pts[i+1] + oy)
                    kolor = 'yellow' if i == 4 else 'white'
                    self.canvas.create_oval(cx_c-6, cy_c-6, cx_c+6, cy_c+6, fill=kolor, outline='red', width=2, tags="node_element")
            else:
                for i in range(0, len(pts), 2):
                    cx_c, cy_c = self.image_to_canvas_coords(pts[i] + ox, pts[i+1] + oy)
                    self.canvas.create_oval(cx_c-6, cy_c-6, cx_c+6, cy_c+6, fill='white', outline='red', width=2, tags="node_element")
        elif w['obj_typ'] == 'pen':
            for i, (px, py) in enumerate(w['obj_pts']):
                cx, cy = self.image_to_canvas_coords(px + ox, py + oy)
                self.canvas.create_oval(cx-4, cy-4, cx+4, cy+4, fill='white', outline='blue', tags="node_element")

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
    
    def przelacz_siatke(self, event=None):
        self.widoczna_siatka = not getattr(self, 'widoczna_siatka', False)
        self.komponuj_i_wyswietl()

    def rysuj_siatke(self):
        self.canvas.delete("grid_lines")
        if not self.doc_size or not getattr(self, 'widoczna_siatka', False): return
        
        okno_szer = self.canvas.winfo_width()
        okno_wys = self.canvas.winfo_height()
        r_size = 22 
        
        r_x = self.display_width / self.doc_size[0]
        r_y = self.display_height / self.doc_size[1]
        
        step = self.get_grid_step()
        
        s_x = int(-self.canvas_img_x_offset / r_x)
        e_x = int((okno_szer - self.canvas_img_x_offset) / r_x)
        for i in range(s_x - (s_x % step), e_x + step, step):
            cx = int(i * r_x + self.canvas_img_x_offset)
            if cx > r_size:
                self.canvas.create_line(cx, r_size, cx, okno_wys, fill="#666666", dash=(2, 4), tags="grid_lines")
                
        s_y = int(-self.canvas_img_y_offset / r_y)
        e_y = int((okno_wys - self.canvas_img_y_offset) / r_y)
        for i in range(s_y - (s_y % step), e_y + step, step):
            cy = int(i * r_y + self.canvas_img_y_offset)
            if cy > r_size:
                self.canvas.create_line(r_size, cy, okno_szer, cy, fill="#666666", dash=(2, 4), tags="grid_lines")
                
    def rysuj_linijki(self):
        self.canvas.delete("ruler")
        if not self.doc_size: return
        
        okno_szer = self.canvas.winfo_width()
        okno_wys = self.canvas.winfo_height()
        r_size = 22 
        
        self.canvas.create_rectangle(0, 0, okno_szer, r_size, fill="#2a2a2a", outline="", tags="ruler")
        self.canvas.create_rectangle(0, 0, r_size, okno_wys, fill="#2a2a2a", outline="", tags="ruler")
        self.canvas.create_rectangle(0, 0, r_size, r_size, fill="#1a1a1a", outline="", tags="ruler") 
        
        r_x = self.display_width / self.doc_size[0]
        r_y = self.display_height / self.doc_size[1]
        
        step = 100
        if r_x > 3: step = 10
        elif r_x > 1.2: step = 50
        elif r_x < 0.3: step = 500
        minor_step = step // 5
        
        font = ("Arial", 9)
        c_tick = "#aaaaaa"
        
        s_x = int(-self.canvas_img_x_offset / r_x)
        e_x = int((okno_szer - self.canvas_img_x_offset) / r_x)
        for i in range(s_x - (s_x % minor_step), e_x + minor_step, minor_step):
            cx = int(i * r_x + self.canvas_img_x_offset)
            if cx > r_size:
                if i % step == 0:
                    self.canvas.create_line(cx, r_size - 10, cx, r_size, fill=c_tick, tags="ruler")
                    self.canvas.create_text(cx + 3, 2, text=str(i), fill=c_tick, anchor="nw", font=font, tags="ruler")
                else:
                    self.canvas.create_line(cx, r_size - 4, cx, r_size, fill=c_tick, tags="ruler")
                    
        s_y = int(-self.canvas_img_y_offset / r_y)
        e_y = int((okno_wys - self.canvas_img_y_offset) / r_y)
        for i in range(s_y - (s_y % minor_step), e_y + minor_step, minor_step):
            cy = int(i * r_y + self.canvas_img_y_offset)
            if cy > r_size:
                if i % step == 0:
                    self.canvas.create_line(r_size - 10, cy, r_size, cy, fill=c_tick, tags="ruler")
                    self.canvas.create_text(2, cy + 2, text=str(i), fill=c_tick, anchor="nw", font=font, tags="ruler")
                else:
                    self.canvas.create_line(r_size - 4, cy, r_size, cy, fill=c_tick, tags="ruler")
                    
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
        
        self.canvas.create_rectangle(
            self.canvas_img_x_offset, 
            self.canvas_img_y_offset, 
            self.canvas_img_x_offset + self.display_width, 
            self.canvas_img_y_offset + self.display_height, 
            fill="gray35",       
            outline="#8F8F8F",   
            tags="doc_bg"
        )
        
        self.canvas.create_image(self.canvas_img_x_offset, self.canvas_img_y_offset, image=self.tk_obraz, anchor="nw")
        
        if self.aktywne_narzedzie == 'crop':
            self.rysuj_ramke_na_plotnie()
        elif self.aktywne_narzedzie == 'move':
            self.rysuj_ramke_zaznaczenia()
        elif self.aktywne_narzedzie == 'node':
            self.rysuj_wezly_zaznaczenia()
            
        self.rysuj_siatke()
        self.rysuj_linijki()
        
        self.aktualizuj_wymiary_w_polach(w=self.doc_size[0], h=self.doc_size[1])

    def rasteryzuj_warstwe(self, w):
        if w.get('is_text'): w.pop('is_text', None)
        if w.get('is_object'): w.pop('is_object', None)

    def zatwierdz_podglad(self):
        if self.warstwa_podgladowa is not None and self.aktywna_warstwa != -1:
            self.zapisz_stan_do_historii()
            w = self.warstwy[self.aktywna_warstwa]
            
            sc = getattr(self, 'slider_scale', None)
            sc_val = sc.get() if sc else 1.0
            
            b = getattr(self, 'slider_brightness', None)
            b_val = b.get() if b else 1.0
            
            c = getattr(self, 'slider_contrast', None)
            c_val = c.get() if c else 1.0
            
            s = getattr(self, 'slider_saturation', None)
            s_val = s.get() if s else 1.0
            
            sh = getattr(self, 'slider_sharpness', None)
            sh_val = sh.get() if sh else 1.0
            
            exp = getattr(self, 'slider_exposure', None)
            exp_val = exp.get() if exp else 0.0
            
            wb = getattr(self, 'slider_white_balance', None)
            wb_val = wb.get() if wb else 0.0
       
            is_only_scale = (b_val == 1.0 and c_val == 1.0 and s_val == 1.0 and sh_val == 1.0 and exp_val == 0.0 and wb_val == 0.0 and sc_val != 1.0)
            
            if is_only_scale and (w.get('is_object') or w.get('is_text')):
                if w.get('is_text'):
                    w['text_x'] = int(w['text_x'] * sc_val)
                    w['text_y'] = int(w['text_y'] * sc_val)
                    w['text_size'] = max(1, int(w['text_size'] * sc_val))
                    self.renderuj_warstwe_tekstu(self.aktywna_warstwa)
                elif w.get('is_object'):
                    if w['obj_typ'] == 'shape':
                        w['obj_pts'] = [p * sc_val for p in w['obj_pts']]
                        w['obj_size'] = max(1, int(w['obj_size'] * sc_val))
                        self.narysuj_obiekt(w)
                    elif w['obj_typ'] == 'pen':
                        w['obj_pts'] = [(p[0]*sc_val, p[1]*sc_val) for p in w['obj_pts']]
                        w['obj_size'] = max(1, int(w['obj_size'] * sc_val))
                        self.narysuj_obiekt(w)
                self.warstwa_podgladowa = None
            else:
                w['obraz'] = self.warstwa_podgladowa
                self.warstwa_podgladowa = None
                self.rasteryzuj_warstwe(w)
            
            self.blokuj_podglad = True
            if hasattr(self, 'slider_brightness'): self.slider_brightness.set(1.0)
            if hasattr(self, 'slider_contrast'): self.slider_contrast.set(1.0)
            if hasattr(self, 'slider_saturation'): self.slider_saturation.set(1.0)
            if hasattr(self, 'slider_sharpness'): self.slider_sharpness.set(1.0)
            if hasattr(self, 'slider_scale'): self.slider_scale.set(1.0)
            if hasattr(self, 'slider_exposure'): self.slider_exposure.set(0.0)
            if hasattr(self, 'slider_white_balance'): self.slider_white_balance.set(0.0)
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
            if w.get('is_object'):
                kopia['is_object'] = True
                kopia['obj_typ'] = w.get('obj_typ')
                
                if w.get('obj_typ') == 'pen':
                    kopia['obj_pts'] = [(p[0], p[1]) for p in w.get('obj_pts', [])]
                    kopia['is_closed'] = w.get('is_closed', False)
                else:
                    kopia['obj_pts'] = list(w.get('obj_pts'))
                    
                kopia['obj_color'] = w.get('obj_color')
                kopia['obj_fill_color'] = w.get('obj_fill_color')
                kopia['obj_size'] = w.get('obj_size')
                kopia['shape_type'] = w.get('shape_type')
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
        
        e_w = getattr(self, 'slider_exposure', None)
        exp = e_w.get() if e_w else 0.0
        
        wb = getattr(self, 'slider_white_balance', None)
        temp = wb.get() if wb else 0.0
        
        b = self.slider_brightness.get() if hasattr(self, 'slider_brightness') else 1.0
        c = self.slider_contrast.get() if hasattr(self, 'slider_contrast') else 1.0
        s = self.slider_saturation.get() if hasattr(self, 'slider_saturation') else 1.0
        sh = self.slider_sharpness.get() if hasattr(self, 'slider_sharpness') else 1.0
        sc = getattr(self, 'slider_scale', None)
        sc_val = sc.get() if sc else 1.0

        rgb = img.convert("RGB")
        
        if exp != 0.0:
            factor = 2.0 ** exp
            rgb = rgb.point(lambda p: p * factor)
            
        if temp != 0.0:
            r, g, b_chan = rgb.split()
            r = r.point(lambda i: i + temp)
            b_chan = b_chan.point(lambda i: i - temp)
            rgb = Image.merge("RGB", (r, g, b_chan))

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
        if hasattr(self, 'slider_exposure'): self.slider_exposure.set(0.0)
        if hasattr(self, 'slider_white_balance'): self.slider_white_balance.set(0.0)
        self.blokuj_podglad = False
    
    def aktualizuj_wlasciwosci_obiektu(self, _=None):
        if self.aktywna_warstwa != -1:
            w = self.warstwy[self.aktywna_warstwa]
            if w.get('is_object'):
                w['obj_size'] = int(self.slider_size.get())
                w['obj_roundness'] = int(self.slider_roundness.get())
                w['obj_bulge'] = int(self.slider_bulge.get()) / 100.0
                self.narysuj_obiekt(w)
                self.komponuj_i_wyswietl()

    def nałoż_filtr(self, filter_type):
        if self.aktywna_warstwa == -1: return
        w = self.warstwy[self.aktywna_warstwa]
        if not w.get('edycja_maski'): self.rasteryzuj_warstwe(w)
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
        if self.aktywna_warstwa == -1: return
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
            self.rasteryzuj_warstwe(w)
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
        self.rasteryzuj_warstwe(w)
        w['obraz'] = ImageOps.mirror(w['obraz'])
        if w.get('maska') is not None:
            w['maska'] = ImageOps.mirror(w['maska'])
        self.komponuj_i_wyswietl()

    def odbij_w_pionie(self):
        if self.aktywna_warstwa == -1: return
        self.zatwierdz_podglad()
        self.zapisz_stan_do_historii()
        w = self.warstwy[self.aktywna_warstwa]
        self.rasteryzuj_warstwe(w)
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
            self.rasteryzuj_warstwe(w)
            wynik = remove(w['obraz'])
            if wynik.mode != "RGBA": wynik = wynik.convert("RGBA")
            w['obraz'] = wynik
            self.komponuj_i_wyswietl()
        except Exception as e:
            messagebox.showerror(self.t["msg_err_title"], f"Błąd AI: {e}")
        finally:
            self.config(cursor="")

    def wykonaj_kadrowanie(self):
        if not self.warstwy or not self.doc_size: return
        try:
            self.zatwierdz_podglad()
            x = int(self.entry_x.get())
            y = int(self.entry_y.get())
            w = int(self.entry_w.get())
            h = int(self.entry_h.get())
            img_w, img_h = self.doc_size

            if w <= 0 or h <= 0: raise ValueError(self.t["err_dim"])
            x, y = max(0, x), max(0, y)
            w, h = min(w, img_w - x), min(h, img_h - y)
            offset_x_change, offset_y_change = x, y

            self.zapisz_stan_do_historii()
            for warstwa in self.warstwy: 
                warstwa['offset_x'] -= offset_x_change
                warstwa['offset_y'] -= offset_y_change
            self.doc_size = (w, h)
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
        
    def image_to_canvas_coords(self, i_x, i_y):
        if not self.doc_size: return 0, 0
        r_x = self.display_width / self.doc_size[0]
        r_y = self.display_height / self.doc_size[1]
        return int(i_x * r_x + self.canvas_img_x_offset), int(i_y * r_y + self.canvas_img_y_offset)

    def is_point_near_object(self, px, py, w):
        ox = w.get('offset_x', 0)
        oy = w.get('offset_y', 0)
        if w.get('is_object') and w['obj_typ'] == 'shape':
            pts = w['obj_pts']
            if len(pts) == 6:
                x1, y1, x2, y2, cx, cy = pts
                min_x, max_x = min(x1, x2, cx) + ox, max(x1, x2, cx) + ox
                min_y, max_y = min(y1, y2, cy) + oy, max(y1, y2, cy) + oy
            else:
                x1, y1, x2, y2 = pts
                min_x, max_x = min(x1, x2) + ox, max(x1, x2) + ox
                min_y, max_y = min(y1, y2) + oy, max(y1, y2) + oy
            return (min_x - 15) <= px <= (max_x + 15) and (min_y - 15) <= py <= (max_y + 15)
        elif w.get('is_object') and w['obj_typ'] == 'pen':
            pts = w['obj_pts']
            if not pts: return False
            r = max(15, w['obj_size'] / 2)
            min_x = min(p[0] for p in pts) + ox - r
            max_x = max(p[0] for p in pts) + ox + r
            min_y = min(p[1] for p in pts) + oy - r
            max_y = max(p[1] for p in pts) + oy + r
            if not (min_x <= px <= max_x and min_y <= py <= max_y): return False
            
            if len(pts) == 1:
                return self.dystans((px, py), (pts[0][0] + ox, pts[0][1] + oy)) <= r
            for i in range(len(pts)-1):
                x1, y1 = pts[i][0] + ox, pts[i][1] + oy
                x2, y2 = pts[i+1][0] + ox, pts[i+1][1] + oy
                if self.point_to_segment_dist(px, py, x1, y1, x2, y2) <= r:
                    return True
            return False
        elif w.get('is_text'):
            x1, y1 = w['text_x'] + ox, w['text_y'] + oy
            approx_w = len(w['text_content']) * (w['text_size'] * 0.6)
            approx_h = w['text_size'] * 1.2
            return (x1 - 15) <= px <= (x1 + approx_w + 15) and (y1 - 15) <= py <= (y1 + approx_h + 15)
        else:
            bbox = w['obraz'].getbbox()
            if bbox:
                bx1, by1, bx2, by2 = bbox
                x1, y1 = bx1 + ox, by1 + oy
                x2, y2 = bx2 + ox, by2 + oy
            else:
                x1, y1 = ox, oy
                x2, y2 = ox + w['obraz'].width, oy + w['obraz'].height
                
            if x1 <= px <= x2 and y1 <= py <= y2:
                try:
                    pixel = w['obraz'].getpixel((int(px - ox), int(py - oy)))
                    if isinstance(pixel, tuple) and len(pixel) == 4:
                        return pixel[3] > 0
                    return True
                except Exception:
                    return True
            return False

    def zastosuj_rysowanie(self, typ, end_x=None, end_y=None, closed=False):
        self.zatwierdz_podglad()
        w = None
        if self.aktywna_warstwa != -1 and self.warstwy:
            w = self.warstwy[self.aktywna_warstwa]
            
        if typ == 'pen':
            self.zapisz_stan_do_historii()
            rozmiar = int(self.slider_size.get())
            outline_color = self.get_rgba(self.color_outline)
            
            real_pts = list(self.pen_points)
            self.pen_points = []  
            
            is_closed = closed or (len(real_pts)>2 and real_pts[0] == real_pts[-1])
            if is_closed and real_pts[0] != real_pts[-1]:
                real_pts.append(real_pts[0])
                
            fill_color = self.get_rgba(self.color_fill) if is_closed else None
            
            img = Image.new("RGBA", self.doc_size, (0, 0, 0, 0))
            nazwa = self.t["pen"]
            idx = self.aktywna_warstwa + 1 if self.aktywna_warstwa != -1 else 0
            nowa_w = {
                'nazwa': nazwa, 
                'obraz': img,
                'widoczna': True, 
                'krycie': 1.0, 
                'tryb': 'Normal', 
                'maska': None, 
                'edycja_maski': False, 
                'offset_x': 0, 
                'offset_y': 0,
                'is_object': True,
                'obj_typ': 'pen',
                'obj_pts': real_pts,
                'obj_color': outline_color,
                'obj_fill_color': fill_color,
                'obj_size': rozmiar,
                'is_closed': is_closed
            }
            nowa_w['obj_roundness'] = int(self.slider_roundness.get()) if hasattr(self, 'slider_roundness') else 0
            nowa_w['obj_bulge'] = (int(self.slider_bulge.get()) / 100.0) if hasattr(self, 'slider_bulge') else 0.0
            self.narysuj_obiekt(nowa_w)
            self.warstwy.insert(idx, nowa_w)
            self.ustaw_aktywna_warstwe(idx)
            self.ustaw_narzedzie('move')
                
        elif typ == 'shape' and end_x and end_y:
            rx1, ry1 = self.canvas_to_image_coords(self.last_x, self.last_y)
            rx2, ry2 = self.canvas_to_image_coords(end_x, end_y)
            shape_type = self.aktywny_ksztalt
            rozmiar = int(self.slider_size.get())
            outline_color = self.get_rgba(self.color_outline)
            fill_color = self.get_rgba(self.color_fill)
            
            sw = abs(rx2 - rx1)
            sh = abs(ry2 - ry1)
            if sw < 2 and sh < 2: 
                if getattr(self, 'temp_draw_id', None): 
                    self.canvas.delete(self.temp_draw_id)
                    self.temp_draw_id = None
                return

            self.zapisz_stan_do_historii()
            if getattr(self, 'temp_draw_id', None): 
                self.canvas.delete(self.temp_draw_id)
                self.temp_draw_id = None
            
            nazwa = f"K: {shape_type[:5]}"
            idx = self.aktywna_warstwa + 1 if self.aktywna_warstwa != -1 else 0
            if shape_type in [self.t.get("shape_curve", ""), "Krzywa (Bézier)", "Curve (Bezier)"]:
                obj_pts = [rx1, ry1, rx2, ry2, (rx1+rx2)/2, (ry1+ry2)/2]
            else:
                obj_pts = [rx1, ry1, rx2, ry2]
            
            nowa_w = {
                'nazwa': nazwa, 
                'obraz': Image.new("RGBA", self.doc_size, (0, 0, 0, 0)),
                'widoczna': True, 
                'krycie': 1.0, 
                'tryb': 'Normal', 
                'maska': None, 
                'edycja_maski': False, 
                'offset_x': 0, 
                'offset_y': 0,
                'is_object': True,
                'obj_typ': 'shape',
                'shape_type': shape_type,
                'obj_pts': obj_pts,         
                'obj_color': outline_color,
                'obj_fill_color': fill_color,
                'obj_size': rozmiar
            }
           
            self.narysuj_obiekt(nowa_w)
            self.warstwy.insert(idx, nowa_w)
            self.ustaw_aktywna_warstwe(idx)
            self.ustaw_narzedzie('move')
            
        self.komponuj_i_wyswietl()

    def zastosuj_wypelnienie(self, x, y):
        if self.aktywna_warstwa == -1: return
        self.zatwierdz_podglad()
        self.zapisz_stan_do_historii()
        w = self.warstwy[self.aktywna_warstwa]
        
        layer_x = x - w.get('offset_x', 0)
        layer_y = y - w.get('offset_y', 0)
        is_mask = w.get('edycja_maski', False)
        
        if is_mask and w.get('maska') is not None:
            img = w['maska']
            r, g, b, a = self.get_rgba(self.color_outline)
            fill_color = int(r * 0.299 + g * 0.587 + b * 0.114)
            ImageDraw.floodfill(img, (layer_x, layer_y), fill_color)
            self.komponuj_i_wyswietl()
            return

        if w.get('is_text'):
            w['text_color'] = self.get_rgba(self.color_outline)
            self.renderuj_warstwe_tekstu(self.aktywna_warstwa)
            self.komponuj_i_wyswietl()
            return
            
        if w.get('is_object'):
            if w['obj_typ'] == 'pen':
                if w.get('is_closed', False):
                    w['obj_fill_color'] = self.get_rgba(self.color_outline)
                    hex_fill = self.color_outline
                    self.color_fill = hex_fill
                    self.btn_color_fill.configure(text=self.t["color_fill"], text_color=hex_fill, border_color=hex_fill)
                else:
                    w['obj_color'] = self.get_rgba(self.color_outline)
            elif w['obj_typ'] == 'shape':
                w['obj_fill_color'] = self.get_rgba(self.color_outline)
                hex_fill = self.color_outline
                self.color_fill = hex_fill
                self.btn_color_fill.configure(text=self.t["color_fill"], text_color=hex_fill, border_color=hex_fill)
            self.narysuj_obiekt(w)
            self.komponuj_i_wyswietl()
            return
            
        self.rasteryzuj_warstwe(w)
        img = w['obraz']
        fill_color = self.get_rgba(self.color_outline)
        ImageDraw.floodfill(img, (layer_x, layer_y), fill_color)
        self.komponuj_i_wyswietl()

    def zakoncz_narzedzie(self, event=None):
        if self.aktywne_narzedzie == 'pen':
            if event and event.keysym == 'Escape':
                self.pen_points = []
                self.canvas.delete("pen_temp_lines")
                self.canvas.delete("pen_cursor")
                self.komponuj_i_wyswietl()
            elif hasattr(self, 'pen_points') and self.pen_points:
                punkty = list(self.pen_points)
                self.pen_points = []
                self.canvas.delete("pen_temp_lines")
                self.canvas.delete("pen_cursor")
                
                if len(punkty) > 1:
                    self.aktywne_narzedzie = None 
                    self.pen_points = punkty
                    self.zastosuj_rysowanie('pen', closed=False)
                    self.pen_points = []
                self.ustaw_narzedzie('pen')
                
        elif self.aktywne_narzedzie == 'shape' and event and event.keysym == 'Escape':
            if getattr(self, 'temp_draw_id', None):
                self.canvas.delete(self.temp_draw_id)
                self.temp_draw_id = None
                
        elif self.aktywne_narzedzie == 'crop' and event and event.keysym == 'Escape':
            self.ustaw_narzedzie(None)

    def on_canvas_double_click(self, event):
        if not self.doc_size: return
        rx, ry = self.canvas_to_image_coords(event.x, event.y)
        for i in reversed(range(len(self.warstwy))):
            w = self.warstwy[i]
            if w['widoczna'] and w.get('is_object') and w['obj_typ'] in ['shape', 'pen']:
                if self.is_point_near_object(rx, ry, w):
                    self.ustaw_aktywna_warstwe(i)
                    self.ustaw_narzedzie('node')
                    return

    def on_canvas_press(self, event):
        if not self.aktywne_narzedzie or not self.doc_size: return
        self.zatwierdz_podglad()
        x, y = event.x, event.y
        self.last_x, self.last_y = x, y

        if self.aktywne_narzedzie == 'move':
            rx, ry = self.canvas_to_image_coords(x, y)
            w = self.warstwy[self.aktywna_warstwa] if self.aktywna_warstwa != -1 else None
            self.akcja_myszy = None
            
            if w and w['widoczna']:
                ox, oy = w.get('offset_x', 0), w.get('offset_y', 0)
                if (w.get('is_object') and w['obj_typ'] in ['shape', 'pen']) or w.get('is_text'):
                    if w.get('is_text'):
                        x1, y1 = w['text_x'], w['text_y']
                        approx_w = len(w['text_content']) * (w['text_size'] * 0.6)
                        approx_h = w['text_size'] * 1.2
                        x2, y2 = x1 + approx_w, y1 + approx_h
                    elif w.get('is_object') and w['obj_typ'] == 'pen':
                        pts = w['obj_pts']
                        if pts:
                            r_b = w['obj_size'] / 2
                            x1 = min(p[0] for p in pts) - r_b
                            y1 = min(p[1] for p in pts) - r_b
                            x2 = max(p[0] for p in pts) + r_b
                            y2 = max(p[1] for p in pts) + r_b
                        else:
                            x1, y1, x2, y2 = 0, 0, 0, 0
                    else:
                        pts = w['obj_pts']
                        if len(pts) == 6:
                            x1_p, y1_p, x2_p, y2_p, cx_p, cy_p = pts
                            min_x = min(x1_p, x2_p, cx_p)
                            max_x = max(x1_p, x2_p, cx_p)
                            min_y = min(y1_p, y2_p, cy_p)
                            max_y = max(y1_p, y2_p, cy_p)
                            x1, y1, x2, y2 = min_x, min_y, max_x, max_y
                        else:
                            x1, y1, x2, y2 = pts

                    cx1, cy1 = self.image_to_canvas_coords(x1+ox, y1+oy)
                    cx2, cy2 = self.image_to_canvas_coords(x2+ox, y2+oy)
                    
                    t = 12
                    if math.hypot(x - cx1, y - cy1) < t: self.akcja_myszy = 'sel_resize_tl'
                    elif math.hypot(x - cx2, y - cy1) < t: self.akcja_myszy = 'sel_resize_tr'
                    elif math.hypot(x - cx1, y - cy2) < t: self.akcja_myszy = 'sel_resize_bl'
                    elif math.hypot(x - cx2, y - cy2) < t: self.akcja_myszy = 'sel_resize_br'
                    elif math.hypot(x - (cx1+cx2)/2, y - cy1) < t: self.akcja_myszy = 'sel_resize_t'
                    elif math.hypot(x - (cx1+cx2)/2, y - cy2) < t: self.akcja_myszy = 'sel_resize_b'
                    elif math.hypot(x - cx1, y - (cy1+cy2)/2) < t: self.akcja_myszy = 'sel_resize_l'
                    elif math.hypot(x - cx2, y - (cy1+cy2)/2) < t: self.akcja_myszy = 'sel_resize_r'

            if not self.akcja_myszy:
                if w and w['widoczna'] and self.is_point_near_object(rx, ry, w):
                    self.akcja_myszy = 'sel_move'
                else:
                    znaleziono = False
                    for i in reversed(range(len(self.warstwy))):
                        if self.warstwy[i]['widoczna'] and self.is_point_near_object(rx, ry, self.warstwy[i]):
                            self.ustaw_aktywna_warstwe(i)
                            w = self.warstwy[i]
                            self.akcja_myszy = 'sel_move'
                            znaleziono = True
                            break
                    if not znaleziono:
                        self.akcja_myszy = 'sel_move' 
            
            self.zapisz_stan_do_historii()
            self.move_start_x = x
            self.move_start_y = y
            if w and self.akcja_myszy == 'sel_move' and w.get('is_object'):
                self.slider_size.set(w.get('obj_size', 5))
                if hasattr(self, 'slider_roundness'): self.slider_roundness.set(w.get('obj_roundness', 0))
                if hasattr(self, 'slider_bulge'): self.slider_bulge.set(int(w.get('obj_bulge', 0.0) * 100))
            if w:
                self.move_start_offset_x = w.get('offset_x', 0)
                self.move_start_offset_y = w.get('offset_y', 0)
                if w.get('is_text'):
                    self.move_start_obj_pts = (w['text_x'], w['text_y'], w['text_size'])
                elif w.get('is_object'):
                    if w['obj_typ'] == 'shape':
                        self.move_start_obj_pts = list(w['obj_pts'])
                    elif w['obj_typ'] == 'pen':
                        self.move_start_obj_pts = [(p[0], p[1]) for p in w['obj_pts']]
                        if w['obj_pts']:
                            self.move_start_brush_bbox = [
                                min(p[0] for p in w['obj_pts']), min(p[1] for p in w['obj_pts']),
                                max(p[0] for p in w['obj_pts']), max(p[1] for p in w['obj_pts'])
                            ]
                        else:
                            self.move_start_brush_bbox = [0,0,0,0]
                
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
                elif abs(y - ym) < t and xm < x < xx: self.akcja_myszy = 'resize_t'
                elif abs(y - yx) < t and xm < x < xx: self.akcja_myszy = 'resize_b'
                elif abs(x - xm) < t and ym < y < yx: self.akcja_myszy = 'resize_l'
                elif abs(x - xx) < t and ym < y < yx: self.akcja_myszy = 'resize_r'
                elif xm < x < xx and ym < y < yx: self.akcja_myszy = 'move'
                else: 
                    self.akcja_myszy = 'draw'
                    self.rect_coords = [x, y, x, y]
            self.rysuj_ramke_na_plotnie()
            self.odswiez_pola_kadrowania()
            
        elif self.aktywne_narzedzie == 'node':
            if self.aktywna_warstwa == -1: return
            w = self.warstwy[self.aktywna_warstwa]
            if not w.get('is_object'): return
            
            rx, ry = self.canvas_to_image_coords(x, y)
            ox, oy = w.get('offset_x', 0), w.get('offset_y', 0)
            self.akcja_myszy = None
            
            if w['obj_typ'] == 'shape':
                pts = w['obj_pts']
                for i in range(0, len(pts), 2):
                    if math.hypot(rx - (pts[i] + ox), ry - (pts[i+1] + oy)) < 15:
                        self.akcja_myszy = f'node_shape_{i}'
                        self.zapisz_stan_do_historii()
                        break
            elif w['obj_typ'] == 'pen':
                for p_idx, (px, py) in enumerate(w['obj_pts']):
                    if math.hypot(rx - (px + ox), ry - (py + oy)) < 10:
                        self.akcja_myszy = f'node_pen_{p_idx}'
                        self.zapisz_stan_do_historii()
                        break
                    
        elif self.aktywne_narzedzie == 'pen':
            rx, ry = self.canvas_to_image_coords(x, y)
            if not hasattr(self, 'pen_points'): self.pen_points = []
            
            if len(self.pen_points) > 2:
                px, py = self.pen_points[0]
                if self.dystans((rx, ry), (px, py)) < 15:
                    self.pen_points.append((px, py))
                    self.zastosuj_rysowanie('pen', closed=True)
                    self.pen_points = []
                    self.canvas.delete("pen_temp_lines")
                    self.canvas.delete("pen_cursor")
                    self.komponuj_i_wyswietl()
                    return

            rx, ry = self.get_snapped_coords(x, y)
            
            self.pen_points.append((rx, ry))
            if len(self.pen_points) > 1:
                px1, py1 = self.image_to_canvas_coords(*self.pen_points[-2])
                px2, py2 = self.image_to_canvas_coords(*self.pen_points[-1])
                self.canvas.create_line(px1, py1, px2, py2, fill=self.color_outline, width=self.slider_size.get(), tags="pen_temp_lines", capstyle=tk.ROUND, joinstyle=tk.ROUND)
                
        elif self.aktywne_narzedzie == 'fill':
            if self.aktywna_warstwa == -1: return
            rx, ry = self.canvas_to_image_coords(x, y)
            self.zastosuj_wypelnienie(rx, ry)
        elif self.aktywne_narzedzie == 'text': 
            self.wstaw_tekst(x, y)
        elif self.aktywne_narzedzie == 'shape': 
            rx, ry = self.get_snapped_coords(x, y)
            x, y = self.image_to_canvas_coords(rx, ry)
            self.last_x, self.last_y = x, y
                
            shape_type = self.aktywny_ksztalt
            outline_c = self.color_outline
            fill_c = self.color_fill if self.color_fill else ""
            width = int(self.slider_size.get())
            if shape_type in [self.t.get("shape_rect", ""), "Prostokąt", "Rectangle", self.t.get("shape_rounded", ""), "Zaokr. Prostokąt", "Rounded Rect"]:
                self.temp_draw_id = self.canvas.create_rectangle(x,y,x,y, outline=outline_c, fill=fill_c, width=width)
            elif shape_type in [self.t.get("shape_ellipse", ""), "Elipsa", "Ellipse"]:
                self.temp_draw_id = self.canvas.create_oval(x,y,x,y, outline=outline_c, fill=fill_c, width=width)
            elif shape_type in [self.t.get("shape_line", ""), "Linia", "Line", self.t.get("shape_curve", ""), "Krzywa (Bézier)", "Curve (Bezier)"]:
                self.temp_draw_id = self.canvas.create_line(x,y,x,y, fill=outline_c, width=width, capstyle=tk.ROUND)
            elif shape_type in [self.t.get("shape_triangle", ""), "Trójkąt", "Triangle"]:
                self.temp_draw_id = self.canvas.create_polygon(x,y,x,y,x,y, outline=outline_c, fill=fill_c, width=width)
                
    def on_canvas_drag(self, event):
        if not self.aktywne_narzedzie or not self.doc_size: return
        x, y = event.x, event.y
        if self.aktywne_narzedzie == 'move':
            if self.aktywna_warstwa == -1 or not self.akcja_myszy: return
            dx = x - self.move_start_x
            dy = y - self.move_start_y
            rx, ry = self.canvas_to_image_coords(x, y)
            w = self.warstwy[self.aktywna_warstwa]
            ox, oy = w.get('offset_x', 0), w.get('offset_y', 0)
            rel_x, rel_y = rx - ox, ry - oy
            
            if self.akcja_myszy == 'sel_move':
                r_x = self.doc_size[0] / self.display_width
                r_y = self.doc_size[1] / self.display_height
                real_dx = dx * r_x
                real_dy = dy * r_y
                if w.get('is_text'):
                    w['text_x'] = self.move_start_obj_pts[0] + real_dx
                    w['text_y'] = self.move_start_obj_pts[1] + real_dy
                    self.renderuj_warstwe_tekstu(self.aktywna_warstwa)
                elif w.get('is_object') and w.get('obj_typ') == 'shape':
                    w['obj_pts'] = [p + (real_dx if i % 2 == 0 else real_dy) for i, p in enumerate(self.move_start_obj_pts)]
                    self.narysuj_obiekt(w)
                elif w.get('is_object') and w.get('obj_typ') == 'pen':
                    w['obj_pts'] = [(p[0] + real_dx, p[1] + real_dy) for p in self.move_start_obj_pts]
                    self.narysuj_obiekt(w)
                else:
                    w['offset_x'] = self.move_start_offset_x + int(dx * r_x)
                    w['offset_y'] = self.move_start_offset_y + int(dy * r_y)
                self.komponuj_i_wyswietl()
                
            elif self.akcja_myszy.startswith('sel_resize_'):
                direction = self.akcja_myszy.split('_')[-1]
                if w.get('is_object') and w.get('obj_typ') == 'shape':
                    px_list = list(self.move_start_obj_pts)
                    if len(px_list) == 6:
                        bx1, by1 = min(px_list[0], px_list[2], px_list[4]), min(px_list[1], px_list[3], px_list[5])
                        bx2, by2 = max(px_list[0], px_list[2], px_list[4]), max(px_list[1], px_list[3], px_list[5])
                    else:
                        bx1, by1 = min(px_list[0], px_list[2]), min(px_list[1], px_list[3])
                        bx2, by2 = max(px_list[0], px_list[2]), max(px_list[1], px_list[3])

                    nbx1, nby1, nbx2, nby2 = bx1, by1, bx2, by2
                    
                    if 'l' in direction: nbx1 = rel_x
                    if 'r' in direction: nbx2 = rel_x
                    if 't' in direction: nby1 = rel_y
                    if 'b' in direction: nby2 = rel_y
                    
                    old_w = bx2 - bx1
                    old_h = by2 - by1
                    new_w = nbx2 - nbx1
                    new_h = nby2 - nby1
                    
                    if old_w == 0: old_w = 1
                    if old_h == 0: old_h = 1
                    
                    new_pts = []
                    for i in range(0, len(px_list), 2):
                        nx = nbx1 + (px_list[i] - bx1) * (new_w / old_w)
                        ny = nby1 + (px_list[i+1] - by1) * (new_h / old_h)
                        new_pts.extend([nx, ny])
                        
                    w['obj_pts'] = new_pts
                    self.narysuj_obiekt(w)
                    self.komponuj_i_wyswietl()
                    
                elif w.get('is_object') and w.get('obj_typ') == 'pen':
                    bx1, by1, bx2, by2 = self.move_start_brush_bbox
                    nbx1, nby1, nbx2, nby2 = bx1, by1, bx2, by2
                    
                    if 'l' in direction: nbx1 = rel_x
                    if 'r' in direction: nbx2 = rel_x
                    if 't' in direction: nby1 = rel_y
                    if 'b' in direction: nby2 = rel_y
                    
                    old_w = bx2 - bx1
                    old_h = by2 - by1
                    new_w = nbx2 - nbx1
                    new_h = nby2 - nby1
                    
                    if old_w == 0: old_w = 1
                    if old_h == 0: old_h = 1
                    
                    new_pts = []
                    for px, py in self.move_start_obj_pts:
                        nx = nbx1 + (px - bx1) * (new_w / old_w)
                        ny = nby1 + (py - by1) * (new_h / old_h)
                        new_pts.append((nx, ny))
                    w['obj_pts'] = new_pts
                    self.narysuj_obiekt(w)
                    self.komponuj_i_wyswietl()
                    
                elif w.get('is_text'):
                    r_y = self.doc_size[1] / self.display_height
                    real_dy = dy * r_y
                    new_size = int(self.move_start_obj_pts[2] + (real_dy if 'b' in direction else -real_dy))
                    w['text_size'] = max(10, new_size)
                    self.slider_font_size.set(w['text_size'])
                    self.renderuj_warstwe_tekstu(self.aktywna_warstwa)
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
            elif self.akcja_myszy == 'resize_t':
                self.rect_coords[1] = y
            elif self.akcja_myszy == 'resize_b':
                self.rect_coords[3] = y
            elif self.akcja_myszy == 'resize_l':
                self.rect_coords[0] = x
            elif self.akcja_myszy == 'resize_r':
                self.rect_coords[2] = x
            
            self.last_x, self.last_y = x, y
            self.rysuj_ramke_na_plotnie()
            self.odswiez_pola_kadrowania()
            
        elif self.aktywne_narzedzie == 'node' and self.akcja_myszy:
            rx, ry = self.get_snapped_coords(x, y)
            w = self.warstwy[self.aktywna_warstwa]
            ox, oy = w.get('offset_x', 0), w.get('offset_y', 0)
            rel_x, rel_y = rx - ox, ry - oy
            
            if self.akcja_myszy.startswith('node_shape_'):
                idx = int(self.akcja_myszy.split('_')[-1])
                w['obj_pts'][idx] = rel_x
                w['obj_pts'][idx+1] = rel_y
                self.narysuj_obiekt(w)
                self.komponuj_i_wyswietl()
            elif self.akcja_myszy.startswith('node_pen_'):
                p_idx = int(self.akcja_myszy.split('_')[2])
                w['obj_pts'][p_idx] = (rel_x, rel_y)
                self.narysuj_obiekt(w)
                self.komponuj_i_wyswietl()
            
        elif self.aktywne_narzedzie == 'shape' and getattr(self, 'temp_draw_id', None):
            rx, ry = self.get_snapped_coords(x, y)
            x, y = self.image_to_canvas_coords(rx, ry)
                
            shape_type = self.aktywny_ksztalt
            if shape_type in [self.t.get("shape_triangle", ""), "Trójkąt", "Triangle"]:
                self.canvas.coords(self.temp_draw_id, self.last_x, y, (self.last_x + x)/2, self.last_y, x, y)
            else:
                self.canvas.coords(self.temp_draw_id, self.last_x, self.last_y, x, y)

    def on_canvas_release(self, event):
        if not self.aktywne_narzedzie or not self.doc_size: return
        if self.aktywne_narzedzie == 'shape': 
            rx, ry = self.get_snapped_coords(event.x, event.y)
            x, y = self.image_to_canvas_coords(rx, ry)
            self.zastosuj_rysowanie('shape', x, y)

    def rysuj_ramke_na_plotnie(self):
        self.canvas.delete("crop_element")
        if not self.rect_coords: return
        x1, y1, x2, y2 = self.rect_coords
        xm, xx = min(x1, x2), max(x1, x2)
        ym, yx = min(y1, y2), max(y1, y2)

        w = xx - xm
        h = yx - ym

        self.canvas.create_rectangle(xm-1, ym-1, xx+1, yx+1, outline='black', width=1, tags="crop_element")
        self.canvas.create_rectangle(xm, ym, xx, yx, outline='white', width=1, tags="crop_element")
        
        if w > 30 and h > 30:
            for i in [1, 2]:
                vx = xm + (w * i / 3)
                self.canvas.create_line(vx, ym, vx, yx, fill='white', width=1, dash=(4, 4), tags="crop_element")
                hy = ym + (h * i / 3)
                self.canvas.create_line(xm, hy, xx, hy, fill='white', width=1, dash=(4, 4), tags="crop_element")

        l = 20
        c = 'white'
        tw = 3
        self.canvas.create_line(xm, ym+l, xm, ym, xm+l, ym, fill=c, width=tw, tags="crop_element")
        self.canvas.create_line(xx-l, ym, xx, ym, xx, ym+l, fill=c, width=tw, tags="crop_element")
        self.canvas.create_line(xm, yx-l, xm, yx, xm+l, yx, fill=c, width=tw, tags="crop_element")
        self.canvas.create_line(xx-l, yx, xx, yx, xx, yx-l, fill=c, width=tw, tags="crop_element")
        mid_x, mid_y = xm + w/2, ym + h/2
        self.canvas.create_line(mid_x-l/2, ym, mid_x+l/2, ym, fill=c, width=tw, tags="crop_element") 
        self.canvas.create_line(mid_x-l/2, yx, mid_x+l/2, yx, fill=c, width=tw, tags="crop_element") 
        self.canvas.create_line(xm, mid_y-l/2, xm, mid_y+l/2, fill=c, width=tw, tags="crop_element") 
        self.canvas.create_line(xx, mid_y-l/2, xx, mid_y+l/2, fill=c, width=tw, tags="crop_element") 

    def ustaw_narzedzie(self, narzedzie):
        if not self.warstwy and narzedzie not in [None, 'crop']: return
        self.zatwierdz_podglad()
        
        poprzednie_narzedzie = self.aktywne_narzedzie
        self.aktywne_narzedzie = None 
        
        if poprzednie_narzedzie == 'pen' and hasattr(self, 'pen_points') and len(self.pen_points) > 1:
            self.zastosuj_rysowanie('pen')
            
        self.pen_points = []
        
        self.canvas.delete("crop_element"); self.rect_coords = None; self.canvas.config(cursor="")
        self.canvas.delete("sel_element")
        self.canvas.delete("node_element")
        self.canvas.delete("pen_temp_lines")
        self.canvas.delete("pen_cursor")
        
        if poprzednie_narzedzie == narzedzie:
            self.aktywne_narzedzie = None
            nazwa = self.t["none"]
            if self.doc_size: self.aktualizuj_wymiary_w_polach(0, 0, self.doc_size[0], self.doc_size[1])
        else:
            self.aktywne_narzedzie = narzedzie
            if narzedzie == 'crop': 
                self.canvas.config(cursor="cross")
                nazwa = self.t["crop_on"]
                if self.doc_size and hasattr(self, 'display_width'):
                    self.rect_coords = [self.canvas_img_x_offset, self.canvas_img_y_offset, self.canvas_img_x_offset + self.display_width, self.canvas_img_y_offset + self.display_height]
                    self.rysuj_ramke_na_plotnie()
                    self.odswiez_pola_kadrowania()
            elif narzedzie == 'pen': 
                self.canvas.config(cursor="crosshair")
                nazwa = f"{self.t['pen']} (Prawy Klik -> Koniec)" if self.lang == "pl" else f"{self.t['pen']} (Right Click -> Finish)"
            elif narzedzie == 'fill': self.canvas.config(cursor="tcross"); nazwa = self.t["fill"]
            elif narzedzie == 'text': self.canvas.config(cursor="xterm"); nazwa = self.t["text"]
            elif narzedzie == 'shape': self.canvas.config(cursor="crosshair"); nazwa = self.aktywny_ksztalt
            elif narzedzie == 'move': 
                self.canvas.config(cursor="fleur")
                nazwa = self.t["move"]
                self.komponuj_i_wyswietl()
            elif narzedzie == 'node':
                self.canvas.config(cursor="crosshair")
                nazwa = self.t.get("node", "Edycja węzłów")
                self.komponuj_i_wyswietl()
            else: nazwa = self.t["none"]
            
        self.lbl_aktywne_narz.configure(text=f"{self.t['active_tool']} {nazwa}")
        if self.aktywne_narzedzie == 'crop': self.btn_crop.configure(text=self.t["crop_off"], border_width=2)
        else: self.btn_crop.configure(text=self.t["crop_on"], border_width=1)

    def przy_zmianie_rozmiaru(self, event):
        self.canvas.coords("help_text", event.width / 2, event.height / 2)
        if self.warstwy:
            if self.resize_timer: self.after_cancel(self.resize_timer)
            self.resize_timer = self.after(150, lambda: self.ustaw_narzedzie('crop') if self.aktywne_narzedzie == 'crop' else self.komponuj_i_wyswietl())

    def eksportuj_do_svg(self, event=None):
        self.zatwierdz_podglad()
        if not self.warstwy: return
        
        sciezka = filedialog.asksaveasfilename(defaultextension=".svg", filetypes=[("Plik SVG", "*.svg")])
        if not sciezka: return
        
        w_doc, h_doc = self.doc_size
        svg_kod = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w_doc}" height="{h_doc}" viewBox="0 0 {w_doc} {h_doc}">']
        
        for w in reversed(self.warstwy):
            if not w['widoczna']: continue
            ox, oy = w.get('offset_x', 0), w.get('offset_y', 0)
            krycie = w.get('krycie', 1.0)
            
            if w.get('is_text'):
                x, y = w['text_x'] + ox, w['text_y'] + oy
                r, g, b, a = w['text_color']
                kolor = f"rgb({r},{g},{b})"
                rozmiar = w['text_size']
                tresc = w['text_content'].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                czcionka = w.get('text_font', 'Arial')
                y_baseline = y + rozmiar * 0.8
                svg_kod.append(f'  <text x="{x}" y="{y_baseline}" font-family="{czcionka}" font-size="{rozmiar}" fill="{kolor}" opacity="{krycie}">{tresc}</text>')
                
            elif w.get('is_object'):
                r, g, b, a = w['obj_color']
                stroke = f"rgb({r},{g},{b})"
                stroke_w = w['obj_size']
                fill = "none"
                if w.get('obj_fill_color'):
                    fr, fg, fb, fa = w['obj_fill_color']
                    fill = f"rgb({fr},{fg},{fb})"
                
                typ = w.get('obj_typ')
                if typ == 'shape':
                    pts = w['obj_pts']
                    if len(pts) == 6:
                        x1, y1, x2, y2, cx, cy = pts
                        min_x, max_x = min(x1, x2, cx) + ox, max(x1, x2, cx) + ox
                        min_y, max_y = min(y1, y2, cy) + oy, max(y1, y2, cy) + oy
                    else:
                        x1, y1, x2, y2 = pts
                        x1, x2 = x1 + ox, x2 + ox
                        y1, y2 = y1 + oy, y2 + oy
                        min_x, max_x = min(x1, x2), max(x1, x2)
                        min_y, max_y = min(y1, y2), max(y1, y2)
                    
                    sw, sh = max_x - min_x, max_y - min_y
                    
                    stype = w.get('shape_type')
                    d_path = ""
                    
                    if stype in [self.t.get("shape_rect", ""), "Prostokąt", "Rectangle"]:
                        d_path = f"M {min_x} {min_y} L {max_x} {min_y} L {max_x} {max_y} L {min_x} {max_y} Z"
                    elif stype in [self.t.get("shape_ellipse", ""), "Elipsa", "Ellipse"]:
                        cx_e, cy_e = min_x + sw/2, min_y + sh/2
                        rx_e, ry_e = sw/2, sh/2
                        d_path = f"M {cx_e-rx_e} {cy_e} A {rx_e} {ry_e} 0 1 0 {cx_e+rx_e} {cy_e} A {rx_e} {ry_e} 0 1 0 {cx_e-rx_e} {cy_e} Z"
                    elif stype in [self.t.get("shape_line", ""), "Linia", "Line"]:
                        d_path = f"M {x1} {y1} L {x2} {y2}"
                    elif stype in [self.t.get("shape_triangle", ""), "Trójkąt", "Triangle"]:
                        d_path = f"M {min_x} {max_y} L {min_x+sw/2} {min_y} L {max_x} {max_y} Z"
                    elif stype in [self.t.get("shape_rounded", ""), "Zaokr. Prostokąt", "Rounded Rect"]:
                        rad = max(1, min(sw, sh) // 5)
                        d_path = (f"M {min_x+rad} {min_y} L {max_x-rad} {min_y} "
                                  f"A {rad} {rad} 0 0 1 {max_x} {min_y+rad} L {max_x} {max_y-rad} "
                                  f"A {rad} {rad} 0 0 1 {max_x-rad} {max_y} L {min_x+rad} {max_y} "
                                  f"A {rad} {rad} 0 0 1 {min_x} {max_y-rad} L {min_x} {min_y+rad} "
                                  f"A {rad} {rad} 0 0 1 {min_x+rad} {min_y} Z")
                    elif stype in [self.t.get("shape_curve", ""), "Krzywa (Bézier)", "Curve (Bezier)"]:
                        cx, cy = pts[4] + ox, pts[5] + oy
                        d_path = f"M {x1} {y1} Q {cx} {cy} {x2} {y2}"

                    if d_path:
                        svg_kod.append(f'  <path d="{d_path}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_w}" opacity="{krycie}" stroke-linejoin="round" stroke-linecap="round"/>')
                        
                elif typ == 'pen':
                    if len(w['obj_pts']) > 1:
                        d_path = f"M {w['obj_pts'][0][0]+ox} {w['obj_pts'][0][1]+oy} "
                        d_path += " ".join([f"L {p[0]+ox} {p[1]+oy}" for p in w['obj_pts'][1:]])
                        
                        is_closed = w.get('is_closed', False)
                        if is_closed:
                            d_path += " Z"
                            
                        p_fill = fill if is_closed and w.get('obj_fill_color') else "none"
                        
                        svg_kod.append(f'  <path d="{d_path}" fill="{p_fill}" stroke="{stroke}" stroke-width="{stroke_w}" opacity="{krycie}" stroke-linejoin="round" stroke-linecap="round"/>')
            else:
                img = w['obraz'].copy()
                if krycie < 1.0:
                    alpha = img.split()[3].point(lambda p: int(p * krycie))
                    img.putalpha(alpha)
                bufor = BytesIO()
                img.save(bufor, format="PNG")
                b64 = base64.b64encode(bufor.getvalue()).decode('utf-8')
                svg_kod.append(f'  <image x="{ox}" y="{oy}" width="{img.width}" height="{img.height}" href="data:image/png;base64,{b64}"/>')
                
        svg_kod.append('</svg>')
        
        with open(sciezka, "w", encoding="utf-8") as f:
            f.write("\n".join(svg_kod))
            
        messagebox.showinfo(self.t["msg_saved_title"], "Wyeksportowano grafikę wektorową jako w pełni edytowalne Krzywe!")

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