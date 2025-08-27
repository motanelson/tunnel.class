#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import tkinter as tk
from typing import List, Tuple

Point = Tuple[float, float]
Rect = Tuple[float, float, float, float]

class GameEngine:
    """
    Desenha um túnel de 'tijolos' em perspetiva com linhas pretas
    num fundo amarelo. As 4 paredes convergem para o centro, e os
    'tijolos' começam grandes e ficam pequenos até ao infinito.
    """

    def __init__(self, root: tk.Tk, bg="#FFD300"):  # amarelo forte
        self.root = root
        self.bg = bg
        self.canvas = tk.Canvas(root, highlightthickness=0, bg=bg)
        self.canvas.pack(fill="both", expand=True)

        # Render sempre que a janela muda de tamanho
        self.canvas.bind("<Configure>", lambda e: self.redraws())

        # Controlos simples (teclas) para afinar rapidamente se quiser:
        # [+]/[-] = mais/menos profundidade; [.] = fator mais pequeno; [,] = fator maior
        root.bind("+", lambda e: self._bump_depth( +5))
        root.bind("-", lambda e: self._bump_depth( -5))
        root.bind(".", lambda e: self._bump_scale( 0.02))
        root.bind(",", lambda e: self._bump_scale(-0.02))

        # parâmetros visuais
        self.margin = 16
        self.depth_layers = 70      # número de “aneis”/retângulos em profundidade
        self.scale = 0.92           # fator de encolhimento por camada (0.80–0.96)
        self.line_width = 2
        self.running_bond_offset = 0.0  # fase inicial do padrão dos tijolos
        self.redraws()

    # Pequenos helpers para ajustar em tempo real
    def _bump_depth(self, delta: int):
        self.depth_layers = max(10, min(200, self.depth_layers + delta))
        self.redraws()

    def _bump_scale(self, delta: float):
        self.scale = max(0.80, min(0.97, self.scale + delta))
        self.redraws()

    def _frames(self, w: int, h: int) -> List[Rect]:
        """Gera retângulos concêntricos que convergem ao centro (ponto de fuga)."""
        cx, cy = w / 2, h / 2
        x1, y1, x2, y2 = self.margin, self.margin, w - self.margin, h - self.margin

        frames: List[Rect] = []
        for _ in range(self.depth_layers):
            frames.append((x1, y1, x2, y2))
            # Aproximar ao centro por fator de escala
            x1 = cx + (x1 - cx) * self.scale
            y1 = cy + (y1 - cy) * self.scale
            x2 = cx + (x2 - cx) * self.scale
            y2 = cy + (y2 - cy) * self.scale
            if abs(x2 - x1) < 2 or abs(y2 - y1) < 2:
                break
        return frames

      
    def redraws(self):
        """Refaz todo o desenho (linhas pretas sobre janela amarela)."""
        c = self.canvas
        c.delete("all")
        w = c.winfo_width() or 800
        h = c.winfo_height() or 600

        # fundo amarelo
        c.configure(bg=self.bg)

        frames = self._frames(w, h)
        if len(frames) < 2:
            return

        # Desenhar os 'anéis' (as juntas horizontais do teto/chão e convergência das paredes)
        for rect in frames:
            x1, y1, x2, y2 = rect
            c.create_rectangle(x1, y1, x2, y2, outline="black", width=self.line_width)

        # Para sugerir tijolos reais nas paredes, desenhamos juntas verticais
        # que seguem um padrão deslocado (running bond) e tornam-se mais densas em profundidade.
        t = self.running_bond_offset
        for i in range(len(frames) - 1-150):
            x1, y1, x2, y2 = frames[i]
            xn1, yn1, xn2, yn2 = frames[i + 1]

            cols = max(1, int(2 + i * 0.15))
            for k in range(1, cols + 1):
                u = ((k / (cols + 1)) + t) % 1.0
            t = (t + 0.18) % 1.0
        for tt in range(0,w,64):
            c.create_line(tt, 0, w/2, h/2, width=max(1, self.line_width-1), fill="black")
        for tt in range(0,900,64):
            c.create_line(tt, h, w/2, h/2, width=max(1, self.line_width-1), fill="black")
        for tt in range(0,600,64):
            c.create_line(0, tt, w/2, h/2, width=max(1, self.line_width-1), fill="black")
        for tt in range(0,600,64):
            c.create_line(w, tt, w/2, h/2, width=max(1, self.line_width-1), fill="black")

            

def main():
    root = tk.Tk()
    root.title("Brick Tunnel - GUI Amarela (linhas pretas)")
    # Janela com fundo amarelo (também visível à volta do canvas se redimensionar)
    root.configure(bg="#FFD300")
    root.geometry("900x600")
    engine = GameEngine(root)

    # Redesenhar periodicamente é opcional; aqui não animamos para manter 100% estático e limpo.
    root.mainloop()

if __name__ == "__main__":
    main()