import tkinter as tk
from tkinter import filedialog, messagebox
import re
import csv
from pathlib import Path
import threading
import math




class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Spectra Entropy Calculator")
        self.geometry("400x400")
        self.file_paths = []

        self.upload_button = tk.Button(self, text="Upload files", command=self.upload_files)
        self.upload_button.pack(pady=10)

        self.file_listbox = tk.Listbox(self)
        self.file_listbox.pack(pady=10)

        self.start_button = tk.Button(self, text="Start", command=self.start_processing)
        self.start_button.pack(pady=10)

        self.iconbitmap(r'C:\Users\Figeys Lab M5846\PycharmProjects\pythonProject\icon.ico')

    def upload_files(self):
        filenames = filedialog.askopenfilenames(filetypes=(("MS1 files", "*.ms1"), ("All files", "*.*")))
        for file in filenames:
            if file not in self.file_paths:
                self.file_paths.append(file)
                self.file_listbox.insert('end', file)

    def start_processing(self):
        if not self.file_paths:
            messagebox.showerror("error", "Please upload the file first.")
            return

        self.processed_files = 0
        for file_path in self.file_paths:
            thread = threading.Thread(target=self.process_file, args=(file_path,))
            thread.start()


        messagebox.showinfo("Running", "File uploaded successfully, please wait.")

    def process_file(self, file_path):
        # Read the file
        with open(file_path, "r") as file:
            ms1 = file.read().splitlines()

        # Function to calculate entropy
        def cal_entropy(intensities):
            I = [i / sum(intensities) for i in intensities]
            IlnI = [-i * math.log(i) for i in I if i > 0]  # Exclude zero intensities to avoid log(0)
            entropy = sum(IlnI)
            return entropy

        # Remove empty spectra
        rt_indices = [i for i, s in enumerate(ms1) if "RTime" in s]
        tic_indices = [i for i, s in enumerate(ms1) if "TIC" in s]
        remove_indices = [i for i in rt_indices if (i + 3) not in tic_indices]

        new_indices = []
        for i in remove_indices:
            new_indices.extend([i - 1, i - 2])
        remove_indices.extend(new_indices)

        remove_indices = set(remove_indices)
        ms1 = [s for i, s in enumerate(ms1) if i not in remove_indices]



        # Extract TIC, BPM, RT, and Scan
        tic = [re.search(r'TIC\t(.*)', s).group(1) for s in ms1 if "TIC" in s]
        bpm = [re.search(r'BPM\t(.*)', s).group(1) for s in ms1 if "BPM" in s]
        rt = [re.search(r'RTime\t(.*)', s).group(1) for s in ms1 if "RTime" in s]
        scan = [re.search(r'scan=(.*)', s).group(1) for s in ms1 if "scan" in s]

        # Pre-process MS1 data for entropy calculation
        ms1 = ms1[5:]
        ms1.append("S")
        scan_index = [i for i, s in enumerate(ms1) if "scan" in s]
        s_index = [i for i, s in enumerate(ms1) if "S" in s]
        ion_count = [s_index - scan_index - 5 for s_index, scan_index in zip(s_index, scan_index)]


        # Calculate entropy for each spectrum
        spec_entr = []
        for i in range(len(s_index)):
            c = ms1[(scan_index[i] + 5):(s_index[i] - 1)]
            intensities = []
            for line in c:
                parts = line.split(" ")
                if len(parts) == 2:
                    try:
                        intensity = float(parts[1])
                        intensities.append(intensity)
                    except ValueError:
                        continue
            spec_entr.append(cal_entropy(intensities))

        spec_entr_n = [e / math.log(count) for e, count in zip(spec_entr, ion_count)]

        # Create a list of results
        spec_entr_table = zip(spec_entr, spec_entr_n, ion_count, tic, rt, scan, bpm)

        # Save the results
        output_file = Path(file_path).with_suffix('.csv')
        with open(output_file, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(
                ["spectra entropy", "normalized spectra entropy", "number of peaks", "TIC", "RT", "scan", "BPM"])
            for row in spec_entr_table:
                csvwriter.writerow(row)

        # 处理完成后增加已处理文件数量
        self.processed_files += 1

        # 当所有文件都处理完成时，显示成功消息
        if self.processed_files == len(self.file_paths):
            self.show_success_message()

    def show_success_message(self):
        messagebox.showinfo("Success", "All files have been dealt with.")



if __name__ == "__main__":
    app = Application()
    app.mainloop()
