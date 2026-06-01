from tkinter import *
from tkinter import messagebox
import pymysql
import bcrypt
import time
import datetime

class Admin:
    def __init__(self, root, username):
        self.root = root
        self.root.title("Admin") 
        self.root.geometry("1000x600+80+80")
        self.root.config(bg="lightblue")
        
        self.username = username
        self.var_username = StringVar()
        self.var_password = StringVar()

        # Database Configuration
        self.host = "localhost"
        self.user = "root"
        self.password = "#@19is16Pro"
        self.database = "nilbima" 
        


        # --- UI Elements ---
        title = Label(self.root, text="" , font=("TITRE BOLD", 25, "bold"), bg="white", fg="green", padx=10, pady=10)
        title.place(x=0, y=20, relwidth=1)

        Button(self.root, text="SECURITY", command=self.login_security, cursor='hand2', bg='skyblue', font=("Arial", 14)).place(x=70, y=110)
        
        # Pass username to popup via lambda
        Button(self.root, text="ADD ITEM", command=lambda: self.itemadd_popup(self.username), cursor='hand2', bg='skyblue', font=("Arial", 14)).place(x=210, y=110)

        Button(self.root, text="GRN", command=lambda: self.grn_popup(self.username), cursor='hand2', bg='skyblue', font=("Arial", 14)).place(x=350, y=110)


        # Main Window Clock Labels
        self.clock = Label(self.root, text="", font=("TITRE BOLD", 12, "bold"), bg="lightblue", fg="black")
        self.clock.place(x=880, y=0, width=120, height=20)

        self.date = Label(self.root, text="", font=("TITRE BOLD", 12, "bold"), bg="lightblue", fg="black")
        self.date.place(x=0, y=0, width=120, height=20)

        self.display_username()
        self.update_clock(self.clock, self.date) # Start the main clock

    def display_username(self):
        label_username = Label(self.root, text=f"Welcome, {self.username}!", font=("Arial", 12), bg="lightblue")
        label_username.place(x=720, y=0, height=18)
        print(f"Logged in as: {self.username}")

    # REUSABLE CLOCK FUNCTION
    def update_clock(self, clock_label, date_label):
        if clock_label.winfo_exists() and date_label.winfo_exists():
            time_string = time.strftime("%I:%M:%S %p")
            date_string = time.strftime("%d-%m-%Y")
            clock_label.config(text=time_string)
            date_label.config(text=date_string)
            # Schedule update on the specific label
            clock_label.after(1000, lambda: self.update_clock(clock_label, date_label))

    # --- Security Logic ---
    def login_security(self):
        self.login_win = Toplevel(self.root)
        self.login_win.title("Log")
        self.login_win.geometry("300x180+400+350")
        self.login_win.config(bg="lightgray")

        Label(self.login_win, text="Username:", bg="lightgray").pack(pady=(10, 2))
        self.entry_user = Entry(self.login_win)
        self.entry_user.pack()
        self.entry_user.focus()

        Label(self.login_win, text="Password:", bg="lightgray").pack(pady=(10, 2))
        self.entry_pass = Entry(self.login_win, show="*")
        self.entry_pass.pack()

        Button(self.login_win, text="Login", command=self.verify_security_login).pack(pady=15)

    def verify_security_login(self):
        u, p = self.entry_user.get(), self.entry_pass.get()
        try:
            connection = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            cursor = connection.cursor()
            cursor.execute("SELECT password FROM login WHERE user=%s", (u,))
            result = cursor.fetchone()
            if result and bcrypt.checkpw(p.encode('utf-8'), result[0].encode('utf-8')):
                self.login_win.destroy()
                self.open_registration_window() 
            else:
                messagebox.showerror("Error", "Invalid Credentials")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def open_registration_window(self):
        self.reg_win = Toplevel(self.root)
        self.reg_win.title("Create New User")
        self.reg_win.geometry("400x400")
        Label(self.reg_win, text="New Username:").pack(pady=5)
        self.new_user = Entry(self.reg_win); self.new_user.pack()
        Label(self.reg_win, text="New Password:").pack(pady=5)
        self.new_pass = Entry(self.reg_win, show="*"); self.new_pass.pack()
        Button(self.reg_win, text="Save User", command=self.save_new_user).pack(pady=20)

    def save_new_user(self):
        u, p = self.new_user.get(), self.new_pass.get()
        hashed_p = bcrypt.hashpw(p.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        try:
            con = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            cur = con.cursor()
            cur.execute("INSERT INTO login (user, password) VALUES (%s, %s)", (u, hashed_p))
            con.commit()
            messagebox.showinfo("Success", "User Created")
            self.reg_win.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # --- Add Item Popup ---
    def itemadd_popup(self, username):
        from tkinter import ttk
        import tkinter as tk
        from tkinter import ttk, messagebox
        self.additem_win = Toplevel(self.root)
        self.additem_win.title("Add Item")
        self.additem_win.geometry("1000x600+80+80")
        self.additem_win.config(bg="lightblue")

        self.var_item = StringVar()
        self.var_date = StringVar()
        self.var_date.set(datetime.datetime.now().date())

        # Popup Clock Labels
        pop_clock = Label(self.additem_win, text="", font=("TITRE BOLD", 12, "bold"), bg="lightblue", fg="black")
        pop_clock.place(x=880, y=0, width=120, height=20)
        pop_date = Label(self.additem_win, text="", font=("TITRE BOLD", 12, "bold"), bg="lightblue", fg="black")
        pop_date.place(x=0, y=0, width=120, height=20)

        # Start clock for THIS popup
        self.update_clock(pop_clock, pop_date)

        title = Label(self.additem_win, text="" , font=("TITRE BOLD", 25, "bold"), bg="white", fg="green")
        title.place(x=0, y=20, relwidth=1)

        Label(self.additem_win, text="Item name:", font=("Arial", 15), bg="lightblue").place(x=50, y=130)
        Entry(self.additem_win, font=("Arial", 15), textvariable=self.var_item).place(x=175, y=130)

        Label(self.additem_win, text="Description:", font=("time new roman", 15), bg="lightblue").place(x=50, y=250)
        self.text_description = Text(self.additem_win, font=("time new roman", 15), bg="white", wrap=WORD)
        self.text_description.place(x=175, y=250, width=225, height=50)

        Label(self.additem_win, text="Add date:", font=("time new roman", 15), bg="lightblue").place(x=50, y=350)    
        Entry(self.additem_win, font=("time new roman", 15),textvariable=self.var_date, bg="white").place(x=175, y=350)



         # Display Invoice Items
        self.tree = ttk.Treeview(self.additem_win, columns=("Item Name","Description", "Add Date"), show="headings")
        self.tree.heading("Item Name", text="Item Name")
        self.tree.heading("Description", text="Description")
        self.tree.heading("Add Date", text="Add Date")
        
        

        self.tree.column("Item Name", width=130, anchor=tk.CENTER)
        self.tree.column("Description", width=50, anchor=tk.CENTER)
        self.tree.column("Add Date", width=50, anchor=tk.CENTER)
        
        
        self.tree.place(x=440, y=130, width=560, height=500)

        Button(self.additem_win, text="Add to Invoice", command=self.add_list, font=("Arial", 15), bg="gray",cursor="hand2").place(x=80, y=400)
        

        Button(self.additem_win, text="Save", command=self.save, font=("Arial", 15), bg="gray",cursor="hand2").place(x=300, y=400,height=40, width=100)

        delete_button = tk.Button(self.additem_win, text="Delete Selected", command=self.delete_selected, font=("Arial", 12), bg="red", fg="white", cursor="hand2")
        delete_button.place(x=80, y=500)

    

    def add_list(self):
        if self.var_item.get() == "" or self.var_date.get() == "" :
            messagebox.showerror("Error", "All fields are required", parent=self.root)
        else:
            items=self.var_item.get()
            description=self.text_description.get("1.0", "end-1c")
            date=self.var_date.get()
            self.tree.insert('', 'end', values=(items, description, date))
            self.var_item.set("")
            self.text_description.delete("1.0", "end")

        
    

    def save(self):
            try:
            # Establishing database connection
                con = pymysql.connect(host="localhost", user="root", password="#@19is16Pro", database="nilbima")
                cur = con.cursor()

            # Iterate over all treeview items
                for row in self.tree.get_children():
                    item_data = self.tree.item(row, 'values')
                    item = item_data[0]
                    description = item_data[1]
                    date = item_data[2]
                   

                # Check if drugname (item) exists in the alldrug table
                    cur.execute("SELECT COUNT(*) FROM mainstock WHERE itemname=%s", (item,))
                    exists = cur.fetchone()[0]
                   

                if exists == 0:
                    

                # Insert data into the mainstock table
                    cur.execute("INSERT INTO mainstock (itemname, itemdetail, adddate) VALUES ( %s, %s, %s)",
                    (item, description, date))


                    con.commit()
                    messagebox.showinfo("Success", "Data saved successfully to the database", parent=self.root)


                else:
                    messagebox.showerror("Error", "Item already exists in the database", parent=self.root)

            # Commit the transaction
                

            except Exception as e:
                messagebox.showerror("Error", f"Error saving data: {str(e)}", parent=self.root)

            finally:
            # Closing the connection
                if con:
                    con.close()

    def delete_selected(self):
        # Get selected item
        selected_item = self.tree.selection()
        if selected_item:
            # Delete the selected item from Treeview
            self.tree.delete(selected_item)           
        
    #----GRNpopup function----#
    def grn_popup(self,username):
        from tkinter import ttk
        import tkinter as tk
        from tkinter import ttk, messagebox
        self.grn_win = Toplevel(self.root)
        self.grn_win.title("Add Item")
        self.grn_win.geometry("1000x600+80+80")
        self.grn_win.config(bg="lightblue")
         
        # Define variables
        self.var_supplier = StringVar()
        self.var_itemname = StringVar()
        self.var_date = StringVar()
        self.var_date.set(datetime.datetime.now().date())
        self.var_quantity = IntVar()
        self.var_Retail_price = DoubleVar()
        self.var_wholesale_price = DoubleVar()
        self.var_total_cost = DoubleVar()
        self.var_grn=IntVar()
        self.var_negn=IntVar()

        self.load_next_grn_number()
        self.total_price = []
        self.invoice_items = []

        


        pop_clock = Label(self.grn_win, text="", font=("TITRE BOLD", 12, "bold"), bg="lightblue", fg="black")
        pop_clock.place(x=880, y=0, width=120, height=20)
        pop_date = Label(self.grn_win, text="", font=("TITRE BOLD", 12, "bold"), bg="lightblue", fg="black")
        pop_date.place(x=0, y=0, width=120, height=20)

        # Start clock for THIS popup
        self.update_clock(pop_clock, pop_date)

        title = Label(self.grn_win, text="" , font=("TITRE BOLD", 25, "bold"), bg="white", fg="green")
        title.place(x=0, y=20, relwidth=1)

        self.grn_value = Label(self.grn_win, textvariable=self.var_grn, font=("time", 15), bg="lightblue", fg="black", padx=10, pady=10)
        self.grn_value.place(x=400, y=90, width=200, height=30)
        
        #supplier details
        Label(self.grn_win, text="Supplier Name:", font=("Arial", 15), bg="lightblue").place(x=10, y=100)
        self.supplier_cb = ttk.Combobox(self.grn_win, textvariable=self.var_supplier, font=("TITRE BOLD", 15), postcommand=self.search_supplier)
        self.supplier_cb.place(x=200, y=100, width=230, height=30)

        Label(self.grn_win, text="Item Name:", font=("Arial", 15), bg="lightblue").place(x=10, y=150)
        self.entry_drugname = Entry(self.grn_win, textvariable=self.var_itemname, font=("Arial", 15), bg="white")
        self.entry_drugname.place(x=200, y=150)
        self.entry_drugname.bind("<KeyRelease>", self.suggest_itemname)
        self.entry_drugname.bind("<Down>", self.move_focus_to_listbox)


        # Listbox for drug suggestions
        self.listbox = Listbox(self.grn_win)
        self.listbox.place(x=200, y=180, width=231, height=50)
        self.listbox.bind("<Return>", self.select_suggestion)
        self.listbox.bind("<Up>", self.on_arrow_key)
        self.listbox.bind("<Down>", self.on_arrow_key)

        Label(self.grn_win, text="Add date:", font=("Arial", 15), bg="lightblue").place(x=10, y=250)
        Entry(self.grn_win, textvariable=self.var_date ,font=("Arial", 15), bg="white").place(x=200, y=250)

        Label(self.grn_win, text="Quantity:", font=("Arial", 15), bg="lightblue").place(x=10, y=300)
        Entry(self.grn_win, textvariable=self.var_quantity, font=("Arial", 15), bg="white").place(x=200, y=300)

        Label(self.grn_win, text="Retail price:", font=("Arial", 15), bg="lightblue").place(x=10, y=350)
        Entry(self.grn_win, textvariable=self.var_Retail_price, font=("Arial", 15), bg="white").place(x=200, y=350)

        Label(self.grn_win, text="Wholesale Price:", font=("Arial", 15), bg="lightblue").place(x=10, y=400)
        Entry(self.grn_win, textvariable=self.var_wholesale_price, font=("Arial", 15), bg="white").place(x=200, y=400)

        Label(self.grn_win, text="Total Cost:", font=("Arial", 15), bg="lightblue").place(x=10, y=450)
        Entry(self.grn_win, textvariable=self.var_total_cost, font=("Arial", 15), bg="white").place(x=200, y=450)

        # Add to Invoice Button
        Button(self.grn_win, text="Add to Invoice", command=self.add_to_invoice, font=("Arial", 15), bg="gray",cursor="hand2").place(x=50, y=550)
         # Save GRN Button
        Button(self.grn_win, text="Save GRN", command=self.save_grn_and_update_stock, font=("Arial", 15), bg="green",cursor="hand2").place(x=250, y=550)
        #delete selected 
        delete_button = tk.Button(self.grn_win, text="Delete Selected", command=self.delete_selected, font=("Arial", 12), bg="red", fg="white", cursor="hand2")
        delete_button.place(x=450, y=550)

        # Display Invoice Items
        self.tree = ttk.Treeview(self.grn_win, columns=("item", "Quantity", "Retail Price", "Wholesale Price", "Total"), show="headings")
        self.tree.heading("item", text="Item Name")
        self.tree.heading("Quantity", text="Quantity")
        self.tree.heading("Retail Price", text="Retail Price")
        self.tree.heading("Wholesale Price", text="Wholesale Price")
        self.tree.heading("Total", text="Total Price")

        self.tree.column("item", width=130, anchor=tk.W)
        self.tree.column("Quantity", width=50, anchor=tk.CENTER)
        self.tree.column("Retail Price", width=70, anchor=tk.CENTER)
        self.tree.column("Wholesale Price", width=80, anchor=tk.CENTER)
        self.tree.column("Total", width=60, anchor=tk.CENTER)
        self.tree.place(x=460, y=130, width=500, height=400)


    def add_to_invoice(self):
        item_name = self.var_itemname.get()
        
        Retail_price = float(self.var_Retail_price.get())
        wholesale_price = float(self.var_wholesale_price.get())
        supplier = self.var_supplier.get()
        
        

    
    
        quantity=int(self.var_quantity.get())
        total_price = quantity * wholesale_price
        self.total_price.append(total_price)
        total_cost = round(sum(self.total_price), 2)
        self.var_total_cost.set(total_cost)
        formatted_total_price = "{:.2f}".format(total_price)
        self.invoice_items.append((supplier, item_name, quantity, Retail_price, wholesale_price, total_price))
        self.tree.insert('', 'end', values=(item_name,  quantity, Retail_price, wholesale_price, formatted_total_price))
        print(self.invoice_items)
        self.var_quantity.set(0)
        self.var_Retail_price.set(0.0)
        self.var_wholesale_price.set(0.0)
        self.var_itemname.set('')


    def load_next_grn_number(self):
        connection = pymysql.connect(host="localhost", user="root", password="#@19is16Pro", database="nilbima")
        cursor = connection.cursor()
        cursor.execute("SELECT MAX(grnno) FROM grntable")
        last_grn = cursor.fetchone()[0]
        if last_grn is None:
            next_grn = 1
        else:
            next_grn = last_grn + 1
        formatted_grn = f"GRN-{next_grn}"
        self.var_negn.set(next_grn)
        self.var_grn.set(formatted_grn)
        connection.close()
    
    def delete_selected(self):
        # Get selected item
        selected_item = self.tree.selection()
        if selected_item:
            # Delete the selected item from Treeview
            self.tree.delete(selected_item)


    def search_supplier(self):
        suppliers = self.fetch_from_db("SELECT supplier FROM suppliers")
        self.supplier_cb["values"] = suppliers

    def fetch_from_db(self, query, params=None):
        connection = pymysql.connect(host="localhost", user="root", password="#@19is16Pro", database="nilbima")
        cursor = connection.cursor()
        cursor.execute(query, params or ())
        result = cursor.fetchall()
        connection.close()
        return [item[0] for item in result]

    def suggest_itemname(self, event):
        user_input = self.var_itemname.get()
        self.listbox.delete(0, END)
        if user_input == "":
            return
        connection = pymysql.connect(host="localhost", user="root", password="#@19is16Pro", database="nilbima")
        cursor = connection.cursor()
        cursor.execute("SELECT itemname FROM mainstock WHERE itemname LIKE %s", (user_input + '%',))
        suggestions = cursor.fetchall()
        connection.close()
        for suggestion in suggestions:
            self.listbox.insert(END, suggestion[0])
        self.listbox.place(x=200, y=180, width=231, height=50)

    def select_suggestion(self, event=None):
        try:
            selected_item = self.listbox.get(self.listbox.curselection())
            self.var_itemname.set(selected_item)
        except TclError:
            pass
    
    def on_arrow_key(self, event):
        if event.keysym == 'Up':
            index = self.listbox.curselection()[0]
            if index > 0:
                self.listbox.selection_clear(0, END)
                self.listbox.selection_set(index - 1)
                self.listbox.activate(index - 1)
        elif event.keysym == 'Down':
            index = self.listbox.curselection()[0]
            if index < self.listbox.size() - 1:
                self.listbox.selection_clear(0, END)
                self.listbox.selection_set(index + 1)
                self.listbox.activate(index + 1)

    def move_focus_to_listbox(self, event=None):
        if self.listbox.size() > 0:
            self.listbox.focus()
            self.listbox.selection_set(0)
            self.listbox.activate(0)

    def save_grn_and_update_stock(self):
        # 1. Validation check before opening connection
        if not self.invoice_items:
            messagebox.showerror("Error", "No items added to the list!")
            return

        connection = None
        try:
            # Establish connection
            connection = pymysql.connect(
                host="localhost", 
                user="root", 
                password="#@19is16Pro", 
                database="nilbima",
                autocommit=False
            )
            cursor = connection.cursor()

            # --- DYNAMIC STRUCTURE FIX ---
            sample_item = self.invoice_items[0]
            name_idx, qty_idx, retail_idx, wholesale_idx = 1, 2, 3, 4
            
            for i, val in enumerate(sample_item):
                val_str = str(val).strip()
                if i == 1 or (i == 0 and not val_str.replace('.','',1).isdigit()):
                    if 'rohan' not in val_str.lower(): 
                        name_idx = i

            # Create comma-separated summary values for grntable
            item_names = ", ".join([str(item[name_idx]).strip() for item in self.invoice_items])  
            quantity = ", ".join([str(item[qty_idx]).strip() for item in self.invoice_items])        
            Retail_price = ",".join([str(item[retail_idx]).strip() for item in self.invoice_items])
            wholesale_price = ",".join([str(item[wholesale_idx]).strip() for item in self.invoice_items])
            
            # --- TASK 1: Insert into grntable ---
            query_grn = """
            INSERT INTO grntable (itemsname, item, grndate, retailprice, wholesaleprice, quantity, supplier, totalcost) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query_grn, (
                item_names,
                len(self.invoice_items),         
                self.var_date.get(),
                Retail_price,
                wholesale_price,
                quantity,
                self.var_supplier.get(),
                self.var_total_cost.get()   
            ))
            
            grn_no = cursor.lastrowid 

            # --- TASKS 2 & 3: Loop through each item ---
            for item in self.invoice_items:
                item_name = str(item[name_idx]).strip()
                qty_received = float(str(item[qty_idx]).strip())
                r_price = float(str(item[retail_idx]).strip())
                w_price = float(str(item[wholesale_idx]).strip())
                item_detail = str(item[5]).strip() if len(item) > 5 else "" 
                
                # 💰 ඉන්වොයිස් එකේ අදාළ අයිතමයේ මුළු වටිනාකම (Quantity x Wholesale Price)
                item_total_cost = qty_received * w_price
                
                # A. mainstock ටේබල් එක අප්ඩේට් කිරීම හෝ අලුතින් ඇතුලත් කිරීම
                # (UNIQUE කර ඇති නිසා නම සමාන නම් කෙලින්ම stock එක එකතු වේ)
                query_upsert = """
                INSERT INTO mainstock (itemname, itemdetail, price, stock, adddate)
                VALUES (%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE 
                    stock = stock + VALUES(stock),
                    price = VALUES(price)
                """
                cursor.execute(query_upsert, (item_name, item_detail, r_price, qty_received, self.var_date.get()))
                
                # itemdetail එකට ලින්ක් කරන්න අවශ්‍ය itemid එක ලබා ගැනීම
                cursor.execute("SELECT itemid FROM mainstock WHERE itemname = %s", (item_name,))
                item_id = cursor.fetchone()[0]
                
                # B. itemdetail ටේබල් එකට දත්ත සහ totalcost එක එකතු කිරීම
                # ⚠️ ඔයාගේ MySQL itemdetail ටේබල් එකේ 'totalcost' කොලම් එකේ නම මේ ආකාරයටම තියෙන්න ඕනෙ
                query_item_detail = """
                INSERT INTO itemdetail (itemid, grnno, retailprice, wholesaleprice, qty) 
                VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(query_item_detail, (item_id, grn_no, r_price, w_price, qty_received))

            # ඔක්කොම සාර්ථක නම් ඩේටාබේස් එකට සේව් කරන්න
            connection.commit()
            messagebox.showinfo("Success", "GRN saved, Stock updated, and Item Details with Total Cost tracked successfully!")
            
        except Exception as e:
            if connection:
                connection.rollback()
            messagebox.showerror("Database Error", f"Transaction failed and rolled back.\nError: {str(e)}")
            
        finally:
            if connection:
                connection.close()
if __name__ == "__main__":
    root = Tk()
    app = Admin(root, "username")
    root.mainloop()