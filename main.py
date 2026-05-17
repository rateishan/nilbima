from tkinter import*
import pymysql
import bcrypt
from tkinter import messagebox
import time
from datetime import datetime, date
from admin import Admin



class adminpage:
    def __init__(self, root):
        self.root = root
        self.root.title("Login") 
        self.root.geometry("1000x600+80+80")
        self.root.config(bg="lightblue")
        self.var_username = StringVar()
        self.var_password = StringVar()




        title = Label(self.root, text="NILBIMA LANKA" , font=("TITRE BOLD", 25, "bold"), bg="white", fg="green", padx=10, pady=10)
        title.place(x=0, y=20, relwidth=1)
        
        self.clock = Label(self.root, text="", font=("TITRE BOLD", 12, "bold"),
                           bg="lightblue", fg="black", padx=10, pady=10, anchor="e")
        self.clock.place(x=900, y=0, width=110, height=20)

        self.date = Label(self.root, text="", font=("TITRE BOLD", 12, "bold"),
                          bg="lightblue", fg="black", padx=10, pady=10, anchor="e")
        self.date.place(x=0, y=0, width=100, height=20)

        self.start_clock(self.root, self.clock, self.date)
 
    def start_clock(self, parent, clock_label, date_label):
        def update_time():
            if not (clock_label.winfo_exists() and date_label.winfo_exists()):
                return
            clock_label.config(text=time.strftime("%I:%M:%S %p"))
            date_label.config(text=time.strftime("%d-%m-%Y"))
            # SAVE AS self.after_id
            self.after_id = parent.after(1000, update_time)
        update_time()

        Label(self.root, text="Username:", font=("Arial", 14),bg="lightblue").place(x=350,y=300)
        self.entry_username = Entry(self.root, textvariable=self.var_username, font=("Arial", 14))
        self.entry_username.place(x=490,y=300)
        self.entry_username.focus()

        # Password
        Label(self.root, text="Password:", font=("Arial", 14),bg="lightblue").place(x=350,y=395)
        self.entry_password = Entry(self.root, textvariable=self.var_password, show="*", font=("Arial", 14))
        self.entry_password.place(x=490,y=395)
        
        

        Button(self.root, text="Login", command=self.login, cursor='hand2', bg='skyblue', font=("Arial", 14)).place(x=570,y=490)

    def login(self):
            try:
                con = pymysql.connect(host="localhost", user="root", password="#@19is16Pro", database="nilbima")
                cur = con.cursor()
            
                # This is where 'result' is created
                cur.execute("SELECT password FROM mainlog WHERE username=%s", (self.var_username.get(),))
                result = cur.fetchone() 
                con.close()

                # --- This 'if' must be perfectly aligned under 'cur.execute' ---
                if result:
                    stored_hashed_password = result[0]
                    typed_password = self.var_password.get()
                    username = self.var_username.get()

                    if bcrypt.checkpw(typed_password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
                        messagebox.showinfo("Success", "Login Successful")
                        self.open_admin(username)
                    else:
                        messagebox.showerror("Error", "Incorrect password")
                else:
                    messagebox.showerror("Error", "Incorrect username")

            except Exception as e:
                messagebox.showerror("DB Error", f"Error: {str(e)}")
            # ... (Keep the rest of your error handling) ...
         
    def open_admin(self, username):
        # 1. Stop the clock timer properly
        if hasattr(self, 'after_id'):
            self.root.after_cancel(self.after_id)
        
        # 2. Destroy and switch
        self.root.destroy()
        
        main_root = Tk()
        self.app = Admin(main_root, username)
        main_root.mainloop()
       




  
# Run login window
if __name__ == "__main__":
    root = Tk()
    app = adminpage(root)
    root.mainloop()