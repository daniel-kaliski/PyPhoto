#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ==============================================================================
# Nazwa pliku: PyGraph.py
# 
# Copyright (c) 2026 Daniel Kaliski
# Ten kod jest objęty licencją GNU GENERAL PUBLIC LICENSE GPL-3.0.
# Pełny tekst licencji znajduje się w pliku LICENSE lub na stronie:
# https://opensource.org/license/gpl-3.0
# ==============================================================================

import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser, simpledialog
from PIL import Image, ImageTk, ImageOps, ImageFilter, ImageEnhance, ImageDraw, ImageFont
from rembg import remove
import locale
import sys
import os
import ctypes

def wykryj_jezyk_systemu():
    try:
        if sys.platform == 'win32' and ctypes.windll.kernel32.GetUserDefaultUILanguage() == 1045: 
            return "pl"
        j, _ = locale.getlocale()
        if j and 'pl' in j.lower(): 
            return "pl"
    except: 
        pass
    return "pl"

TEXTS = {
    "pl": {
        "title": "PyGraph - Edytor z Warstwami",
        "tools": "Narzędzia",
        "open": "⇧ Otwórz",
        "undo": "⟲ Cofnij (Undo)",
        "transform": "Transformacje:",
        "rotate": "⟳ Obróć o 90°",
        "adjust": "Dopasowanie warstwy:",
        "brightness": "Jasność",
        "contrast": "Kontrast",
        "saturation": "Nasycenie",
        "sharpness": "Ostrość",
        "scale": "Skala warstwy",
        "apply_adj": "✓ Zastosuj dopasowanie",
        "interactive": "Narzędzia interaktywne:",
        "move": "⬀ Przesuń",
        "brush": "✎ Pędzel",
        "text": "T Tekst",
        "rectangle": "▭ Prostokąt",
        "color": "■ Kolor",
        "size": "Grubość pędzla",
        "font_size": "Wielkość tekstu",
        "effects": "Filtry (na warstwie):",
        "bw": "Czarno-biały",
        "blur": "Rozmycie",
        "sharpen": "Wyostrz",
        "invert": "Negatyw",
        "emboss": "Płaskorzeźba",
        "edges": "Krawędzie",
        "apply_filter": "✓ Zastosuj filtr",
        "remove_bg": "✂ Usuń tło (AI)",
        "crop": "Kadrowanie (Cały obszar):",
        "crop_on": "◩ Aktywuj ramkę",
        "crop_off": "◪ Wyłącz ramkę",
        "crop_apply": "✓ Zastosuj cięcie",
        "save": "⭳ Eksportuj obraz",
        "layers": "WARSTWY",
        "layer_add": "＋ Nowa",
        "layer_insert": "⍐ Wstaw",
        "layer_del": "✖ Usuń",
        "rename_title": "Zmiana nazwy",
        "rename_prompt": "Podaj nową nazwę warstwy:",
        "opacity": "Krycie warstwy:",
        "bg_layer": "Tło",
        "new_layer": "Warstwa",
        "help": "Wczytaj obrazek, by rozpocząć projekt",
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
        "title": "PyGraph - Layered Editor",
        "tools": "Tools",
        "open": "⇧ Open",
        "undo": "⟲ Undo",
        "transform": "Transformations:",
        "rotate": "⟳ Rotate 90°",
        "adjust": "Layer Adjustments:",
        "brightness": "Brightness",
        "contrast": "Contrast",
        "saturation": "Saturation",
        "sharpness": "Sharpness",
        "scale": "Layer Scale",
        "apply_adj": "✓ Apply Adjustments",
        "interactive": "Interactive Tools:",
        "move": "⬀ Move",
        "brush": "✎ Brush",
        "text": "T Text",
        "rectangle": "▭ Rect",
        "color": "■ Color",
        "size": "Brush Size",
        "font_size": "Font Size",
        "effects": "Filters (Active Layer):",
        "bw": "Black & White",
        "blur": "Blur",
        "sharpen": "Sharpen",
        "invert": "Invert",
        "emboss": "Emboss",
        "edges": "Find Edges",
        "apply_filter": "✓ Apply Filter",
        "remove_bg": "✂ Remove BG (AI)",
        "crop": "Cropping (Canvas):",
        "crop_on": "◩ Activate Frame",
        "crop_off": "◪ Deactivate Frame",
        "crop_apply": "✓ Apply Crop",
        "save": "⭳ Export Image",
        "layers": "LAYERS",
        "layer_add": "＋ Add",
        "layer_insert": "⍐ Insert",
        "layer_del": "✖ Delete",
        "rename_title": "Rename",
        "rename_prompt": "Enter new layer name:",
        "opacity": "Layer Opacity:",
        "bg_layer": "Background",
        "new_layer": "Layer",
        "help": "Load an image to start the project",
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

class PyGraph(ctk.CTk):
    
    def __init__(self):
        super().__init__()
        
        self.lang = wykryj_jezyk_systemu()
        self.t = TEXTS[self.lang]

        self.title(self.t["title"])
        
        try:
            with open("pygraph_cfg.txt", "r") as f:
                self.geometry(f.read().strip())
        except:
            self.geometry("1400x900")
            
        self.minsize(1000, 650)
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

        self.klucze_filtrow = ["bw", "blur", "sharpen", "invert", "emboss", "edges"]

        self.grid_columnconfigure(0, minsize=350, weight=0)
        self.grid_columnconfigure(1, weight=1) 
        self.grid_columnconfigure(2, minsize=260, weight=0)
        self.grid_rowconfigure(0, weight=1)
        
        self.panel_lewy = ctk.CTkFrame(self, corner_radius=0, width=350)
        self.panel_lewy.grid(row=0, column=0, sticky="nsew")
        self.panel_lewy.grid_propagate(False)

        self.btn_lang = ctk.CTkButton(self.panel_lewy, text="PL" if self.lang == "pl" else "EN", width=60, height=28, corner_radius=6, command=self.przelacz_jezyk, fg_color="transparent", border_width=1, border_color="white", text_color="white", hover_color="#333")
        self.btn_lang.pack(anchor="nw", padx=10, pady=10)

        self.panel_narzedzi = ctk.CTkScrollableFrame(self.panel_lewy, fg_color="transparent")
        self.panel_narzedzi.pack(side="top", fill="both", expand=True)

        self.lbl_narzedzia = ctk.CTkLabel(self.panel_narzedzi, text=self.t["tools"], font=ctk.CTkFont(size=20, weight="bold"))
        self.lbl_narzedzia.pack(pady=(0, 10))

        self.btn_otworz = ctk.CTkButton(self.panel_narzedzi, text=self.t["open"], height=32, corner_radius=6, command=self.otworz_obraz, fg_color="transparent", border_width=1, border_color="white", text_color="white", hover_color="#333")
        self.btn_otworz.pack(pady=5, padx=20, fill="x")
        
        self.btn_cofnij = ctk.CTkButton(self.panel_narzedzi, text=self.t["undo"], height=32, corner_radius=6, fg_color="transparent", border_width=1, border_color="white", text_color="gray50", state="disabled", command=self.cofnij, hover_color="#333")
        self.btn_cofnij.pack(pady=5, padx=20, fill="x")

        self.lbl_transform = ctk.CTkLabel(self.panel_narzedzi, text=self.t["transform"], font=ctk.CTkFont(weight="bold"))
        self.lbl_transform.pack(pady=(15, 0))
        
        self.btn_obroc = ctk.CTkButton(self.panel_narzedzi, text=self.t["rotate"], height=32, corner_radius=6, command=self.obroc_obraz, fg_color="transparent", border_width=1, border_color="white", text_color="white", hover_color="#333")
        self.btn_obroc.pack(pady=5, padx=20, fill="x")

        self.lbl_interactive = ctk.CTkLabel(self.panel_narzedzi, text=self.t["interactive"], font=ctk.CTkFont(weight="bold"))
        self.lbl_interactive.pack(pady=(20, 5))

        ramka_narzedzi = ctk.CTkFrame(self.panel_narzedzi, fg_color="transparent")
        ramka_narzedzi.pack(pady=5, padx=15, fill="x")
        ramka_narzedzi.grid_columnconfigure(0, weight=1)
        ramka_narzedzi.grid_columnconfigure(1, weight=1)
        
        self.btn_move = self.stworz_przycisk_narzedzia(ramka_narzedzi, self.t["move"], 'move')
        self.btn_move.grid(row=0, column=0, padx=2, pady=2, sticky="ew")
        
        self.btn_brush = self.stworz_przycisk_narzedzia(ramka_narzedzi, self.t["brush"], 'brush')
        self.btn_brush.grid(row=0, column=1, padx=2, pady=2, sticky="ew")
        
        self.btn_text = self.stworz_przycisk_narzedzia(ramka_narzedzi, self.t["text"], 'text')
        self.btn_text.grid(row=1, column=0, padx=2, pady=2, sticky="ew")
        
        self.btn_rect = self.stworz_przycisk_narzedzia(ramka_narzedzi, self.t["rectangle"], 'rect')
        self.btn_rect.grid(row=1, column=1, padx=2, pady=2, sticky="ew")

        ramka_opcji = ctk.CTkFrame(self.panel_narzedzi, fg_color="transparent")
        ramka_opcji.pack(pady=10, padx=20, fill="x")
        
        self.btn_color = ctk.CTkButton(ramka_opcji, text=self.t["color"], height=30, corner_radius=6, command=self.wybierz_kolor, fg_color="transparent", border_width=1, border_color="white", text_color=self.current_color, hover_color="#333")
        self.btn_color.pack(side="top", fill="x", pady=(0, 10))
        
        ramka_grubosc = ctk.CTkFrame(ramka_opcji, fg_color="transparent")
        ramka_grubosc.pack(fill="x", pady=2)
        self.lbl_size = ctk.CTkLabel(ramka_grubosc, text=self.t["size"], width=100, anchor="w")
        self.lbl_size.pack(side="left", padx=(0, 5))
        self.slider_size = ctk.CTkSlider(ramka_grubosc, from_=1, to=100, button_color="#888", button_hover_color="#bbb")
        self.slider_size.set(5)
        self.slider_size.pack(side="right", expand=True, fill="x")

        ramka_czcionka = ctk.CTkFrame(ramka_opcji, fg_color="transparent")
        ramka_czcionka.pack(fill="x", pady=2)
        self.lbl_font_size = ctk.CTkLabel(ramka_czcionka, text=self.t["font_size"], width=100, anchor="w")
        self.lbl_font_size.pack(side="left", padx=(0, 5))
        self.slider_font_size = ctk.CTkSlider(ramka_czcionka, from_=10, to=300, button_color="#888", button_hover_color="#bbb")
        self.slider_font_size.set(40)
        self.slider_font_size.pack(side="right", expand=True, fill="x")

        self.lbl_adjust = ctk.CTkLabel(self.panel_narzedzi, text=self.t["adjust"], font=ctk.CTkFont(weight="bold"))
        self.lbl_adjust.pack(pady=(20, 0))

        for nazwa, attr in [("brightness", "slider_brightness"), ("contrast", "slider_contrast"), ("saturation", "slider_saturation"), ("sharpness", "slider_sharpness"), ("scale", "slider_scale")]:
            lbl = ctk.CTkLabel(self.panel_narzedzi, text=self.t[nazwa])
            lbl.pack(pady=(5, 0))
            if nazwa in ["brightness", "contrast"]:
                suwak = ctk.CTkSlider(self.panel_narzedzi, from_=0.1, to=2.0, command=self.podglad_suwakow)
            elif nazwa == "scale":
                suwak = ctk.CTkSlider(self.panel_narzedzi, from_=0.1, to=3.0, command=self.podglad_suwakow)
            else:
                suwak = ctk.CTkSlider(self.panel_narzedzi, from_=0.0, to=3.0, command=self.podglad_suwakow)
            suwak.set(1.0)
            suwak.pack(pady=0, padx=20)
            setattr(self, attr, suwak)
            setattr(self, f"lbl_{nazwa}", lbl)

        self.btn_apply_adj = ctk.CTkButton(self.panel_narzedzi, text=self.t["apply_adj"], height=32, corner_radius=6, command=self.zastosuj_suwaki, fg_color="transparent", border_width=1, border_color="white", text_color="white", hover_color="#333")
        self.btn_apply_adj.pack(pady=(15, 0), padx=20, fill="x")

        self.lbl_efekty = ctk.CTkLabel(self.panel_narzedzi, text=self.t["effects"], font=ctk.CTkFont(weight="bold"))
        self.lbl_efekty.pack(pady=(20, 5))
        
        self.combo_filtry = ctk.CTkComboBox(self.panel_narzedzi, values=[self.t[k] for k in self.klucze_filtrow], state="readonly", corner_radius=6, fg_color="#242424", border_color="white", text_color="white")
        self.combo_filtry.pack(pady=(5,10), padx=20, fill="x")
        self.combo_filtry.set(self.t["bw"])
        
        self.btn_zastosuj_filtr = ctk.CTkButton(self.panel_narzedzi, text=self.t["apply_filter"], height=32, corner_radius=6, command=self.zastosuj_wybrany_filtr, fg_color="transparent", border_width=1, border_color="white", text_color="white", hover_color="#333")
        self.btn_zastosuj_filtr.pack(pady=(0, 10), padx=20, fill="x")

        self.btn_rembg = ctk.CTkButton(self.panel_narzedzi, text=self.t["remove_bg"], height=32, corner_radius=6, command=self.usun_tlo, fg_color="transparent", border_width=1, border_color="white", text_color="white", hover_color="#333")
        self.btn_rembg.pack(pady=(10, 5), padx=20, fill="x")

        self.lbl_kadrowanie = ctk.CTkLabel(self.panel_narzedzi, text=self.t["crop"], font=ctk.CTkFont(weight="bold"))
        self.lbl_kadrowanie.pack(pady=(15, 0))
        
        self.btn_crop = self.stworz_przycisk_narzedzia(self.panel_narzedzi, self.t["crop_on"], 'crop')
        self.btn_crop.pack(pady=(5,5), padx=20, fill="x")
        
        self.ramka_px = ctk.CTkFrame(self.panel_narzedzi, fg_color="transparent")
        self.ramka_px.pack(pady=5, padx=15, fill="x")
        self.ramka_px.grid_columnconfigure(0, weight=1)
        self.ramka_px.grid_columnconfigure(1, weight=1)
        
        self.entry_x, self.lbl_x = self.stworz_pole_px(self.ramka_px, "X:", 0, 0)
        self.entry_y, self.lbl_y = self.stworz_pole_px(self.ramka_px, "Y:", 0, 1)
        self.entry_w, self.lbl_w = self.stworz_pole_px(self.ramka_px, self.t["width"], 1, 0)
        self.entry_h, self.lbl_h = self.stworz_pole_px(self.ramka_px, self.t["height"], 1, 1)
        
        self.btn_dokladne_crop = ctk.CTkButton(self.panel_narzedzi, text=self.t["crop_apply"], height=32, corner_radius=6, command=self.zastosuj_ciecie_z_pol, fg_color="transparent", border_width=1, border_color="white", text_color="white", hover_color="#333")
        self.btn_dokladne_crop.pack(pady=5, padx=20, fill="x")

        self.panel_obrazu = ctk.CTkFrame(self)
        self.panel_obrazu.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.canvas = tk.Canvas(self.panel_obrazu, bg="gray25", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.text_label = ctk.CTkLabel(self.panel_obrazu, text=self.t["help"], font=("Arial", 16), text_color="gray70")
        self.canvas.create_window(0, 0, window=self.text_label, anchor="center", tags="help_text")

        self.canvas.bind("<Configure>", self.przy_zmianie_rozmiaru)
        self.canvas.bind("<ButtonPress-1>", self.on_canvas_press)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_canvas_release)

        self.panel_prawy = ctk.CTkFrame(self, corner_radius=0, width=260)
        self.panel_prawy.grid(row=0, column=2, sticky="nsew")
        self.panel_prawy.grid_propagate(False)

        self.lbl_layers_title = ctk.CTkLabel(self.panel_prawy, text=self.t["layers"], font=ctk.CTkFont(size=18, weight="bold"))
        self.lbl_layers_title.pack(pady=(20, 10))

        ramka_kontrolek_warstw = ctk.CTkFrame(self.panel_prawy, fg_color="transparent")
        ramka_kontrolek_warstw.pack(fill="x", padx=10, pady=5)
        
        self.btn_add_layer = ctk.CTkButton(ramka_kontrolek_warstw, text=self.t["layer_add"], width=65, height=28, corner_radius=6, command=self.dodaj_pusta_warstwe, fg_color="transparent", border_width=1, border_color="white", text_color="white", hover_color="#333")
        self.btn_add_layer.pack(side="left", padx=2, expand=True)
        
        self.btn_insert_layer = ctk.CTkButton(ramka_kontrolek_warstw, text=self.t["layer_insert"], width=65, height=28, corner_radius=6, command=self.wstaw_obraz, fg_color="transparent", border_width=1, border_color="white", text_color="white", hover_color="#333")
        self.btn_insert_layer.pack(side="left", padx=2, expand=True)
        
        self.btn_del_layer = ctk.CTkButton(ramka_kontrolek_warstw, text=self.t["layer_del"], width=65, height=28, corner_radius=6, command=self.usun_aktywna_warstwe, fg_color="transparent", border_width=1, border_color="white", text_color="white", hover_color="#333")
        self.btn_del_layer.pack(side="left", padx=2, expand=True)

        ramka_strzalek = ctk.CTkFrame(self.panel_prawy, fg_color="transparent")
        ramka_strzalek.pack(pady=0)
        self.btn_up_layer = ctk.CTkButton(ramka_strzalek, text="⏶", width=60, height=24, corner_radius=6, command=lambda: self.przesun_warstwe(-1), fg_color="transparent", border_width=1, border_color="white", text_color="white", hover_color="#333")
        self.btn_up_layer.pack(side="left", padx=5)
        self.btn_down_layer = ctk.CTkButton(ramka_strzalek, text="⏷", width=60, height=24, corner_radius=6, command=lambda: self.przesun_warstwe(1), fg_color="transparent", border_width=1, border_color="white", text_color="white", hover_color="#333")
        self.btn_down_layer.pack(side="left", padx=5)

        self.lbl_opacity = ctk.CTkLabel(self.panel_prawy, text=self.t["opacity"])
        self.lbl_opacity.pack(pady=(15, 0))
        self.slider_opacity = ctk.CTkSlider(self.panel_prawy, from_=0.0, to=1.0, command=self.zmien_krycie_warstwy, button_color="#888", button_hover_color="#bbb")
        self.slider_opacity.set(1.0)
        self.slider_opacity.pack(pady=(5, 15), padx=20)

        self.panel_listy_warstw = ctk.CTkScrollableFrame(self.panel_prawy, fg_color="transparent", corner_radius=6)
        self.panel_listy_warstw.pack(fill="both", expand=True, padx=10, pady=5)

        self.btn_zapisz = ctk.CTkButton(self.panel_prawy, text=self.t["save"], height=36, corner_radius=6, command=self.zapisz_obraz, fg_color="transparent", border_width=1, border_color="white", text_color="white", hover_color="#333")
        self.btn_zapisz.pack(side="bottom", pady=(10, 20), padx=20, fill="x")

        self.bind("<Control-z>", lambda e: self.cofnij())
        self.bind("<Command-z>", lambda e: self.cofnij()) 
        self.bind("<Control-s>", lambda e: self.zapisz_obraz())
        self.bind("<Command-s>", lambda e: self.zapisz_obraz()) 
        self.bind("<Control-o>", lambda e: self.otworz_obraz())
        self.bind("<Command-o>", lambda e: self.otworz_obraz()) 
        self.bind("<Key>", self.obsloz_skroty_narzedzi)

    def stworz_pole_px(self, rodzic, tekst, rzad, kolumna):
        ramka = ctk.CTkFrame(rodzic, fg_color="transparent")
        ramka.grid(row=rzad, column=kolumna, padx=2, pady=2, sticky="ew")
        lbl = ctk.CTkLabel(ramka, text=tekst, font=("Arial", 11))
        lbl.pack(side="left")
        entry = ctk.CTkEntry(ramka, height=28, corner_radius=4, font=("Arial", 11))
        entry.pack(side="left", padx=2, expand=True, fill="x")
        return entry, lbl

    def zamykanie_okna(self):
        try:
            with open("pygraph_cfg.txt", "w") as f:
                f.write(self.geometry())
        except:
            pass
        self.destroy()

    def _update_text(self, widget_name, text_key):
        try:
            widget = getattr(self, widget_name)
            widget.configure(text=self.t[text_key])
        except Exception:
            pass 

    def przelacz_jezyk(self):
        stary_jezyk = self.lang
        obecny_wybor = self.combo_filtry.get()
        wybrany_klucz = "bw"
        for k in self.klucze_filtrow:
            if TEXTS[stary_jezyk][k] == obecny_wybor:
                wybrany_klucz = k
                break

        self.lang = "en" if self.lang == "pl" else "pl"
        self.t = TEXTS[self.lang]
        
        self.title(self.t["title"])
        self.btn_lang.configure(text="PL" if self.lang == "pl" else "EN")
        
        self._update_text("lbl_narzedzia", "tools")
        self._update_text("btn_otworz", "open")
        self._update_text("btn_cofnij", "undo")
        self._update_text("lbl_transform", "transform")
        self._update_text("btn_obroc", "rotate")
        self._update_text("lbl_adjust", "adjust")
        self._update_text("lbl_brightness", "brightness")
        self._update_text("lbl_contrast", "contrast")
        self._update_text("lbl_saturation", "saturation")
        self._update_text("lbl_sharpness", "sharpness")
        self._update_text("lbl_scale", "scale")
        self._update_text("btn_apply_adj", "apply_adj")
        self._update_text("lbl_interactive", "interactive")
        self._update_text("btn_move", "move")
        self._update_text("btn_brush", "brush")
        self._update_text("btn_text", "text")
        self._update_text("btn_rect", "rectangle")
        self._update_text("btn_color", "color")
        self._update_text("lbl_size", "size")
        self._update_text("lbl_font_size", "font_size")
        self._update_text("lbl_efekty", "effects")
        self._update_text("btn_zastosuj_filtr", "apply_filter")
        self._update_text("btn_rembg", "remove_bg")
        self._update_text("lbl_kadrowanie", "crop")
        self._update_text("lbl_w", "width")
        self._update_text("lbl_h", "height")
        self._update_text("btn_dokladne_crop", "crop_apply")
        self._update_text("lbl_layers_title", "layers")
        self._update_text("btn_add_layer", "layer_add")
        self._update_text("btn_insert_layer", "layer_insert")
        self._update_text("btn_del_layer", "layer_del")
        self._update_text("lbl_opacity", "opacity")
        self._update_text("btn_zapisz", "save")
        self._update_text("text_label", "help")

        if self.aktywne_narzedzie == 'crop':
            self._update_text("btn_crop", "crop_off")
        else:
            self._update_text("btn_crop", "crop_on")
            
        nowe_wartosci = [self.t[k] for k in self.klucze_filtrow]
        self.combo_filtry.configure(values=nowe_wartosci)
        self.combo_filtry.set(self.t[wybrany_klucz])
        
        self.zaktualizuj_styl_narzedzi()

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
        elif char == 'r': self.ustaw_narzedzie('rect')
        elif char == 'c': self.ustaw_narzedzie('crop')

    def stworz_przycisk_narzedzia(self, rodzic, tekst, wartosc):
        return ctk.CTkButton(rodzic, text=tekst, height=32, width=50, corner_radius=6, 
                             fg_color="transparent", border_width=1, border_color="white", 
                             text_color="white", hover_color="#333", command=lambda: self.ustaw_narzedzie(wartosc))

    def zaktualizuj_styl_narzedzi(self):
        act = {"fg_color": "transparent", "text_color": "white", "border_width": 2, "border_color": "white"}
        inact = {"fg_color": "transparent", "text_color": "white", "border_width": 1, "border_color": "white"}
        
        self.btn_move.configure(**(act if self.aktywne_narzedzie == 'move' else inact))
        self.btn_brush.configure(**(act if self.aktywne_narzedzie == 'brush' else inact))
        self.btn_text.configure(**(act if self.aktywne_narzedzie == 'text' else inact))
        self.btn_rect.configure(**(act if self.aktywne_narzedzie == 'rect' else inact))
        
        if self.aktywne_narzedzie == 'crop':
            self.btn_crop.configure(text=self.t["crop_off"], **act)
        else:
            self.btn_crop.configure(text=self.t["crop_on"], **inact)

    def wybierz_kolor(self):
        kolor = colorchooser.askcolor(color=self.current_color)[1]
        if kolor: 
            self.current_color = kolor
            self.btn_color.configure(text_color=kolor)

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
                self.btn_cofnij.configure(state="disabled", fg_color="transparent", text_color="gray50", border_color="white")
                
                nazwa = os.path.basename(sciezka)[:15]
                self.dodaj_warstwe(img, nazwa)
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
                
                pusta = Image.new("RGBA", self.doc_size, (0, 0, 0, 0))
                x = (self.doc_size[0] - img.width) // 2
                y = (self.doc_size[1] - img.height) // 2
                pusta.paste(img, (x, y))
                
                nazwa = os.path.basename(sciezka)[:12]
                
                idx = self.aktywna_warstwa + 1 if self.aktywna_warstwa != -1 else 0
                self.warstwy.insert(idx, {'nazwa': nazwa, 'obraz': pusta, 'widoczna': True, 'krycie': 1.0})
                self.ustaw_aktywna_warstwe(idx)
            except Exception as e:
                messagebox.showerror(self.t["msg_err_title"], f"{self.t['err_open']} {e}")

    def dodaj_warstwe(self, obraz, nazwa):
        self.warstwy.append({'nazwa': nazwa, 'obraz': obraz, 'widoczna': True, 'krycie': 1.0})
        self.odswiez_panel_warstw()
        self.komponuj_i_wyswietl()

    def dodaj_pusta_warstwe(self):
        if not self.doc_size: return
        self.zatwierdz_podglad()
        self.zapisz_stan_do_historii()
        pusta = Image.new("RGBA", self.doc_size, (0, 0, 0, 0))
        nazwa = f"{self.t['new_layer']} {len(self.warstwy)}"
        
        idx = self.aktywna_warstwa + 1 if self.aktywna_warstwa != -1 else 0
        self.warstwy.insert(idx, {'nazwa': nazwa, 'obraz': pusta, 'widoczna': True, 'krycie': 1.0})
        self.ustaw_aktywna_warstwe(idx)

    def usun_aktywna_warstwe(self):
        if len(self.warstwy) <= 1: return 
        self.zatwierdz_podglad()
        self.zapisz_stan_do_historii()
        del self.warstwy[self.aktywna_warstwa]
        self.ustaw_aktywna_warstwe(max(0, self.aktywna_warstwa - 1))

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
            
            ramka = ctk.CTkFrame(self.panel_listy_warstw, fg_color="transparent", corner_radius=6)
            ramka.pack(fill="x", pady=3, padx=2)
            
            is_active = (i == self.aktywna_warstwa)
            bw = 2 if is_active else 1
            
            ikona = "👁" if w['widoczna'] else "✖"
            btn_vis = ctk.CTkButton(ramka, text=ikona, width=30, fg_color="transparent", border_width=1, border_color="white", text_color="white", hover_color="#333", command=lambda idx=i: self.przelacz_widocznosc(idx))
            btn_vis.pack(side="left", padx=5, pady=5)
            
            btn_name = ctk.CTkButton(ramka, text=w['nazwa'], fg_color="transparent", border_width=bw, border_color="white", text_color="white", hover_color="#333", anchor="w", command=lambda idx=i: self.ustaw_aktywna_warstwe(idx))
            btn_name.pack(side="left", fill="x", expand=True, padx=5, pady=5)
            
            btn_rename = ctk.CTkButton(ramka, text="✎", width=25, fg_color="transparent", border_width=1, border_color="white", text_color="white", hover_color="#333", command=lambda idx=i: self.zmien_nazwe_warstwy(idx))
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
                
                if w['krycie'] < 1.0:
                    img = img.copy()
                    alpha = img.split()[3]
                    alpha = alpha.point(lambda p: int(p * w['krycie']))
                    img.putalpha(alpha)
                    
                kompozyt = Image.alpha_composite(kompozyt, img)

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
            self.warstwy[self.aktywna_warstwa]['obraz'] = self.warstwa_podgladowa
            self.warstwa_podgladowa = None
            
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
            kopia_warstw.append({
                'nazwa': w['nazwa'],
                'widoczna': w['widoczna'],
                'krycie': w['krycie'],
                'obraz': w['obraz'].copy()
            })
        self.historia.append((self.doc_size, self.aktywna_warstwa, kopia_warstw))
        self.btn_cofnij.configure(state="normal", fg_color="transparent", border_width=1, border_color="white", text_color="white")

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
            if not self.historia: 
                self.btn_cofnij.configure(state="disabled", fg_color="transparent", border_width=1, border_color="white", text_color="gray50")
            self.resetuj_suwaki()
            if self.aktywne_narzedzie: self.ustaw_narzedzie(self.aktywne_narzedzie)
            self.odswiez_panel_warstw()
            self.komponuj_i_wyswietl()

    def podglad_suwakow(self, value=None):
        if getattr(self, 'blokuj_podglad', False): return
        if self.aktywna_warstwa == -1: return
        if self.aktywne_narzedzie: self.ustaw_narzedzie(self.aktywne_narzedzie)

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
            new_w = max(1, int(self.doc_size[0] * sc_val))
            new_h = max(1, int(self.doc_size[1] * sc_val))
            scaled = rgb.resize((new_w, new_h), Image.Resampling.LANCZOS)
            pusta = Image.new("RGBA", self.doc_size, (0, 0, 0, 0))
            offset_x = (self.doc_size[0] - new_w) // 2
            offset_y = (self.doc_size[1] - new_h) // 2
            pusta.paste(scaled, (offset_x, offset_y))
            rgb = pusta
            
        self.warstwa_podgladowa = rgb
        self.komponuj_i_wyswietl()

    def zastosuj_suwaki(self):
        self.zatwierdz_podglad()

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
        self.zatwierdz_podglad()
        self.zapisz_stan_do_historii()
        
        img = self.warstwy[self.aktywna_warstwa]['obraz']
        if img.mode != "RGBA": img = img.convert("RGBA")
            
        r, g, b, a = img.split()
        rgb = Image.merge("RGB", (r, g, b))
        
        if filter_type == "grayscale": rgb = ImageOps.grayscale(rgb).convert("RGB")
        elif filter_type == "invert": rgb = ImageOps.invert(rgb)
        else: rgb = rgb.filter(filter_type)
        
        r2, g2, b2 = rgb.split()
        self.warstwy[self.aktywna_warstwa]['obraz'] = Image.merge("RGBA", (r2, g2, b2, a))
        self.komponuj_i_wyswietl()

    def filtr_szary(self): self.nałoż_filtr("grayscale")
    def filtr_rozmycie(self): self.nałoż_filtr(ImageFilter.GaussianBlur(radius=3))
    def filtr_wyostrzenie(self): self.nałoż_filtr(ImageFilter.SHARPEN)
    def filtr_negatyw(self): self.nałoż_filtr("invert")
    def filtr_plaskorzezba(self): self.nałoż_filtr(ImageFilter.EMBOSS)
    def filtr_krawedzie(self): self.nałoż_filtr(ImageFilter.FIND_EDGES)
    
    def zastosuj_wybrany_filtr(self):
        w = self.combo_filtry.get()
        k = next((key for key in self.klucze_filtrow if self.t[key] == w), None)
        if k == "bw": self.filtr_szary()
        elif k == "blur": self.filtr_rozmycie()
        elif k == "sharpen": self.filtr_wyostrzenie()
        elif k == "invert": self.filtr_negatyw()
        elif k == "emboss": self.filtr_plaskorzezba()
        elif k == "edges": self.filtr_krawedzie()

    def obroc_obraz(self):
        if self.aktywna_warstwa != -1:
            self.zatwierdz_podglad()
            self.zapisz_stan_do_historii()
            self.warstwy[self.aktywna_warstwa]['obraz'] = self.warstwy[self.aktywna_warstwa]['obraz'].rotate(-90, expand=True)
            if self.aktywna_warstwa == 0:
                self.doc_size = (self.doc_size[1], self.doc_size[0])
            self.komponuj_i_wyswietl()

    def usun_tlo(self):
        if self.aktywna_warstwa == -1: return
        try:
            self.zatwierdz_podglad()
            self.zapisz_stan_do_historii()
            self.config(cursor="watch")
            self.update()
            
            wynik = remove(self.warstwy[self.aktywna_warstwa]['obraz'])
            if wynik.mode != "RGBA": wynik = wynik.convert("RGBA")
            self.warstwy[self.aktywna_warstwa]['obraz'] = wynik
            
            self.komponuj_i_wyswietl()
        except Exception as e:
            messagebox.showerror(self.t["msg_err_title"], f"Błąd AI: {e}")
        finally:
            self.config(cursor="")

    def zastosuj_ciecie(self):
        if not self.warstwy or not self.rect_coords: return
        try:
            self.zatwierdz_podglad()
            x1, y1, x2, y2 = self.rect_coords
            rx1, ry1 = self.canvas_to_image_coords(min(x1, x2), min(y1, y2))
            rx2, ry2 = self.canvas_to_image_coords(max(x1, x2), max(y1, y2))
            
            box = (max(0, rx1), max(0, ry1), min(self.doc_size[0], rx2), min(self.doc_size[1], ry2))
            
            self.zapisz_stan_do_historii()
            for w in self.warstwy: w['obraz'] = w['obraz'].crop(box)
            self.doc_size = (box[2]-box[0], box[3]-box[1])
            
            self.ustaw_narzedzie('crop')
            self.komponuj_i_wyswietl()
        except Exception as e:
            messagebox.showerror(self.t["msg_err_title"], f"Błąd kadrowania: {e}")

    def zastosuj_ciecie_z_pol(self):
        if not self.warstwy: return
        try:
            x, y = int(self.entry_x.get()), int(self.entry_y.get())
            w, h = int(self.entry_w.get()), int(self.entry_h.get())
            img_w, img_h = self.doc_size

            if w <= 0 or h <= 0: raise ValueError(self.t["err_dim"])
            x, y = max(0, x), max(0, y)
            w, h = min(w, img_w - x), min(h, img_h - y)

            self.zatwierdz_podglad()
            self.zapisz_stan_do_historii()
            box = (x, y, x + w, y + h)
            for warstwa in self.warstwy: warstwa['obraz'] = warstwa['obraz'].crop(box)
            self.doc_size = (box[2]-box[0], box[3]-box[1])
            
            if self.aktywne_narzedzie: self.ustaw_narzedzie(self.aktywne_narzedzie)
            self.komponuj_i_wyswietl()
        except ValueError as e:
            messagebox.showerror(self.t["err_val"], f"{self.t['err_val']} {e}")

    def canvas_to_image_coords(self, c_x, c_y):
        if not self.doc_size: return 0, 0
        rel_x = c_x - self.canvas_img_x_offset
        rel_y = c_y - self.canvas_img_y_offset
        r_x = self.doc_size[0] / self.display_width
        r_y = self.doc_size[1] / self.display_height
        return int(rel_x * r_x), int(rel_y * r_y)

    def zastosuj_rysowanie(self, typ, end_x=None, end_y=None):
        if self.aktywna_warstwa == -1: return
        self.zatwierdz_podglad()
        self.zapisz_stan_do_historii()
        
        img = self.warstwy[self.aktywna_warstwa]['obraz']
        draw = ImageDraw.Draw(img)
        rgb = tuple(int(self.current_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)) + (255,)
        rozmiar = int(self.slider_size.get())

        if typ == 'brush' and len(self.draw_points) > 1:
            real_pts = [self.canvas_to_image_coords(px, py) for px, py in self.draw_points]
            draw.line(real_pts, fill=rgb, width=rozmiar, joint="curve")
        elif typ == 'rect' and end_x and end_y:
            rx1, ry1 = self.canvas_to_image_coords(self.last_x, self.last_y)
            rx2, ry2 = self.canvas_to_image_coords(end_x, end_y)
            draw.rectangle([min(rx1, rx2), min(ry1, ry2), max(rx1, rx2), max(ry1, ry2)], outline=rgb, width=rozmiar)
            if self.temp_draw_id: self.canvas.delete(self.temp_draw_id)
            
        self.komponuj_i_wyswietl()

    def wstaw_tekst(self, x, y):
        tekst = simpledialog.askstring("Tekst", "Wpisz tekst:")
        if not tekst: return self.ustaw_narzedzie('text')
        
        self.zatwierdz_podglad()
        self.zapisz_stan_do_historii()
        
        rx, ry = self.canvas_to_image_coords(x, y)
        img = self.warstwy[self.aktywna_warstwa]['obraz']
        draw = ImageDraw.Draw(img)
        rgb = tuple(int(self.current_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)) + (255,)
        rozmiar_czcionki = int(self.slider_font_size.get())
        
        try: font = ImageFont.truetype("arial.ttf", size=rozmiar_czcionki)
        except: font = ImageFont.load_default()
        
        draw.text((rx, ry), tekst, fill=rgb, font=font)
        self.ustaw_narzedzie('text')
        self.komponuj_i_wyswietl()

    def on_canvas_press(self, event):
        if self.aktywna_warstwa == -1 or not self.aktywne_narzedzie: return
        
        self.zatwierdz_podglad()
        
        x, y = event.x, event.y
        self.last_x, self.last_y = x, y

        if self.aktywne_narzedzie == 'move':
            self.zapisz_stan_do_historii()
            self.move_original_img = self.warstwy[self.aktywna_warstwa]['obraz'].copy()
        elif self.aktywne_narzedzie == 'crop':
            if not self.rect_coords: self.akcja_myszy, self.rect_coords = 'draw', [x, y, x, y]
            else:
                x1, y1, x2, y2 = self.rect_coords
                xm, xx, ym, yx = min(x1,x2), max(x1,x2), min(y1,y2), max(y1,y2)
                if abs(x-xm)<10 and abs(y-ym)<10: self.akcja_myszy = 'resize_tl'
                elif xm<x<xx and ym<y<yx: self.akcja_myszy = 'move'
                else: self.akcja_myszy, self.rect_coords = 'draw', [x, y, x, y]
            self.rysuj_ramke_na_plotnie()
        elif self.aktywne_narzedzie == 'brush': self.draw_points = [(x, y)]
        elif self.aktywne_narzedzie == 'text': self.wstaw_tekst(x, y)
        elif self.aktywne_narzedzie == 'rect': self.temp_draw_id = self.canvas.create_rectangle(x,y,x,y, outline=self.current_color, width=self.slider_size.get())

    def on_canvas_drag(self, event):
        if self.aktywna_warstwa == -1 or not self.aktywne_narzedzie: return
        x, y = event.x, event.y
        
        if self.aktywne_narzedzie == 'move' and hasattr(self, 'move_original_img'):
            dx = x - self.last_x
            dy = y - self.last_y
            r_x = self.doc_size[0] / self.display_width
            r_y = self.doc_size[1] / self.display_height
            
            idx = int(dx * r_x)
            idy = int(dy * r_y)
            
            pusta = Image.new("RGBA", self.doc_size, (0, 0, 0, 0))
            pusta.paste(self.move_original_img, (idx, idy))
            self.warstwy[self.aktywna_warstwa]['obraz'] = pusta
            self.komponuj_i_wyswietl()
            
        elif self.aktywne_narzedzie == 'crop' and self.akcja_myszy:
            dx, dy = x - self.last_x, y - self.last_y
            if self.akcja_myszy == 'draw': self.rect_coords[2], self.rect_coords[3] = x, y
            elif self.akcja_myszy == 'move':
                self.rect_coords[0] += dx; self.rect_coords[1] += dy
                self.rect_coords[2] += dx; self.rect_coords[3] += dy
            elif self.akcja_myszy == 'resize_tl': self.rect_coords[0], self.rect_coords[1] = x, y
            elif self.akcja_myszy == 'resize_tr': self.rect_coords[2], self.rect_coords[1] = x, y
            elif self.akcja_myszy == 'resize_bl': self.rect_coords[0], self.rect_coords[3] = x, y
            elif self.akcja_myszy == 'resize_br': self.rect_coords[2], self.rect_coords[3] = x, y
            self.last_x, self.last_y = x, y
            self.rysuj_ramke_na_plotnie()
        elif self.aktywne_narzedzie == 'brush':
            self.canvas.create_line(self.last_x, self.last_y, x, y, fill=self.current_color, width=self.slider_size.get(), capstyle=tk.ROUND, smooth=True)
            self.draw_points.append((x, y))
            self.last_x, self.last_y = x, y
        elif self.aktywne_narzedzie == 'rect' and self.temp_draw_id:
            self.canvas.coords(self.temp_draw_id, self.last_x, self.last_y, x, y)

    def on_canvas_release(self, event):
        if self.aktywna_warstwa == -1 or not self.aktywne_narzedzie: return
        
        if self.aktywne_narzedzie == 'move':
            if hasattr(self, 'move_original_img'): del self.move_original_img 
        elif self.aktywne_narzedzie == 'brush': self.zastosuj_rysowanie('brush')
        elif self.aktywne_narzedzie == 'rect': self.zastosuj_rysowanie('rect', event.x, event.y)

    def rysuj_ramke_na_plotnie(self):
        self.canvas.delete("crop_element")
        if not self.rect_coords: return
        x1, y1, x2, y2 = self.rect_coords
        self.canvas.create_rectangle(x1, y1, x2, y2, outline='#00ff00', width=2, dash=(5,5), tags="crop_element")
        r, k = 5, '#00ff00'
        for px, py in [(x1,y1), (x2,y1), (x1,y2), (x2,y2)]: self.canvas.create_oval(px-r, py-r, px+r, py+r, fill=k, tags="crop_element")

    def ustaw_narzedzie(self, narzedzie):
        if not self.warstwy: return
        self.zatwierdz_podglad()
        self.canvas.delete("crop_element"); self.rect_coords = None; self.canvas.config(cursor="")
        
        if self.aktywne_narzedzie == narzedzie:
            self.aktywne_narzedzie = None
        else:
            self.aktywne_narzedzie = narzedzie
            if narzedzie == 'crop': self.canvas.config(cursor="cross")
            elif narzedzie == 'brush': self.canvas.config(cursor="pencil")
            elif narzedzie == 'text': self.canvas.config(cursor="xterm")
            elif narzedzie == 'rect': self.canvas.config(cursor="crosshair")
            elif narzedzie == 'move': self.canvas.config(cursor="fleur") 

        self.zaktualizuj_styl_narzedzi()

    def przy_zmianie_rozmiaru(self, event):
        self.canvas.coords("help_text", event.width / 2, event.height / 2)
        if self.warstwy:
            if self.resize_timer: self.after_cancel(self.resize_timer)
            self.resize_timer = self.after(150, lambda: self.ustaw_narzedzie('crop') if self.aktywne_narzedzie == 'crop' else self.komponuj_i_wyswietl())

    def zapisz_obraz(self, event=None):
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
    aplikacja = PyGraph()
    aplikacja.mainloop()