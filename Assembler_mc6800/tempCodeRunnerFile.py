import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from assembler import Assembler, AssemblerError

# Renk ve font ayarları
BG_COLOR = "#fce4ec"
BTN_COLOR = "#c8e6c9"
FONT_COLOR = "#4a4a4a"
MEM_USED_COLOR = "#dcedc8"
TITLE_FONT = ("Helvetica", 12, "bold")
LABEL_FONT = ("Helvetica", 10)
TEXT_FONT = ("Consolas", 11)
MEM_FONT = ("Consolas", 8)

class AssemblerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("MC6800 Assembler")
        self.root.configure(bg=BG_COLOR)
        self.root.geometry("1200x700")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=3)
        self.root.grid_columnconfigure(1, weight=2)

        self.asm = Assembler()

        # Sol Panel
        sol_frame = tk.Frame(self.root, bg=BG_COLOR)
        sol_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        sol_frame.grid_rowconfigure(1, weight=1)
        sol_frame.grid_columnconfigure(0, weight=1)

        tk.Label(sol_frame, text="Assembly Kodu", bg=BG_COLOR, fg=FONT_COLOR, font=TITLE_FONT).grid(row=0, column=0, sticky="w")

        kod_frame = tk.Frame(sol_frame, bg=BG_COLOR)
        kod_frame.grid(row=1, column=0, sticky="nsew")

        self.satir_numaralari = tk.Text(kod_frame, width=4, padx=4, takefocus=0, border=0,
                                        background=BG_COLOR, state="disabled", fg=FONT_COLOR,
                                        font=TEXT_FONT)
        self.satir_numaralari.pack(side="left", fill="y")

        self.kod_alani = tk.Text(kod_frame, wrap="none", font=TEXT_FONT)
        self.kod_alani.pack(side="left", fill="both", expand=True)
        self.kod_alani.bind("<KeyRelease>", self.guncelle_satir_numaralari)

        scrollbar = tk.Scrollbar(kod_frame)
        scrollbar.pack(side="right", fill="y")
        self.kod_alani.config(yscrollcommand=scrollbar.set)
        self.satir_numaralari.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.kod_scroll)

        btn_frame = tk.Frame(sol_frame, bg=BG_COLOR)
        btn_frame.grid(row=2, column=0, pady=5)

        self.btn_yukle = tk.Button(btn_frame, text="📂 Kod Yükle", command=self.kod_yukle, bg=BTN_COLOR,
                                   activebackground="#a5d6a7", fg=FONT_COLOR, font=LABEL_FONT)
        self.btn_yukle.pack(side="left", padx=5)

        self.btn_derle = tk.Button(btn_frame, text="❤ Derle", command=self.derle, bg=BTN_COLOR,
                                   activebackground="#a5d6a7", fg=FONT_COLOR, font=("Helvetica", 12, "bold"))
        self.btn_derle.pack(side="left", padx=5)

        self.status_label = tk.Label(sol_frame, text="", bg=BG_COLOR, fg="green", font=("Consolas", 10))
        self.status_label.grid(row=3, column=0, pady=5, sticky="w")

        self.ceviri_tablosu = ttk.Treeview(sol_frame, columns=("Adres", "Kod", "Opcode", "Operand"), show="headings")
        for col in ("Adres", "Kod", "Opcode", "Operand"):
            self.ceviri_tablosu.heading(col, text=col)
            self.ceviri_tablosu.column(col, anchor="center")
        self.ceviri_tablosu.grid(row=4, column=0, sticky="nsew", pady=10)
        sol_frame.grid_rowconfigure(4, weight=1)

        # Sağ Panel
        sag_frame = tk.Frame(self.root, bg=BG_COLOR)
        sag_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        sag_frame.grid_rowconfigure(1, weight=1)
        sag_frame.grid_columnconfigure(0, weight=1)

        reg_frame = tk.LabelFrame(sag_frame, text="Registerlar", bg=BG_COLOR, fg=FONT_COLOR, font=LABEL_FONT)
        reg_frame.grid(row=0, column=0, sticky="ew", pady=5)

        self.reg_labels = {}
        for idx, reg in enumerate(["A", "B", "X", "SP"]):
            lbl = tk.Label(reg_frame, text=f"{reg}: 00", font=TEXT_FONT, bg=BG_COLOR, fg=FONT_COLOR)
            lbl.grid(row=idx, column=0, sticky="w")
            self.reg_labels[reg] = lbl

        mem_frame = tk.LabelFrame(sag_frame, text="Bellek (256 byte)", bg=BG_COLOR, fg=FONT_COLOR)
        mem_frame.grid(row=1, column=0, sticky="nsew")
        mem_frame.grid_rowconfigure(tuple(range(17)), weight=1)
        mem_frame.grid_columnconfigure(tuple(range(17)), weight=1)

        for j in range(16):
            header = tk.Label(mem_frame, text=f"{j:02X}", font=("Consolas", 9, "bold"), bg=BG_COLOR, fg=FONT_COLOR)
            header.grid(row=0, column=j+1)

        self.mem_labels = []
        for i in range(16):
            addr_lbl = tk.Label(mem_frame, text=f"{i*16:04X}", font=("Consolas", 9, "bold"), bg=BG_COLOR, fg=FONT_COLOR)
            addr_lbl.grid(row=i+1, column=0, sticky="e")

            row = []
            for j in range(16):
                lbl = tk.Label(mem_frame, text="00", width=3, relief="solid", borderwidth=1,
                               bg="white", font=MEM_FONT, fg=FONT_COLOR)
                lbl.grid(row=i+1, column=j+1, padx=1, pady=1, sticky="nsew")
                row.append(lbl)
            self.mem_labels.append(row)

        self.guncelle_gorunum()

    def kod_scroll(self, *args):
        self.kod_alani.yview(*args)
        self.satir_numaralari.yview(*args)

    def guncelle_satir_numaralari(self, event=None):
        self.satir_numaralari.config(state="normal")
        self.satir_numaralari.delete("1.0", tk.END)
        satir_sayisi = int(self.kod_alani.index('end-1c').split('.')[0])
        satirlar = "\n".join(str(i) for i in range(1, satir_sayisi + 1))
        self.satir_numaralari.insert("1.0", satirlar)
        self.satir_numaralari.config(state="disabled")

    def kod_yukle(self):
        dosya = filedialog.askopenfilename(filetypes=[("Assembly Files", "*.asm *.txt")])
        if dosya:
            with open(dosya, "r", encoding="utf-8") as f:
                icerik = f.read()
                self.kod_alani.delete("1.0", tk.END)
                self.kod_alani.insert(tk.END, icerik)
            self.guncelle_satir_numaralari()

    def derle(self):
        kod = self.kod_alani.get("1.0", tk.END)
        try:
            self.asm = Assembler()
            self.asm.assemble(kod)
            self.guncelle_gorunum()
            self.status_label.config(text="✔ Derleme Başarılı", fg="green")
            self.ceviri_tablosu.delete(*self.ceviri_tablosu.get_children())
            for satir, opcode, operand, addr in self.asm.listing:
                self.ceviri_tablosu.insert("", "end", values=(
                    f"{addr:04X}" if addr is not None else "",
                    satir.strip(),
                    f"{opcode:02X}" if opcode is not None else "",
                    operand if operand else ""
                ))
        except AssemblerError as e:
            self.status_label.config(text=f"❌ Hata: {str(e)}", fg="red")

    def guncelle_gorunum(self):
        for i in range(16):
            for j in range(16):
                val = self.asm.memory[i * 16 + j]
                lbl = self.mem_labels[i][j]
                lbl.config(text=f"{val:02X}", bg=MEM_USED_COLOR if val != 0 else "white")

        for reg, lbl in self.reg_labels.items():
            val = self.asm.registers[reg]
            if reg == "X":
                lbl.config(text=f"{reg}: {val:04X}")
            else:
                lbl.config(text=f"{reg}: {val:02X}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AssemblerGUI(root)
    root.mainloop()
