import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkcalendar import *
import requests
from tkinter import messagebox
import json

window = tk.Tk()
window.title("Expense tracker")

global counter
global amount
global last_row_id
global amount_list

counter = 0
amount_list = []


#functions

def clear_fields_after_btn():
    amount_ent.delete(0, END)
    currency_ent.delete(0, END)
    cat_ent.delete(0, END)
    payment_ent.delete(0, END)
 
    
last_row_id = None  

def delete_last_row():
    global total
    global last_row_id

    if last_row_id:
        
        table.delete(last_row_id)




    
def usd_sum():
    global total
    global last_row_id
    global currency
    global amount

    # Convert amount to USD using the API
    convert_to = "USD"
    url = f"https://api.apilayer.com/fixer/convert?to={convert_to}&from={currency}&amount={amount}"

    payload = {}
    headers = {
       "apikey": "BYxSx5ORAl8MEw4UkyTyQPQoN0RT8Mx8"
    }


    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an exception for HTTP errors

    data = response.json()

    if data["success"]:
        result_value = data["result"]
    else:
        messagebox.showinfo("Conversion Failed", "Please try again or check the API response.")

 
    amount_list.append(result_value)

    total = sum(amount_list)
    formatted_result = round(total, 2)

   
     
    # Delete the last row
    delete_last_row()

    # Insert a new row with the converted value
    table.insert(parent="", index=counter, values=(formatted_result, "USD"))

    # Apply the "last_row" tag to the last row
    last_row_id = table.get_children()[-1]
    table.item(last_row_id, tags=("last_row",))

    # Configure the background color for the last row
    table.tag_configure("last_row", background="yellow")
    
    





def add_to_table ():
    global counter
    global amount
    global last_row_id
    global currency
    amount = amount_ent.get()
    currency = currency_ent.get()
    cateogry = cat_ent.get()
    payment = payment_ent.get()
    date = calen.get_date()
    

    

    if not amount or not currency or not cateogry or not payment or not date  :
        messagebox.showinfo("showinfo", "complete all fields please")

    else:  
        try:
           float_amount = float(amount)
           if float_amount <= 0  :
               messagebox.showinfo("error", "insert correct amount")
           else:
                
                table.insert(parent="", index=counter,values=(amount ,currency,cateogry,payment,date) )
                counter +=1
                


                usd_sum()
                clear_fields_after_btn()
                
                
               
        except ValueError:
           messagebox.showinfo("error", "insert correct amount")
        


          
#widgets
main_frame = tk.Frame(window)

#labels
amount_lab = tk.Label(main_frame, text="Amount", fg="black",font=("arial", 18))
currency_lab = tk.Label(main_frame, text="Currency", fg="black",font=("arial", 18))
cat_lab = tk.Label(main_frame, text="Category", fg="black",font=("arial", 18))
payment_lab = tk.Label(main_frame, text="Payment Method", fg="black",font=("arial", 18))
date_lab = tk.Label(main_frame, text="Date", fg="black",font=("arial", 18))
add_btn = tk.Button(main_frame,text="Add Expense",anchor=CENTER, width=15,height=1,font=("arial", 10,"bold"),command=add_to_table)

#entry
amount_ent = tk.Entry(main_frame,width=15 ,font=("arial", 15))
currency_ent = ttk.Combobox(main_frame,width=25,font=("arial", 10),values="EUR GBP  EGP USD")
cat_ent = ttk.Combobox(main_frame,width=25,font=("arial", 10),values="savings installment  rental food")
payment_ent = ttk.Combobox(main_frame,width=25,font=("arial", 10),values="VFcash Paypal Creditcard")
calen = DateEntry(main_frame,width=28)


#grid
main_frame.grid(row=0, column=0)
amount_lab.grid(row=0 ,column=0,padx=150, pady=10)
currency_lab.grid(row=1 , column=0,padx=50, pady=10)
cat_lab.grid(row=2 , column=0,padx=50, pady=10)
payment_lab.grid(row=3 , column=0,padx=50, pady=10)
date_lab.grid(row=4 , column=0,padx=50, pady=10)

amount_ent.grid(row=0 ,column=1,padx=50, pady=10)
currency_ent.grid(row=1 , column=1,padx=50, pady=10)
cat_ent.grid(row=2 , column=1,padx=50, pady=10)
payment_ent.grid(row=3 , column=1,padx=50, pady=10)

add_btn.grid(row=5 , column=1,padx=50, pady=10)
calen.grid(row=4 , column=1,padx=50, pady=10)


#table
table_frame = tk.Frame(window)
table = ttk.Treeview(table_frame, columns=('Amo', 'Curr','Cate','Pay', 'Dat'), show="headings")
table.heading('Amo', text='Amount')
table.heading('Curr', text='Currency')
table.heading('Cate', text='Category')
table.heading('Pay', text='Payment')
table.heading('Dat', text='Date')

columns = table["columns"]
for col in columns:
    table.column(col,anchor="center")

style = ttk.Style(table)
style.configure("Treeview.Heading", background="gray",relief="raised",rowheight=25,font=('Arial',14))

table_frame.grid(row=2, column=0,padx=10, pady=50)
table.pack(fill="both",expand=True)













window.mainloop()
