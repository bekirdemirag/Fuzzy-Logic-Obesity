import tkinter as tk
from tkinter import messagebox
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Bulanık mantık sistemi oluşturma
'''
ctrl.Antecedent giriş değişkenlerini 
ctrl.Consequent çıkış değişkenini tanımlamak için kullanılır.
fuzz.trapmf ve fuzz.trimf fonksiyonları üyelik fonksiyonlarını tanımlamak için kullanılır.
np.arange(start, stop, step):
vki (Vücut Kitle İndeksi): 0 ile 40 arasında değişir.
yas (Yaş): 0 ile 100 arasında değişir.
aktivite (Fiziksel Aktivite): 0 ile 10 arasında değişir.
beslenme (Beslenme Alışkanlıkları): 0 ile 10 arasında değişir.
'''
vki = ctrl.Antecedent(np.arange(0, 41, 1), 'vki')
yas = ctrl.Antecedent(np.arange(0, 101, 1), 'yas')
aktivite = ctrl.Antecedent(np.arange(0, 11, 1), 'aktivite')
beslenme = ctrl.Antecedent(np.arange(0, 11, 1), 'beslenme')
risk = ctrl.Consequent(np.arange(0, 101, 1), 'risk')

'''
"Zayıf" (Trapmf):
VKİ değeri 0-18.5 arasında tamamen "zayıf".
18.5-24 arasında "zayıf" olma derecesi azalır.
24'ten büyük bir değerin "zayıf" olma derecesi sıfırdır.
"Normal" (Trimf):
VKİ değeri 18.5-29 aralığında "normal".
24 noktasında tam anlamıyla "normal".
18.5 ve 29 kenarlarında "normal" olma derecesi azalmaktadır.
"Fazla Kilolu" (Trimf):
VKİ değeri 24-35 aralığında "fazla kilolu".
29 noktasında tam anlamıyla "fazla kilolu".
24 ve 35 kenarlarında "fazla kilolu" olma derecesi azalmaktadır.
"Obez" (Trapmf):
VKİ değeri 30-40 aralığında tamamen "obez".
35 noktasından sonra kademeli olarak 40'a kadar tam üyelik devam eder.
'''

vki['zayıf'] = fuzz.trapmf(vki.universe, [0, 0, 18.5, 24])
vki['normal'] = fuzz.trimf(vki.universe, [18.5, 24, 29])
vki['fazla kilolu'] = fuzz.trimf(vki.universe, [24, 29, 35])
vki['obez'] = fuzz.trapmf(vki.universe, [30, 35, 40, 40])

yas['genç'] = fuzz.trapmf(yas.universe, [0, 0, 25, 40])
yas['orta'] = fuzz.trimf(yas.universe, [25, 40, 60])
yas['yaşlı'] = fuzz.trapmf(yas.universe, [50, 60, 100, 100])

aktivite['düşük'] = fuzz.trapmf(aktivite.universe, [0, 0, 3, 5])
aktivite['orta'] = fuzz.trimf(aktivite.universe, [3, 5, 7])
aktivite['yüksek'] = fuzz.trapmf(aktivite.universe, [5, 7, 10, 10])

beslenme['sağlıklı'] = fuzz.trapmf(beslenme.universe, [0, 0, 3, 5])
beslenme['orta'] = fuzz.trimf(beslenme.universe, [3, 5, 7])
beslenme['sağlıksız'] = fuzz.trapmf(beslenme.universe, [5, 7, 10, 10])

risk['düşük'] = fuzz.trapmf(risk.universe, [0, 0, 30, 50])
risk['orta'] = fuzz.trimf(risk.universe, [30, 50, 70])
risk['yüksek'] = fuzz.trapmf(risk.universe, [50, 70, 100, 100])

'''rules = [
    ctrl.Rule(vki['normal'] & aktivite['yüksek'] & beslenme['sağlıklı'], risk['düşük']),
    ctrl.Rule(vki['obez'] & aktivite['düşük'] & beslenme['sağlıksız'], risk['yüksek']),
    ctrl.Rule(vki['fazla kilolu'] & yas['genç'], risk['orta']),
    ctrl.Rule(vki['zayıf'] & yas['yaşlı'] & beslenme['sağlıksız'], risk['orta']),
    ctrl.Rule(vki['obez'] & yas['yaşlı'] & aktivite['düşük'], risk['yüksek']),
    ctrl.Rule(vki['normal'] & yas['orta'] & beslenme['orta'], risk['orta']),
    ctrl.Rule(vki['zayıf'] & aktivite['orta'] & beslenme['sağlıklı'], risk['düşük']),
    ctrl.Rule(vki['fazla kilolu'] & yas['orta'] & aktivite['orta'], risk['orta']),
    ctrl.Rule(vki['obez'] & yas['orta'] & aktivite['yüksek'], risk['yüksek']),
    ctrl.Rule(vki['normal'] & yas['genç'] & aktivite['düşük'], risk['orta']),
    ctrl.Rule(vki['zayıf'] & yas['genç'] & beslenme['orta'], risk['düşük']),
    # Varsayılan kural, herhangi bir kurala uymayanalar için, orta riski atar.
    ctrl.Rule(~(vki['zayıf'] | vki['normal'] | vki['fazla kilolu'] | vki['obez']), risk['orta'])
]
'''

