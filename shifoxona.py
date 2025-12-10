import os
import time
import json
from datetime import datetime

if not os.path.exists("ids"):
    os.makedirs("ids")

def load_json(filename):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except:
        return {}


def save_json(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


def update_id_card(phone, event_type, details):
    filename = f"ids/{phone}.json"
    
    data = load_json(filename)
    if not data:
        data = {
            "phone": phone,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "history": []
        }
    
    record = {
        "event": event_type,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "details": details
    }
    data["history"].append(record)
    save_json(filename, data)


doctors_db = load_json("doctors.json")
users_db = load_json("users.json")
admin_db = load_json("admin.json")


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


YASHIL = '\033[32m'
QIZIL = '\033[31m'
SARIQ = '\033[33m'
KOK = '\033[34m'
RESET = '\033[0m'

def print_color(text, color=RESET):
    print(f"{color}{text}{RESET}")


def wait(seconds):
    time.sleep(seconds)


def admin_panel():
    while True:
        clear()
        print_color("--- ADMIN PANEL ---", SARIQ)
        print("1. Doktorlarni ko'rish")
        print("2. Doktor qo'shish")
        print("3. Doktor o'chirish")
        print("4. Foydalanuvchilar ro'yxati")
        print("5. Foydalanuvchini boshqarish")
        print("6. Foydalanuvchi ID Kartasini ko'rish")
        print("0. Chiqish")

        choice = input("\nTanlov: ")

        if choice == "1":
            clear()
            print_color("--- DOKTORLAR RO'YXATI ---", KOK)
            if not doctors_db:
                print("Hozircha shifokorlar yo'q.")
            else:
                for k, d in doctors_db.items():
                    print(f"ID: {k} | {d['name']} | {d['type']}")
            input("\nQaytish uchun Enter...")

        elif choice == "2":
            clear()
            print_color("--- YANGI DOKTOR QO'SHISH ---", KOK)
            doc_id = input("Doktor ID (login): ")
            if doc_id in doctors_db:
                print_color("Bu ID allaqachon mavjud!", QIZIL)
                wait(1.5)
                continue

            name = input("Ism-familiya: ")
            password = input("Parol: ")
            type_ = input("Mutaxassislik: ")

            doctors_db[doc_id] = {
                'name': name,
                'password': password,
                'type': type_,
                'bemorlar': [],
                'slots': {}
            }

            save_json("doctors.json", doctors_db)
            print_color("Doktor muvaffaqiyatli qo'shildi!", YASHIL)
            wait(1.5)

        elif choice == "3":
            clear()
            print_color("--- DOKTOR O'CHIRISH ---", KOK)
            doc_id = input("O'chirmoqchi bo'lgan doktor ID: ")
            if doc_id not in doctors_db:
                print_color("Bunday ID mavjud emas!", QIZIL)
            else:
                del doctors_db[doc_id]
                save_json("doctors.json", doctors_db)
                print_color("Doktor o'chirildi!", YASHIL)
            wait(1.5)

        elif choice == "4":
            clear()
            print_color("--- FOYDALANUVCHILAR RO'YXATI ---", KOK)
            if not users_db:
                print("Bazada foydalanuvchi yo'q.")
            else:
                for phone, u in users_db.items():
                    status = "BLOKLANGAN" if u.get("blocked") else "Faol"
                    print(f"{phone} | {u['name']} | {status}")
            input("\nQaytish uchun Enter...")

        elif choice == "5":
            clear()
            print_color("--- FOYDALANUVCHI BOSHQARISH ---", KOK)
            phone = input("Foydalanuvchi telefon raqami: ")

            if phone not in users_db:
                print_color("Bunday foydalanuvchi mavjud emas!", QIZIL)
                wait(1.5)
                continue

            usr = users_db[phone]

            while True:
                clear()
                print_color(f"{usr['name']} ({phone})", SARIQ)
                print("1. Kartasini ko'rish")
                print("2. Bloklash")
                print("3. Blokdan chiqarish")
                print("0. Chiqish")

                c = input("\nTanlov: ")

                if c == "1":
                    clear()
                    print_color("--- BEMOR KARTASI ---", KOK)
                    if not usr.get("history"):
                        print("Hali hech qaysi shifokorga murojaat qilmagan.")
                    else:
                        for i, h in enumerate(usr['history'], 1):
                            doc_name = h.get('doctor', 'Noma\'lum') # get xatolik chiqmasligi uchun, agar [] ishlatganda hech nima bo'lmasa xatolik berardi
                            doc_type = h.get('type', '')
                            time_v = h.get('time', '')
                            print(f"{i}. Shifokor: {doc_name} ({doc_type}) | Sana: {time_v}")
                    input("\nOrqaga qaytish uchun Enter...")

                elif c == "2":
                    usr["blocked"] = True
                    save_json("users.json", users_db)
                    print_color("Foydalanuvchi bloklandi!", YASHIL)
                    wait(1)

                elif c == "3":
                    usr["blocked"] = False
                    save_json("users.json", users_db)
                    print_color("Foydalanuvchi blokdan chiqarildi!", YASHIL)
                    wait(1)

                elif c == "0":
                    break
                else:
                    print_color("Xato tanlov!", QIZIL)
                    wait(1)
        
        elif choice == "6":
            clear()
            print_color("--- ID CARD KO'RISH ---", KOK)
            phone = input("Foydalanuvchi telefon raqami: ")
            filepath = f"ids/{phone}.json"
            
            if os.path.exists(filepath):
                data = load_json(filepath)
                print_color(f"\nID Fayl: {phone}", SARIQ)
                print(f"Yaratilgan sana: {data.get('created_at')}")
                print("-" * 30)
                for item in data.get('history', []):
                    print(f"[{item['timestamp']}] -> {item['event']}")
                    print(f"   Tafsilot: {item['details']}")
                    print("-" * 15)
            else:
                print_color("Bu raqamga tegishli ID karta (fayl) topilmadi.", QIZIL)
            
            input("\nQaytish uchun Enter...")

        elif choice == "0":
            break
        else:
            print_color("Noto'g'ri tanlov!", QIZIL)
            wait(1)


def doctor_panel(doc_username):
    current_doc = doctors_db[doc_username]

    while True:
        clear()
        print_color(f"--- SHIFOKOR PANELI: {current_doc['name']} ---", SARIQ)
        print(f"Mutaxassislik: {current_doc['type']}")
        print("--------------------------------")
        print("1. Bemorlar ro'yxati")
        print("2. Qabulni boshlash")
        print("3. Qabul vaqtlari qo'shish")
        print("4. Qabul vaqtlarini ko'rish")
        print("0. Chiqish")

        choice = input("\nTanlov: ")

        if choice == "1":
            clear()
            print_color("--- BEMORLAR ---", KOK)
            if not current_doc['bemorlar']:
                print("Navbatda bemor yo'q.")
            else:
                for i, p in enumerate(current_doc['bemorlar'], 1):
                    slot_time = p.get('selected_slot', 'Jonli navbat')
                    print(f"{i}. {p['name']} | Tel: {p['phone']} | Vaqt: {slot_time}")
            input("\nOrqaga qaytish uchun Enter...")

        elif choice == "2":
            if not current_doc['bemorlar']:
                print_color("Bemor yo'q!", QIZIL)
                wait(1.5)
            else:
                patient = current_doc['bemorlar'][0]
                print(f"{patient['name']} ko'rikka kiryapti...")
                wait(2)
                
                update_id_card(patient['phone'], "visit_done", {
                    "doctor": current_doc['name'],
                    "type": current_doc['type'],
                    "status": "Ko'rikdan o'tdi",
                    "slot": patient.get('selected_slot')
                })
                
                current_doc['bemorlar'].pop(0)
                save_json("doctors.json", doctors_db)
                print_color("Ko'rik tugadi va tarixga yozildi!", YASHIL)
                wait(1.5)

        elif choice == "3":
            clear()
            print_color("--- VAQT QO'SHISH ---", KOK)
            print("Format: 14:00-15:00")
            new_slot = input("Vaqt oralig'ini kiriting: ")
            
            if "slots" not in current_doc:
                current_doc["slots"] = {}
                
            if new_slot in current_doc["slots"]:
                print_color("Bu vaqt allaqachon mavjud!", QIZIL)
            else:
                current_doc["slots"][new_slot] = None 
                save_json("doctors.json", doctors_db)
                print_color(f"{new_slot} vaqti qo'shildi!", YASHIL)
            wait(1.5)

        elif choice == "4":
            clear()
            print_color("--- MENING VAQTLARIM ---", KOK)
            if "slots" not in current_doc or not current_doc["slots"]:
                print("Vaqtlar belgilanmagan.")
            else:
                for time_slot, status in current_doc["slots"].items():
                    holat = f"{QIZIL}BAND ({status}){RESET}" if status else f"{YASHIL}BO'SH{RESET}"
                    print(f"{time_slot} - {holat}")
            input("\nQaytish uchun Enter...")

        elif choice == "0":
            break

        else:
            print_color("Noto'g'ri tanlov!", QIZIL)
            wait(1)


def show_full_id_card(phone):
    clear()
    filepath = f"ids/{phone}.json"
    print_color(f"--- RAQAMLI ID KARTA: {phone} ---", KOK)
    
    if not os.path.exists(filepath):
        print("ID karta fayli topilmadi.")
    else:
        data = load_json(filepath)
        print(f"Ro'yxatdan o'tgan sana: {data.get('created_at', 'Noma\'lum')}")
        print("\n--- TARIX ---")
        for h in data.get('history', []):
            print(f"[{h['timestamp']}] - {h['event']}")
            details = h.get('details', {})
            if 'doctor' in details:
                print(f"   Doktor: {details['doctor']} ({details.get('type')})")
            if 'slot' in details:
                print(f"   Vaqt: {details['slot']}")
            if 'status' in details:
                print(f"   Status: {details['status']}")
            print(" . . . . . . . . .")
            
    input("\nOrqaga qaytish uchun Enter...")


def show_user_card(phone):
    clear()
    if phone not in users_db:
        print_color("Foydalanuvchi topilmadi!", QIZIL)
        input("\nOrqaga qaytish uchun Enter...")
        return

    usr = users_db[phone]
    print_color(f"--- {usr.get('name','No-name')}NING ESKI TIBBIY KARTASI ---", KOK)

    if not usr.get("history"):
        print("Siz hali hech qaysi shifokorga murojaat qilmagansiz.")
        input("\nOrqaga qaytish uchun Enter...")
        return

    for i, h in enumerate(usr["history"], 1):
        print(f"{i}. Shifokor: {h['doctor']} | Mutaxassislik: {h['type']} | Sana: {h['time']}")

    input("\nOrqaga qaytish uchun Enter...")


def user_panel(phone):
    current_user = users_db[phone]

    while True:
        clear()
        print_color(f"--- FOYDALANUVCHI PANELI: {current_user['name']} ---", SARIQ)
        print("1. Ma'lumotlarim")
        print("2. Shifokor qabuliga yozilish")
        print("3. Mening eski kartam")
        print("4. Mening ID Kartam")
        print("0. Chiqish")

        choice = input("\nTanlov: ")

        if choice == "1":
            clear()
            print_color("--- MA'LUMOTLAR ---", KOK)
            print(f"Ism: {current_user['name']}")
            print(f"Yosh: {current_user['age']}")
            print(f"Telefon: {phone}")
            input("\nOrqaga qaytish uchun Enter...")

        elif choice == "2":
            clear()
            print_color("--- SHIFOKORLAR ---", KOK)

            doc_list = []
            for idd, d in doctors_db.items():
                doc_list.append((idd, d))
                print(f"{len(doc_list)}. {d['name']} | {d['type']}")

            print("\n0. Orqaga")
            
            try:
                sel_idx = int(input("\nShifokor raqamini tanlang: ")) - 1
            except:
                sel_idx = -1
            if sel_idx == -1:
                continue

            if 0 <= sel_idx < len(doc_list):
                selected_id, doc = doc_list[sel_idx]
                
                clear()
                print_color(f"--- {doc['name']} QABUL VAQTLARI ---", SARIQ)
                
                available_slots = []
                if "slots" in doc:
                    for t, status in doc["slots"].items():
                        if status is None:
                            available_slots.append(t)
                
                if not available_slots:
                    print_color("Bu shifokorda bo'sh vaqtlar yo'q!", QIZIL)
                    wait(2)
                    continue
                
                for i, t in enumerate(available_slots, 1):
                    print(f"{i}. {t}")
                
                try:
                    time_idx = int(input("\nVaqtni tanlang: ")) - 1
                    if 0 <= time_idx < len(available_slots):
                        chosen_time = available_slots[time_idx]
                        
                        doc['slots'][chosen_time] = phone
                        
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        doc['bemorlar'].append({
                            'name': current_user['name'],
                            'phone': phone,
                            'time': timestamp,
                            'selected_slot': chosen_time
                        })
                        
                        if "history" not in current_user:
                            current_user["history"] = []
                        current_user["history"].append({
                            'doctor': doc['name'],
                            'type': doc['type'],
                            'time': timestamp
                        })
                        
                        save_json("doctors.json", doctors_db)
                        save_json("users.json", users_db)
                        
                        update_id_card(phone, "booking", {
                            "doctor": doc['name'],
                            "type": doc['type'],
                            "slot": chosen_time,
                            "status": "Band qilindi"
                        })

                        print_color(f"{chosen_time} vaqtiga yozildingiz!", YASHIL)
                        wait(2)
                    else:
                        print_color("Xato vaqt tanlandi!", QIZIL)
                        wait(1)
                except ValueError:
                    print_color("Raqam kiriting!", QIZIL)
                    wait(1)

            else:
                print_color("Noto'g'ri shifokor tanlandi!", QIZIL)
                wait(1.5)

        elif choice == "3":
            show_user_card(phone)
        
        elif choice == "4":
            show_full_id_card(phone)

        elif choice == "0":
            break

        else:
            print_color("Noto'g'ri tanlov!", QIZIL)
            wait(1)


def login(user_type):
    clear()

    if user_type == "admin":
        print_color("--- ADMIN KIRISH ---", SARIQ)
        u = input("Login: ")
        p = input("Parol: ")

        if u == admin_db.get('username') and p == admin_db.get('password'):
            admin_panel()
        else:
            print_color("Login yoki parol noto'g'ri!", QIZIL)
            wait(1.5)


    elif user_type == "doctor":
        print_color("--- SHIFOKOR KIRISH ---", SARIQ)
        username = input("Login: ")
        password = input("Parol: ")

        if username in doctors_db and doctors_db[username]['password'] == password:
            doctor_panel(username)
        else:
            print_color("Login yoki parol noto'g'ri!", QIZIL)
            wait(1.5)


    elif user_type == "user":
        print_color("--- FOYDALANUVCHI ---", SARIQ)
        phone = input("Telefon (+998...): ")

        if phone not in users_db:
            print_color("Ro'yxatdan o'tish:", KOK)
            name = input("Ism-familiya: ")
            age = input("Yosh: ")
            password = input("Parol: ")

            users_db[phone] = {
                'name': name,
                'age': age,
                'password': password,
                'blocked': False,
                'history': []
            }

            save_json("users.json", users_db)
            
            update_id_card(phone, "register", {
                "name": name,
                "age": age,
                "status": "Created"
            })
            
            print_color("Ro'yxatdan o'tildi!", YASHIL)
            wait(1.5)
            user_panel(phone)

        else:
            if users_db[phone].get("blocked"):
                print_color("Profilingiz bloklangan!", QIZIL)
                wait(2)
                return

            password = input("Parol: ")

            if password == users_db[phone]["password"]:
                user_panel(phone)
            else:
                print_color("Parol noto'g'ri!", QIZIL)
                wait(2)


while True:
    clear()
    print_color("=== SHIFOXONA TIZIMI ===", KOK)
    print("1. Admin sifatida kirish")
    print("2. Shifokor sifatida kirish")
    print("3. Foydalanuvchi sifatida kirish")
    print("0. Chiqish")

    c = input("\nTanlov: ")

    if c == "1":
        login("admin")
    elif c == "2":
        login("doctor")
    elif c == "3":
        login("user")
    elif c == "0":
        print_color("Dastur to'xtatildi.", YASHIL)
        break
    else:
        print_color("Noto'g'ri tanlov!", QIZIL)
        wait(1)