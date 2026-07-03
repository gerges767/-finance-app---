import os
import re
import sqlite3
from datetime import datetime, timedelta
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.utils import platform
from kivymd.app import MDApp
from kivymd.uix.snackbar import Snackbar

# حجم الشاشة للاختبار على الكمبيوتر فقط
if platform != 'android':
    Window.size = (360, 720)

KV = '''
MDScreenManager:
    id: sm

    # ===== الشاشة الرئيسية =====
    MDScreen:
        name: "home"
        md_bg_color: [0.04, 0.12, 0.20, 1]

        MDBoxLayout:
            orientation: "vertical"

            # رأس التطبيق
            MDBoxLayout:
                size_hint_y: None
                height: "100dp"
                padding: "12dp", "10dp"
                md_bg_color: [0.02, 0.07, 0.12, 1]
                orientation: "vertical"

                MDLabel:
                    text: "💼 محفظة التمويل والتحصيل"
                    font_style: "H6"
                    halign: "center"
                    bold: True
                    theme_text_color: "Custom"
                    text_color: [0.0, 0.75, 0.95, 1]

                MDLabel:
                    id: date_lbl
                    text: ""
                    font_style: "Caption"
                    halign: "center"
                    theme_text_color: "Custom"
                    text_color: [0.5, 0.75, 0.85, 1]

            # بطاقة التنبيه
            MDCard:
                size_hint_y: None
                height: "75dp"
                padding: "12dp"
                margin: "10dp", "8dp", "10dp", "4dp"
                md_bg_color: [0.35, 0.04, 0.06, 1]
                radius: [12]

                MDLabel:
                    id: alert_lbl
                    text: "⏳ جاري الفحص..."
                    halign: "center"
                    bold: True
                    theme_text_color: "Custom"
                    text_color: [1, 0.4, 0.4, 1]

            # الإحصائيات
            MDBoxLayout:
                size_hint_y: None
                height: "78dp"
                spacing: "6dp"
                padding: "10dp", "4dp"

                MDCard:
                    padding: "6dp"
                    md_bg_color: [0.04, 0.22, 0.38, 1]
                    radius: [10]
                    orientation: "vertical"
                    MDLabel:
                        id: s_total
                        text: "0"
                        font_style: "H5"
                        halign: "center"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: [0.0, 0.9, 1, 1]
                    MDLabel:
                        text: "العملاء"
                        font_style: "Caption"
                        halign: "center"
                        theme_text_color: "Custom"
                        text_color: [0.7, 0.9, 1, 1]

                MDCard:
                    padding: "6dp"
                    md_bg_color: [0.06, 0.30, 0.12, 1]
                    radius: [10]
                    orientation: "vertical"
                    MDLabel:
                        id: s_paid
                        text: "0"
                        font_style: "H5"
                        halign: "center"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: [0.3, 1, 0.5, 1]
                    MDLabel:
                        text: "مدفوع"
                        font_style: "Caption"
                        halign: "center"
                        theme_text_color: "Custom"
                        text_color: [0.6, 1, 0.7, 1]

                MDCard:
                    padding: "6dp"
                    md_bg_color: [0.32, 0.14, 0.04, 1]
                    radius: [10]
                    orientation: "vertical"
                    MDLabel:
                        id: s_pending
                        text: "0"
                        font_style: "H5"
                        halign: "center"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: [1, 0.6, 0.2, 1]
                    MDLabel:
                        text: "معلق"
                        font_style: "Caption"
                        halign: "center"
                        theme_text_color: "Custom"
                        text_color: [1, 0.8, 0.5, 1]

                MDCard:
                    padding: "6dp"
                    md_bg_color: [0.22, 0.06, 0.30, 1]
                    radius: [10]
                    orientation: "vertical"
                    MDLabel:
                        id: s_overdue
                        text: "0"
                        font_style: "H5"
                        halign: "center"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: [1, 0.3, 0.9, 1]
                    MDLabel:
                        text: "متأخر"
                        font_style: "Caption"
                        halign: "center"
                        theme_text_color: "Custom"
                        text_color: [1, 0.6, 1, 1]

            # أزرار القائمة
            ScrollView:
                MDBoxLayout:
                    orientation: "vertical"
                    padding: "12dp"
                    spacing: "7dp"
                    adaptive_height: True

                    MDRaisedButton:
                        text: "➕  إضافة عميل جديد"
                        md_bg_color: [0.0, 0.45, 0.70, 1]
                        size_hint_x: 1
                        height: "50dp"
                        font_size: "15sp"
                        on_release: app.go("add_client")

                    MDRaisedButton:
                        text: "📋  قائمة العملاء والأقساط"
                        md_bg_color: [0.04, 0.28, 0.48, 1]
                        size_hint_x: 1
                        height: "50dp"
                        font_size: "15sp"
                        on_release: app.go("clients")

                    MDRaisedButton:
                        text: "✅  تسجيل تحصيل قسط"
                        md_bg_color: [0.08, 0.42, 0.18, 1]
                        size_hint_x: 1
                        height: "50dp"
                        font_size: "15sp"
                        on_release: app.go("collect")

                    MDRaisedButton:
                        text: "🚨  الأقساط المتأخرة"
                        md_bg_color: [0.45, 0.06, 0.08, 1]
                        size_hint_x: 1
                        height: "50dp"
                        font_size: "15sp"
                        on_release: app.go("overdue")

                    MDRaisedButton:
                        text: "📊  التقارير والإحصائيات"
                        md_bg_color: [0.35, 0.20, 0.04, 1]
                        size_hint_x: 1
                        height: "50dp"
                        font_size: "15sp"
                        on_release: app.go("reports")

                    MDRaisedButton:
                        text: "📁  استيراد بيانات من ملف"
                        md_bg_color: [0.25, 0.10, 0.42, 1]
                        size_hint_x: 1
                        height: "50dp"
                        font_size: "15sp"
                        on_release: app.open_file_manager()

            MDLabel:
                text: "Mokhtar Gerges  —  محفظة التمويل الرقمية"
                font_style: "Caption"
                halign: "center"
                size_hint_y: None
                height: "26dp"
                theme_text_color: "Custom"
                text_color: [0.3, 0.5, 0.6, 1]

    # ===== إضافة عميل =====
    MDScreen:
        name: "add_client"
        md_bg_color: [0.04, 0.12, 0.20, 1]

        MDBoxLayout:
            orientation: "vertical"

            MDTopAppBar:
                title: "إضافة عميل جديد"
                specific_text_color: [0.0, 0.85, 1, 1]
                md_bg_color: [0.02, 0.07, 0.12, 1]
                left_action_items: [["arrow-right", lambda x: app.go("home")]]

            ScrollView:
                MDBoxLayout:
                    orientation: "vertical"
                    padding: "14dp"
                    spacing: "9dp"
                    adaptive_height: True

                    MDTextField:
                        id: f_name
                        hint_text: "اسم العميل كامل *"
                        mode: "rectangle"
                        text_color_normal: [1,1,1,1]
                        hint_text_color_normal: [0.5,0.75,0.9,1]
                        line_color_normal: [0.0,0.6,0.85,1]
                        halign: "right"

                    MDTextField:
                        id: f_phone
                        hint_text: "رقم هاتف العميل *"
                        mode: "rectangle"
                        input_filter: "int"
                        text_color_normal: [1,1,1,1]
                        hint_text_color_normal: [0.5,0.75,0.9,1]
                        line_color_normal: [0.0,0.6,0.85,1]
                        halign: "right"

                    MDTextField:
                        id: f_address
                        hint_text: "العنوان"
                        mode: "rectangle"
                        text_color_normal: [1,1,1,1]
                        hint_text_color_normal: [0.5,0.75,0.9,1]
                        line_color_normal: [0.0,0.6,0.85,1]
                        halign: "right"

                    MDTextField:
                        id: f_guarantor
                        hint_text: "اسم الضامن"
                        mode: "rectangle"
                        text_color_normal: [1,1,1,1]
                        hint_text_color_normal: [0.5,0.75,0.9,1]
                        line_color_normal: [0.0,0.6,0.85,1]
                        halign: "right"

                    MDTextField:
                        id: f_gphone
                        hint_text: "هاتف الضامن"
                        mode: "rectangle"
                        input_filter: "int"
                        text_color_normal: [1,1,1,1]
                        hint_text_color_normal: [0.5,0.75,0.9,1]
                        line_color_normal: [0.0,0.6,0.85,1]
                        halign: "right"

                    MDTextField:
                        id: f_total
                        hint_text: "إجمالي مبلغ التمويل (ج.م) *"
                        mode: "rectangle"
                        input_filter: "float"
                        text_color_normal: [1,1,1,1]
                        hint_text_color_normal: [0.5,0.75,0.9,1]
                        line_color_normal: [0.0,0.6,0.85,1]
                        halign: "right"

                    MDTextField:
                        id: f_count
                        hint_text: "عدد الأقساط *"
                        mode: "rectangle"
                        input_filter: "int"
                        text_color_normal: [1,1,1,1]
                        hint_text_color_normal: [0.5,0.75,0.9,1]
                        line_color_normal: [0.0,0.6,0.85,1]
                        halign: "right"

                    MDTextField:
                        id: f_start
                        hint_text: "تاريخ أول قسط (YYYY-MM-DD)"
                        mode: "rectangle"
                        text_color_normal: [1,1,1,1]
                        hint_text_color_normal: [0.5,0.75,0.9,1]
                        line_color_normal: [0.0,0.6,0.85,1]
                        halign: "right"

                    MDTextField:
                        id: f_notes
                        hint_text: "ملاحظات"
                        mode: "rectangle"
                        text_color_normal: [1,1,1,1]
                        hint_text_color_normal: [0.5,0.75,0.9,1]
                        line_color_normal: [0.0,0.6,0.85,1]
                        halign: "right"
                        multiline: True

                    MDRaisedButton:
                        text: "💾  حفظ العميل وإنشاء جدول الأقساط"
                        md_bg_color: [0.0, 0.52, 0.22, 1]
                        size_hint_x: 1
                        height: "52dp"
                        font_size: "15sp"
                        on_release: app.save_client()

    # ===== قائمة العملاء =====
    MDScreen:
        name: "clients"
        md_bg_color: [0.04, 0.12, 0.20, 1]

        MDBoxLayout:
            orientation: "vertical"

            MDTopAppBar:
                title: "قائمة العملاء"
                specific_text_color: [0.0, 0.85, 1, 1]
                md_bg_color: [0.02, 0.07, 0.12, 1]
                left_action_items: [["arrow-right", lambda x: app.go("home")]]
                right_action_items: [["refresh", lambda x: app.load_clients()]]

            MDTextField:
                id: search_f
                hint_text: "🔍 بحث باسم أو هاتف العميل..."
                size_hint_y: None
                height: "48dp"
                on_text: app.load_clients(self.text)
                padding: "8dp"
                text_color_normal: [1,1,1,1]

            ScrollView:
                MDList:
                    id: clients_lv

    # ===== تسجيل التحصيل =====
    MDScreen:
        name: "collect"
        md_bg_color: [0.04, 0.12, 0.20, 1]

        MDBoxLayout:
            orientation: "vertical"

            MDTopAppBar:
                title: "تسجيل التحصيل"
                specific_text_color: [0.0, 0.85, 1, 1]
                md_bg_color: [0.02, 0.07, 0.12, 1]
                left_action_items: [["arrow-right", lambda x: app.go("home")]]

            ScrollView:
                MDBoxLayout:
                    orientation: "vertical"
                    padding: "14dp"
                    spacing: "10dp"
                    adaptive_height: True

                    MDTextField:
                        id: col_search
                        hint_text: "ابحث باسم أو هاتف العميل"
                        mode: "rectangle"
                        text_color_normal: [1,1,1,1]
                        hint_text_color_normal: [0.5,0.75,0.9,1]
                        line_color_normal: [0.0,0.6,0.85,1]
                        on_text: app.search_collect(self.text)

                    MDCard:
                        size_hint_y: None
                        height: "180dp"
                        padding: "12dp"
                        md_bg_color: [0.04, 0.20, 0.32, 1]
                        radius: [12]

                        MDLabel:
                            id: col_result
                            text: "اكتب اسم أو هاتف العميل للبحث..."
                            theme_text_color: "Custom"
                            text_color: [0.7, 0.9, 1, 1]
                            halign: "center"

                    MDRaisedButton:
                        text: "✅  تأكيد تحصيل القسط"
                        md_bg_color: [0.08, 0.48, 0.18, 1]
                        size_hint_x: 1
                        height: "52dp"
                        font_size: "15sp"
                        on_release: app.confirm_collect()

                    MDRaisedButton:
                        text: "✅  تحصيل الكل (جميع الأقساط المستحقة)"
                        md_bg_color: [0.04, 0.35, 0.14, 1]
                        size_hint_x: 1
                        height: "52dp"
                        font_size: "14sp"
                        on_release: app.collect_all()

    # ===== الأقساط المتأخرة =====
    MDScreen:
        name: "overdue"
        md_bg_color: [0.08, 0.02, 0.02, 1]

        MDBoxLayout:
            orientation: "vertical"

            MDTopAppBar:
                title: "الأقساط المتأخرة"
                specific_text_color: [1, 0.4, 0.4, 1]
                md_bg_color: [0.18, 0.02, 0.02, 1]
                left_action_items: [["arrow-right", lambda x: app.go("home")]]
                right_action_items: [["refresh", lambda x: app.load_overdue()]]

            ScrollView:
                MDList:
                    id: overdue_lv

    # ===== التقارير =====
    MDScreen:
        name: "reports"
        md_bg_color: [0.04, 0.12, 0.20, 1]

        MDBoxLayout:
            orientation: "vertical"

            MDTopAppBar:
                title: "التقارير والإحصائيات"
                specific_text_color: [0.0, 0.85, 1, 1]
                md_bg_color: [0.02, 0.07, 0.12, 1]
                left_action_items: [["arrow-right", lambda x: app.go("home")]]
                right_action_items: [["refresh", lambda x: app.load_reports()]]

            ScrollView:
                MDBoxLayout:
                    id: reports_box
                    orientation: "vertical"
                    padding: "12dp"
                    spacing: "8dp"
                    adaptive_height: True
'''


class FinanceMobileApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "LightBlue"
        self.sel_cid = None
        db_dir = self.user_data_dir
        os.makedirs(db_dir, exist_ok=True)
        self.db_path = os.path.join(db_dir, "finance.db")
        self.init_db()
        self._fm = None
        return Builder.load_string(KV)

    def on_start(self):
        self.root.ids.date_lbl.text = "📅 " + datetime.now().strftime("%A  %d / %m / %Y")
        self.refresh_home()
        self._request_android_permissions()

    def _request_android_permissions(self):
        if platform == 'android':
            try:
                from android.permissions import request_permissions, Permission
                request_permissions([
                    Permission.READ_EXTERNAL_STORAGE,
                    Permission.WRITE_EXTERNAL_STORAGE,
                    Permission.READ_CONTACTS,
                    Permission.CAMERA,
                    Permission.INTERNET,
                    Permission.ACCESS_NETWORK_STATE,
                    Permission.RECEIVE_BOOT_COMPLETED,
                    Permission.VIBRATE,
                ])
            except Exception as e:
                pass

    def init_db(self):
        self.conn = sqlite3.connect(self.db_path)
        self.conn.execute("PRAGMA journal_mode=WAL")
        self.cur = self.conn.cursor()
        self.cur.executescript('''
            CREATE TABLE IF NOT EXISTS customers (
                id   INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT,
                address TEXT,
                guarantor TEXT,
                gphone TEXT,
                total REAL DEFAULT 0,
                count INTEGER DEFAULT 1,
                inst_amount REAL DEFAULT 0,
                start_date TEXT,
                notes TEXT,
                created TEXT DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS installments (
                id      INTEGER PRIMARY KEY AUTOINCREMENT,
                cid     INTEGER,
                num     INTEGER,
                amount  REAL,
                due     TEXT,
                paid_on TEXT,
                status  TEXT DEFAULT "Pending",
                notes   TEXT,
                FOREIGN KEY(cid) REFERENCES customers(id)
            );
        ''')
        self.conn.commit()

    # ===== التنقل بين الشاشات =====
    def go(self, name):
        self.root.current = name
        if name == "clients":     self.load_clients()
        elif name == "overdue":   self.load_overdue()
        elif name == "reports":   self.load_reports()
        elif name == "home":      self.refresh_home()

    def refresh_home(self):
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            self.cur.execute("SELECT COUNT(*) FROM customers")
            self.root.ids.s_total.text = str(self.cur.fetchone()[0])
            self.cur.execute("SELECT COUNT(*) FROM installments WHERE status='Paid'")
            self.root.ids.s_paid.text = str(self.cur.fetchone()[0])
            self.cur.execute("SELECT COUNT(*) FROM installments WHERE status='Pending'")
            self.root.ids.s_pending.text = str(self.cur.fetchone()[0])
            self.cur.execute("SELECT COUNT(*) FROM installments WHERE status='Pending' AND due<?", (today,))
            ov = self.cur.fetchone()[0]
            self.root.ids.s_overdue.text = str(ov)
            if ov > 0:
                self.root.ids.alert_lbl.text = f"🚨 تنبيه: {ov} قسط متأخر يحتاج تحصيل!"
                self.root.ids.alert_lbl.text_color = [1, 0.3, 0.3, 1]
            else:
                self.cur.execute("SELECT COUNT(*) FROM installments WHERE status='Pending' AND due=?", (today,))
                today_count = self.cur.fetchone()[0]
                if today_count > 0:
                    self.root.ids.alert_lbl.text = f"📅 لديك {today_count} قسط مستحق اليوم"
                    self.root.ids.alert_lbl.text_color = [1, 0.75, 0.2, 1]
                else:
                    self.root.ids.alert_lbl.text = "🟢 رائع! لا توجد أقساط متأخرة اليوم."
                    self.root.ids.alert_lbl.text_color = [0.3, 1, 0.5, 1]
        except Exception as e:
            pass

    # ===== حفظ عميل جديد =====
    def save_client(self):
        try:
            name  = self.root.ids.f_name.text.strip()
            phone = self.root.ids.f_phone.text.strip()
            addr  = self.root.ids.f_address.text.strip()
            guar  = self.root.ids.f_guarantor.text.strip()
            gph   = self.root.ids.f_gphone.text.strip()
            total = float(self.root.ids.f_total.text or 0)
            count = int(self.root.ids.f_count.text or 1)
            start = self.root.ids.f_start.text.strip() or datetime.now().strftime("%Y-%m-%d")
            notes = self.root.ids.f_notes.text.strip()

            if not name:
                self.snack("❌ يرجى إدخال اسم العميل!"); return
            if total <= 0:
                self.snack("❌ يرجى إدخال مبلغ التمويل!"); return
            if count <= 0:
                self.snack("❌ يرجى إدخال عدد الأقساط!"); return

            inst_amount = round(total / count, 2)
            self.cur.execute('''INSERT INTO customers
                (name,phone,address,guarantor,gphone,total,count,inst_amount,start_date,notes)
                VALUES (?,?,?,?,?,?,?,?,?,?)''',
                (name,phone,addr,guar,gph,total,count,inst_amount,start,notes))
            cid = self.cur.lastrowid

            try:
                start_dt = datetime.strptime(start, "%Y-%m-%d")
            except:
                start_dt = datetime.now()

            for i in range(count):
                due = (start_dt + timedelta(days=30*(i+1))).strftime("%Y-%m-%d")
                self.cur.execute(
                    'INSERT INTO installments (cid,num,amount,due,status) VALUES (?,?,?,?,"Pending")',
                    (cid, i+1, inst_amount, due))
            self.conn.commit()

            for fid in ['f_name','f_phone','f_address','f_guarantor',
                        'f_gphone','f_total','f_count','f_start','f_notes']:
                self.root.ids[fid].text = ''

            self.snack(f"✅ تم حفظ [{name}] وإنشاء {count} قسط بنجاح!")
            self.refresh_home()
            self.go("home")
        except Exception as e:
            self.snack(f"❌ خطأ: {str(e)}")

    # ===== قائمة العملاء =====
    def load_clients(self, search=""):
        from kivymd.uix.list import TwoLineListItem
        lv = self.root.ids.clients_lv
        lv.clear_widgets()
        try:
            if search and len(search) >= 1:
                self.cur.execute('''
                    SELECT c.id,c.name,c.phone,c.total,
                    COUNT(CASE WHEN i.status="Pending" THEN 1 END) pend
                    FROM customers c LEFT JOIN installments i ON c.id=i.cid
                    WHERE c.name LIKE ? OR c.phone LIKE ?
                    GROUP BY c.id ORDER BY c.id DESC''',
                    (f'%{search}%', f'%{search}%'))
            else:
                self.cur.execute('''
                    SELECT c.id,c.name,c.phone,c.total,
                    COUNT(CASE WHEN i.status="Pending" THEN 1 END) pend
                    FROM customers c LEFT JOIN installments i ON c.id=i.cid
                    GROUP BY c.id ORDER BY c.id DESC''')
            rows = self.cur.fetchall()
            if not rows:
                from kivymd.uix.list import OneLineListItem
                lv.add_widget(OneLineListItem(text="لا يوجد عملاء — أضف عميلاً جديداً"))
                return
            for r in rows:
                cid,name,phone,total,pend = r
                item = TwoLineListItem(
                    text=f"[b]{name}[/b]  |  {phone or '—'}",
                    secondary_text=f"التمويل: {total:,.0f} ج.م  |  أقساط معلقة: {pend}"
                )
                item.bind(on_release=lambda x, c=cid, n=name: self.client_detail(c, n))
                lv.add_widget(item)
        except Exception as e:
            self.snack(f"خطأ: {str(e)}")

    def client_detail(self, cid, cname):
        from kivymd.uix.dialog import MDDialog
        from kivymd.uix.button import MDRaisedButton, MDFlatButton
        self.cur.execute("SELECT * FROM customers WHERE id=?", (cid,))
        c = self.cur.fetchone()
        if not c: return
        self.cur.execute(
            "SELECT num,amount,due,status FROM installments WHERE cid=? ORDER BY num", (cid,))
        insts = self.cur.fetchall()
        paid   = sum(1 for i in insts if i[3]=='Paid')
        pend   = sum(1 for i in insts if i[3]=='Pending')
        paid_v = sum(i[1] for i in insts if i[3]=='Paid')
        pend_v = sum(i[1] for i in insts if i[3]=='Pending')
        txt  = f"📱 الهاتف: {c[2] or '—'}\n"
        txt += f"🏠 العنوان: {c[3] or '—'}\n"
        txt += f"🔒 الضامن: {c[4] or '—'}  |  {c[5] or '—'}\n"
        txt += f"💰 إجمالي التمويل: {c[6]:,.0f} ج.م\n"
        txt += f"📦 قيمة القسط: {c[8]:,.0f} ج.م\n\n"
        txt += f"✅ مدفوع: {paid} قسط = {paid_v:,.0f} ج.م\n"
        txt += f"⏳ معلق: {pend} قسط = {pend_v:,.0f} ج.م\n\n"
        nxt = [i for i in insts if i[3]=='Pending'][:3]
        if nxt:
            txt += "أقرب أقساط:\n"
            for n in nxt:
                txt += f"  • قسط #{n[0]} — {n[2]} — {n[1]:,.0f} ج.م\n"
        dlg = MDDialog(
            title=f"📋 {cname}",
            text=txt,
            buttons=[
                MDFlatButton(text="إغلاق", on_release=lambda x: dlg.dismiss()),
                MDRaisedButton(
                    text="✅ تحصيل القسط التالي",
                    md_bg_color=[0.08,0.48,0.18,1],
                    on_release=lambda x: [dlg.dismiss(), self._collect_next(cid)])
            ]
        )
        dlg.open()

    # ===== التحصيل =====
    def search_collect(self, text):
        if not text or len(text) < 2:
            self.root.ids.col_result.text = "اكتب اسم أو هاتف العميل للبحث..."
            self.sel_cid = None
            return
        self.cur.execute('''
            SELECT c.id,c.name,c.phone,
            COUNT(CASE WHEN i.status="Pending" THEN 1 END) pend,
            MIN(CASE WHEN i.status="Pending" THEN i.due END) ndue,
            MIN(CASE WHEN i.status="Pending" THEN i.amount END) namt
            FROM customers c LEFT JOIN installments i ON c.id=i.cid
            WHERE c.name LIKE ? OR c.phone LIKE ?
            GROUP BY c.id LIMIT 1''', (f'%{text}%', f'%{text}%'))
        r = self.cur.fetchone()
        if r:
            self.sel_cid = r[0]
            txt = f"✅ العميل: {r[1]}\nالهاتف: {r[2] or '—'}\n\n"
            if r[3] and r[3] > 0:
                txt += f"القسط القادم: {r[5]:,.0f} ج.م\nتاريخ الاستحقاق: {r[4]}\nعدد المعلق: {r[3]} قسط"
            else:
                txt += "✅ لا توجد أقساط معلقة لهذا العميل"
            self.root.ids.col_result.text = txt
        else:
            self.root.ids.col_result.text = "❌ لم يتم العثور على عميل."
            self.sel_cid = None

    def confirm_collect(self):
        if not self.sel_cid:
            self.snack("❌ ابحث عن العميل أولاً!"); return
        self._collect_next(self.sel_cid)
        self.root.ids.col_search.text = ''
        self.root.ids.col_result.text = "✅ تم التحصيل! ابحث عن عميل آخر."
        self.sel_cid = None

    def _collect_next(self, cid):
        self.cur.execute('''SELECT id FROM installments
            WHERE cid=? AND status="Pending" ORDER BY num LIMIT 1''', (cid,))
        r = self.cur.fetchone()
        if not r:
            self.snack("✅ تم تحصيل جميع أقساط هذا العميل!"); return
        today = datetime.now().strftime("%Y-%m-%d")
        self.cur.execute("UPDATE installments SET status='Paid', paid_on=? WHERE id=?",
                         (today, r[0]))
        self.conn.commit()
        self.snack("✅ تم تسجيل التحصيل بنجاح!")
        self.refresh_home()

    def collect_all(self):
        from kivymd.uix.dialog import MDDialog
        from kivymd.uix.button import MDRaisedButton, MDFlatButton
        today = datetime.now().strftime("%Y-%m-%d")
        self.cur.execute("SELECT COUNT(*) FROM installments WHERE status='Pending' AND due<=?", (today,))
        cnt = self.cur.fetchone()[0]
        if cnt == 0:
            self.snack("لا توجد أقساط مستحقة اليوم"); return
        dlg = MDDialog(
            title="⚠️ تأكيد التحصيل الكامل",
            text=f"هل تريد تحصيل كل الأقساط المستحقة ({cnt} قسط) حتى اليوم؟",
            buttons=[
                MDFlatButton(text="إلغاء", on_release=lambda x: dlg.dismiss()),
                MDRaisedButton(
                    text="✅ نعم تحصيل الكل",
                    md_bg_color=[0.08,0.48,0.18,1],
                    on_release=lambda x: [dlg.dismiss(), self._do_collect_all(today)])
            ]
        )
        dlg.open()

    def _do_collect_all(self, today):
        self.cur.execute("UPDATE installments SET status='Paid', paid_on=? WHERE status='Pending' AND due<=?",
                         (today, today))
        self.conn.commit()
        self.snack(f"✅ تم تحصيل جميع الأقساط المستحقة!")
        self.refresh_home()

    # ===== الأقساط المتأخرة =====
    def load_overdue(self):
        from kivymd.uix.list import TwoLineListItem, OneLineListItem
        lv = self.root.ids.overdue_lv
        lv.clear_widgets()
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            self.cur.execute('''
                SELECT c.name, c.phone, i.num, i.amount, i.due
                FROM installments i JOIN customers c ON i.cid=c.id
                WHERE i.status="Pending" AND i.due<=?
                ORDER BY i.due''', (today,))
            rows = self.cur.fetchall()
            if not rows:
                lv.add_widget(OneLineListItem(text="🟢 لا توجد أقساط متأخرة!")); return
            for r in rows:
                try:
                    days = (datetime.now() - datetime.strptime(r[4], "%Y-%m-%d")).days
                except:
                    days = 0
                item = TwoLineListItem(
                    text=f"{r[0]}  |  {r[2] or '—'}",
                    secondary_text=f"متأخر {days} يوم  |  {r[3]:,.0f} ج.م  |  استحق: {r[4]}"
                )
                lv.add_widget(item)
        except Exception as e:
            self.snack(f"خطأ: {str(e)}")

    # ===== التقارير =====
    def load_reports(self):
        from kivymd.uix.card import MDCard
        from kivymd.uix.label import MDLabel
        box = self.root.ids.reports_box
        box.clear_widgets()
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            self.cur.execute("SELECT COUNT(*), SUM(total) FROM customers")
            r = self.cur.fetchone()
            total_c, total_v = r[0], (r[1] or 0)
            self.cur.execute("SELECT SUM(amount) FROM installments WHERE status='Paid'")
            collected = self.cur.fetchone()[0] or 0
            self.cur.execute("SELECT SUM(amount) FROM installments WHERE status='Pending'")
            remaining = self.cur.fetchone()[0] or 0
            self.cur.execute("SELECT COUNT(*) FROM installments WHERE status='Pending' AND due<?", (today,))
            overdue_n = self.cur.fetchone()[0]
            self.cur.execute("SELECT COUNT(*) FROM installments WHERE status='Pending' AND due=?", (today,))
            today_n = self.cur.fetchone()[0]
            pct = (collected/total_v*100) if total_v > 0 else 0

            stats = [
                ("👥 إجمالي العملاء",        str(total_c),            [0.04,0.22,0.38,1]),
                ("💰 إجمالي التمويل",         f"{total_v:,.0f} ج.م",  [0.06,0.30,0.12,1]),
                ("✅ إجمالي المحصّل",          f"{collected:,.0f} ج.م",[0.08,0.40,0.16,1]),
                ("⏳ المتبقي للتحصيل",        f"{remaining:,.0f} ج.م",[0.32,0.14,0.04,1]),
                ("🚨 أقساط متأخرة",           str(overdue_n),          [0.40,0.04,0.06,1]),
                ("📅 مستحق اليوم",            str(today_n),            [0.30,0.18,0.04,1]),
                ("📈 نسبة التحصيل",           f"{pct:.1f}%",           [0.04,0.22,0.38,1]),
            ]
            for lbl_txt, val, col in stats:
                card = MDCard(
                    orientation="vertical", padding="10dp",
                    md_bg_color=col, radius=[10],
                    size_hint_y=None, height="68dp")
                card.add_widget(MDLabel(
                    text=val, font_style="H5", halign="center",
                    theme_text_color="Custom", text_color=[1,1,1,1], bold=True))
                card.add_widget(MDLabel(
                    text=lbl_txt, font_style="Caption", halign="center",
                    theme_text_color="Custom", text_color=[0.8,0.9,1,1]))
                box.add_widget(card)
        except Exception as e:
            from kivymd.uix.label import MDLabel
            box.add_widget(MDLabel(text=f"خطأ: {str(e)}"))

    # ===== استيراد الملفات =====
    def open_file_manager(self):
        from kivymd.uix.filemanager import MDFileManager
        if not self._fm:
            self._fm = MDFileManager(
                exit_manager=self._exit_fm,
                select_path=self._select_path,
                preview=False
            )
        if platform == 'android':
            path = '/sdcard'
        else:
            path = os.path.expanduser('~')
        self._fm.show(path)

    def _exit_fm(self, *args):
        if self._fm:
            self._fm.close()

    def _select_path(self, path):
        self._exit_fm()
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            phones = list(set(re.findall(r'(01[0125]\d{8})', content)))
            names  = list(set(re.findall(r'([\u0621-\u064A]{3,}\s[\u0621-\u064A]{3,})', content)))
            added = 0
            for i, name in enumerate(names[:100]):
                phone = phones[i] if i < len(phones) else ""
                self.cur.execute(
                    "INSERT INTO customers (name,phone,guarantor,total,count,inst_amount) VALUES (?,?,?,0,1,0)",
                    (name, phone, "مستورد"))
                added += 1
            self.conn.commit()
            self.refresh_home()
            self.snack(f"✅ تم استيراد {added} عميل من الملف!")
        except Exception as e:
            self.snack(f"❌ خطأ في قراءة الملف: {str(e)}")

    def snack(self, msg):
        Snackbar(
            text=msg,
            snackbar_x="10dp",
            snackbar_y="10dp",
            size_hint_x=0.95,
            bg_color=[0.04,0.22,0.38,1]
        ).open()


if __name__ == '__main__':
    FinanceMobileApp().run()
