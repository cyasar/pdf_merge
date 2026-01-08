import customtkinter as ctk
from tkinter import filedialog, messagebox, Menu
from pypdf import PdfWriter
import os
import fitz  # PyMuPDF
from PIL import Image
import io
import json
from datetime import datetime

# Set appearance mode and default color theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

HISTORY_FILE = "history.json"

class PDFMergerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window setup
        self.title("Akademik Portal PDF Birleştirme Yazılımı")
        self.geometry("900x700")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Create Menu
        self._create_menu()

        self.pdf_files = []

        # Header
        self.header_frame = ctk.CTkFrame(self, corner_radius=0)
        self.header_frame.grid(row=0, column=0, sticky="ew")
        
        self.header_label = ctk.CTkLabel(self.header_frame, text="Akademik Portal PDF Birleştirme Yazılımı", font=("Roboto Medium", 22))
        self.header_label.pack(pady=(20, 5), padx=20)

        self.author_label = ctk.CTkLabel(self.header_frame, text="Hazırlayan: Dr. Cumali Yaşar\nİletişim: cumali.yasar@gmail.com\nÇanakkale Onsekiz Mart Üniversitesi - Enformatik Bölümü", font=("Roboto", 12), text_color="gray")
        self.author_label.pack(pady=(0, 20), padx=20)

        # File List Area
        self.scrollable_frame = ctk.CTkScrollableFrame(self, label_text="Seçilen Dosyalar")
        self.scrollable_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        
        # Action Buttons Area
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=20)
        self.button_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        self.add_button = ctk.CTkButton(self.button_frame, text="Dosya Ekle", command=self.add_files, height=40, font=("Roboto Medium", 14))
        self.add_button.grid(row=0, column=0, padx=10, sticky="ew")

        self.clear_button = ctk.CTkButton(self.button_frame, text="Temizle", command=self.clear_files, height=40, fg_color="#CF3A3A", hover_color="#962A2A", font=("Roboto Medium", 14))
        self.clear_button.grid(row=0, column=1, padx=10, sticky="ew")
        
        self.history_button = ctk.CTkButton(self.button_frame, text="Geçmiş", command=self.show_history, height=40, fg_color="#555", hover_color="#333", font=("Roboto Medium", 14))
        self.history_button.grid(row=0, column=2, padx=10, sticky="ew")

        self.preview_button = ctk.CTkButton(self.button_frame, text="Ön İzleme", command=self.preview_merged_pdf, height=40, fg_color="#E0A800", hover_color="#C69500", text_color="white", font=("Roboto Medium", 14))
        self.preview_button.grid(row=0, column=3, padx=10, sticky="ew")

        self.merge_button = ctk.CTkButton(self.button_frame, text="BİRLEŞTİR", command=self.merge_pdfs, height=40, fg_color="#2CC985", hover_color="#228C5E", text_color="white", font=("Roboto Medium", 14))
        self.merge_button.grid(row=0, column=4, padx=10, sticky="ew")

        # Status Bar
        self.status_label = ctk.CTkLabel(self, text="Hazır", font=("Roboto", 12), text_color="gray")
        self.status_label.grid(row=3, column=0, sticky="w", padx=20, pady=(0, 10))

    def _create_menu(self):
        menubar = Menu(self)
        self.config(menu=menubar)

        # File Menu
        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Dosya", menu=file_menu)
        file_menu.add_command(label="Çıkış", command=self.quit)

        # Help Menu
        help_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Yardım", menu=help_menu)
        help_menu.add_command(label="Nasıl Kullanılır?", command=self.show_usage)
        help_menu.add_command(label="Hakkında", command=self.show_about)

    def show_usage(self):
        usage_text = (
            "1. 'Dosya Ekle' butonu ile PDF veya Resim dosyası seçin.\n"
            "2. Dosyaları ↑ ve ↓ tuşlarıyla sıralayın.\n"
            "3. 'Ön İzleme' ile sonucun nasıl görüneceğine bakın.\n"
            "4. 'BİRLEŞTİR' tuşu ile dosyayı kaydedin."
        )
        messagebox.showinfo("Nasıl Kullanılır", usage_text)

    def show_about(self):
        about_text = (
            "Akademik Portal PDF Birleştirme Yazılımı\n"
            "Versiyon 1.2\n\n"
            "Hazırlayan: Dr. Cumali Yaşar\n"
            "İletişim: cumali.yasar@gmail.com\n"
            "Çanakkale Onsekiz Mart Üniversitesi\n"
            "Enformatik Bölümü"
        )
        messagebox.showinfo("Hakkında", about_text)

    def load_history(self):
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []

    def save_to_history(self, file_path):
        history = self.load_history()
        entry = {
            "path": file_path,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        # Add to beginning
        history.insert(0, entry)
        # Keep last 20
        history = history[:20]
        
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=4)

    def show_history(self):
        history = self.load_history()
        if not history:
            messagebox.showinfo("Geçmiş", "Henüz kayıtlı işlem yok.")
            return

        history_window = ctk.CTkToplevel(self)
        history_window.title("İşlem Geçmişi")
        history_window.geometry("700x500")
        
        # Make the window modal-like by bringing it to front
        history_window.attributes('-topmost', True)
        
        title_lbl = ctk.CTkLabel(history_window, text="Geçmiş İşlemler", font=("Roboto Medium", 18))
        title_lbl.pack(pady=10)
        
        scroll = ctk.CTkScrollableFrame(history_window)
        scroll.pack(fill="both", expand=True, padx=10, pady=10)

        for item in history:
            path = item.get('path')
            date = item.get('date')
            
            # Check if file still exists
            exists = os.path.exists(path)
            
            row = ctk.CTkFrame(scroll, fg_color="transparent")
            row.pack(fill="x", pady=5)
            
            lbl_date = ctk.CTkLabel(row, text=date, width=150, text_color="gray", anchor="w")
            lbl_date.pack(side="left", padx=5)
            
            btn_text = os.path.basename(path) if exists else f"{os.path.basename(path)} (Silinmiş)"
            
            if exists:
                # Use a closure to capture 'path' correctly in the loop
                link_btn = ctk.CTkButton(row, text=btn_text, fg_color="#333", border_width=0, 
                                         text_color="#4db6ac", hover_color="#444", anchor="w",
                                         command=lambda p=path: self.open_history_file(p))
                link_btn.pack(side="left", fill="x", expand=True, padx=5)
            else:
                 lbl_deleted = ctk.CTkLabel(row, text=btn_text, text_color="#ef5350", anchor="w")
                 lbl_deleted.pack(side="left", fill="x", expand=True, padx=5)

    def open_history_file(self, path):
        try:
            os.startfile(path)
        except Exception as e:
            messagebox.showerror("Hata", f"Dosya açılamadı:\n{e}")

    def add_files(self):
        files = filedialog.askopenfilenames(filetypes=[("PDF & Images", "*.pdf *.png *.jpg *.jpeg")])
        if files:
            for file in files:
                if file not in self.pdf_files:
                    self.pdf_files.append(file)
            self.update_file_list()
            self.status_label.configure(text=f"{len(self.pdf_files)} dosya seçildi.")

    def update_file_list(self):
        # Clear current widgets
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        for index, file_path in enumerate(self.pdf_files):
            filename = os.path.basename(file_path)
            
            # Row container
            row_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
            row_frame.pack(fill="x", pady=2)
            
            # Icon/Index
            index_label = ctk.CTkLabel(row_frame, text=f"{index+1}.", width=30, anchor="w")
            index_label.pack(side="left", padx=(5,0))
            
            # Filename
            lbl = ctk.CTkLabel(row_frame, text=filename, anchor="w")
            lbl.pack(side="left", fill="x", expand=True, padx=5)
            
            # Move Up
            if index > 0:
                up_btn = ctk.CTkButton(row_frame, text="↑", width=30, height=20, fg_color="#555", hover_color="#333", command=lambda i=index: self.move_file(i, -1))
                up_btn.pack(side="right", padx=2)
            
            # Move Down
            if index < len(self.pdf_files) - 1:
                down_btn = ctk.CTkButton(row_frame, text="↓", width=30, height=20, fg_color="#555", hover_color="#333", command=lambda i=index: self.move_file(i, 1))
                down_btn.pack(side="right", padx=2)

            # Remove button
            remove_btn = ctk.CTkButton(row_frame, text="X", width=30, height=20, fg_color="#CF3A3A", hover_color="#962A2A", command=lambda f=file_path: self.remove_file(f))
            remove_btn.pack(side="right", padx=5)

    def move_file(self, index, direction):
        new_index = index + direction
        if 0 <= new_index < len(self.pdf_files):
            self.pdf_files[index], self.pdf_files[new_index] = self.pdf_files[new_index], self.pdf_files[index]
            self.update_file_list()

    def remove_file(self, file_path):
        if file_path in self.pdf_files:
            self.pdf_files.remove(file_path)
            self.update_file_list()
            self.status_label.configure(text=f"{len(self.pdf_files)} dosya seçildi.")

    def clear_files(self):
        self.pdf_files = []
        self.update_file_list()
        self.status_label.configure(text="Liste temizlendi.")

    def _append_to_merger(self, merger, file_path):
        """Helper to append either PDF or Image file to the merger"""
        if file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            try:
                img = Image.open(file_path)
                if img.mode == 'RGBA':
                    img = img.convert('RGB')
                
                # Create an in-memory PDF from image
                img_bytes = io.BytesIO()
                img.save(img_bytes, format='PDF')
                img_bytes.seek(0)
                
                merger.append(img_bytes)
            except Exception as e:
                print(f"Error converting image {file_path}: {e}")
                # You might want to log this or skip
        else:
            # Assume PDF
            merger.append(file_path)

    def _create_merged_pdf_in_memory(self):
        merger = PdfWriter()
        for file_path in self.pdf_files:
            self._append_to_merger(merger, file_path)
        
        memory_file = io.BytesIO()
        merger.write(memory_file)
        memory_file.seek(0)
        return memory_file

    def preview_merged_pdf(self):
        if len(self.pdf_files) < 1:
            messagebox.showwarning("Uyarı", "Ön izleme için en az 1 dosya seçmelisiniz.")
            return

        self.status_label.configure(text="Ön izleme oluşturuluyor...")
        self.update()

        try:
            # Merge to memory
            merged_stream = self._create_merged_pdf_in_memory()
            
            # Open with PyMuPDF
            doc = fitz.open(stream=merged_stream, filetype="pdf")
            
            # Create Preview Window
            preview_window = ctk.CTkToplevel(self)
            preview_window.title("PDF Ön İzleme")
            preview_window.geometry("600x800")
            
            # Make the window modal-like by bringing it to front
            preview_window.attributes('-topmost', True)
            
            # Scrollable frame for pages
            page_scroll = ctk.CTkScrollableFrame(preview_window, label_text=f"Toplam Sayfa: {len(doc)}")
            page_scroll.pack(fill="both", expand=True, padx=10, pady=10)
            
            # Render pages (Limit to first 50)
            max_pages = min(len(doc), 50) 
            for page_num in range(max_pages):
                page = doc.load_page(page_num)
                # Calculate zoom to fit width of 500
                zoom = 500 / page.rect.width
                mat = fitz.Matrix(zoom, zoom)
                pix = page.get_pixmap(matrix=mat)
                
                # Convert to PIL Image
                mode = "RGBA" if pix.alpha else "RGB"
                img = Image.frombytes(mode, [pix.width, pix.height], pix.samples)
                
                # Create CTkImage
                ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(pix.width, pix.height))
                
                # Label for page
                img_label = ctk.CTkLabel(page_scroll, image=ctk_img, text="")
                img_label.pack(pady=10)
                
                num_label = ctk.CTkLabel(page_scroll, text=f"Sayfa {page_num + 1}")
                num_label.pack(pady=(0, 20))

            if len(doc) > max_pages:
                warning_label = ctk.CTkLabel(page_scroll, text=f"... ve {len(doc) - max_pages} sayfa daha (Performans için gizlendi)", text_color="orange")
                warning_label.pack(pady=20)

            self.status_label.configure(text="Ön izleme hazır.")

        except Exception as e:
            messagebox.showerror("Hata", f"Ön izleme hatası:\n{e}")
            self.status_label.configure(text="Ön izleme hatası.")

    def merge_pdfs(self):
        if len(self.pdf_files) < 2 and len(self.pdf_files) > 0:
             # Just one file is okay if we are converting image to PDF, but usually merge imply 2+.
             # But user said "merge images to single pdf", so even 1 image -> 1 pdf is valid.
             pass
        elif len(self.pdf_files) == 0:
            messagebox.showwarning("Uyarı", "Lütfen en az 1 dosya seçin.")
            return

        try:
            output_file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
            if not output_file:
                return

            self.status_label.configure(text="Birleştiriliyor...")
            self.update()

            merger = PdfWriter()
            for file_path in self.pdf_files:
                self._append_to_merger(merger, file_path)

            merger.write(output_file)
            merger.close()

            # Save to history
            self.save_to_history(output_file)

            self.status_label.configure(text="İşlem tamamlandı!")
            messagebox.showinfo("Başarılı", f"PDFler başarıyla birleştirildi:\n{output_file}")
            
            # Open the file
            os.startfile(output_file)

        except Exception as e:
            messagebox.showerror("Hata", f"Bir hata oluştu:\n{e}")
            self.status_label.configure(text="Hata oluştu.")

if __name__ == "__main__":
    app = PDFMergerApp()
    app.mainloop()