# Tüm kombinasyonlardan kuralları otomatik oluşturma

rules = []
for vki_label in vki.terms:
    for yas_label in yas.terms:
        for aktivite_label in aktivite.terms:
            for beslenme_label in beslenme.terms:
                # VKİ "zayıf" ise genelde düşük risk
                if vki_label == 'zayıf':
                    rules.append(ctrl.Rule(vki[vki_label] & yas[yas_label] & aktivite[aktivite_label] & beslenme[beslenme_label], risk['düşük']))
                elif vki_label == 'obez':
                    rules.append(ctrl.Rule(vki[vki_label] & yas[yas_label] & aktivite[aktivite_label] & beslenme[beslenme_label], risk['yüksek']))
                else:
                    rules.append(ctrl.Rule(vki[vki_label] & yas[yas_label] & aktivite[aktivite_label] & beslenme[beslenme_label], risk['orta']))


obesity_ctrl = ctrl.ControlSystem(rules)
obesity_sim = ctrl.ControlSystemSimulation(obesity_ctrl)

# Üyelik derecelerini hesaplayan fonksiyon
def calculate_membership(variable, value):
    memberships = {}
    for label in variable.terms:
        memberships[label] = fuzz.interp_membership(variable.universe, variable[label].mf, value)
    return memberships

# Obezite riskini hesaplama
def calculate_risk():
    try:
        # Kullanıcıdan alınan değerler
        vki_value = float(vki_entry.get())
        yas_value = float(yas_entry.get())
        aktivite_value = float(aktivite_entry.get())
        beslenme_value = float(beslenme_entry.get())

        # Bulanık mantık hesaplaması
        obesity_sim.input['vki'] = vki_value
        obesity_sim.input['yas'] = yas_value
        obesity_sim.input['aktivite'] = aktivite_value
        obesity_sim.input['beslenme'] = beslenme_value
        obesity_sim.compute()

        # Sonucu göster
        result = f"Obezite Riski: {obesity_sim.output['risk']:.2f}"
        messagebox.showinfo("Sonuç", result)

    except Exception as e:
        messagebox.showerror("Hata", f"Giriş değerlerinde bir hata var: {e}")

# Hesaplama detaylarını gösterme
def calculate_risk_with_details():
    try:
        # Kullanıcıdan alınan değerler
        vki_value = float(vki_entry.get())
        yas_value = float(yas_entry.get())
        aktivite_value = float(aktivite_entry.get())
        beslenme_value = float(beslenme_entry.get())

        # Üyelik derecelerini hesaplama
        vki_memberships = calculate_membership(vki, vki_value)
        yas_memberships = calculate_membership(yas, yas_value)
        aktivite_memberships = calculate_membership(aktivite, aktivite_value)
        beslenme_memberships = calculate_membership(beslenme, beslenme_value)

        # Detayları ekrana yazdırma
        details = "Giriş Değerleri ve Üyelik Dereceleri:\n"
        details += f"VKI: {vki_value} -> {vki_memberships}\n"
        details += f"Yaş: {yas_value} -> {yas_memberships}\n"
        details += f"Fiziksel Aktivite: {aktivite_value} -> {aktivite_memberships}\n"
        details += f"Beslenme: {beslenme_value} -> {beslenme_memberships}\n"

        # Bulanık mantık hesaplaması
        obesity_sim.input['vki'] = vki_value
        obesity_sim.input['yas'] = yas_value
        obesity_sim.input['aktivite'] = aktivite_value
        obesity_sim.input['beslenme'] = beslenme_value
        obesity_sim.compute()

        # Sonucu ekleme
        details += f"\nObezite Riski: {obesity_sim.output['risk']:.2f}"

        # Sonuçları kullanıcıya göster
        messagebox.showinfo("Hesaplama Detayları", details)

    except Exception as e:
        messagebox.showerror("Hata", f"Giriş değerlerinde bir hata var: {e}")

# Tkinter GUI
root = tk.Tk()
root.title("Obezite Riski Tahmini")

# Giriş alanları
tk.Label(root, text="Vücut Kitle İndeksi (VKİ):").grid(row=0, column=0, padx=10, pady=5)
vki_entry = tk.Entry(root)
vki_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Yaş:").grid(row=1, column=0, padx=10, pady=5)
yas_entry = tk.Entry(root)
yas_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Fiziksel Aktivite (0-10):").grid(row=2, column=0, padx=10, pady=5)
aktivite_entry = tk.Entry(root)
aktivite_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Beslenme (0-10):").grid(row=3, column=0, padx=10, pady=5)
beslenme_entry = tk.Entry(root)
beslenme_entry.grid(row=3, column=1, padx=10, pady=5)

# Hesaplama düğmeleri
calculate_button = tk.Button(root, text="Risk Hesapla", command=calculate_risk)
calculate_button.grid(row=4, column=0, columnspan=2, pady=10)

details_button = tk.Button(root, text="Hesaplama Detayları", command=calculate_risk_with_details)
details_button.grid(row=5, column=0, columnspan=2, pady=10)

# Uygulamayı çalıştır
root.mainloop()