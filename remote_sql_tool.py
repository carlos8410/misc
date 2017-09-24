# Write a GUI-based program that provides several Entry fields for login info, 
# a button and a text output.
# 
# When the Send button is clicked, it will make a MySQL query using the login info
# If the request succeed, the text output should show the formated query data
# Otherwise it should show the error information



from tkinter import ttk
import tkinter 
from tkinter.filedialog import asksaveasfile
import urllib.request
import mysql.connector

ALL = 'news'

class Application:
    def __init__(self, root):
        self.root = root
        self.output = ''
        self.root.title('Blocking Command Demo')
        self.init_widgets()
            
            
    def init_widgets(self):
        ttk.Label(self.root, text="Host").grid(row=0, column=0, sticky='w')
        ttk.Label(self.root, text="Port").grid(row=1, column=0, sticky='w')        
        ttk.Label(self.root, text="Username").grid(row=2, column=0, sticky='w')
        ttk.Label(self.root, text="Password").grid(row=3, column=0, sticky='w')
        ttk.Label(self.root, text="SQL query").grid(row=4, column=0, sticky='w')
 
        self.e1 = ttk.Entry(self.root, width=40)
        self.e2 = ttk.Entry(self.root, width=40)
        self.e3 = ttk.Entry(self.root, width=40)
        self.e4 = ttk.Entry(self.root, width=40)
        self.e5 = ttk.Entry(self.root, width=40)
        
        self.e1.grid(row=0, column=1, sticky='e')                
        self.e2.grid(row=1, column=1, sticky='e')
        self.e3.grid(row=2, column=1, sticky='e')
        self.e4.grid(row=3, column=1, sticky='e')
        self.e5.grid(row=4, column=1, sticky='e')

        self.btn = ttk.Button(self.root, command=self.send_request, text='Send', width=8)
        self.btn.grid(column=0, row=5, sticky='w')
        self.btn = ttk.Button(self.root, command=self.file_save, text='Export', width=8)
        self.btn.grid(column=0, row=5, sticky='e')
                
        self.txt = tkinter.Text(self.root, width=80, height=20)
        self.txt.grid(column=0, row=6, columnspan=2, sticky='nwes')
        sb = ttk.Scrollbar(command=self.txt.yview, orient='vertical')
        sb.grid(column=2, row=6, sticky='ns')
        self.txt['yscrollcommand'] = sb.set
        

    
    def output_to_vertical_format(self, cursor):
        widths = []
        tavnit = '|'
        separator = '+' 
        formated_output = ''

        fields = [col[0] for col in cursor.description]
        data_output = cursor.fetchall()
        
        for cd in cursor.description:
            widths.append(max(cd[2] if cd[2] else 0, len(cd[0])))

        for w in widths:
            tavnit += " %-"+"%ss |" % (w,)
            separator += '-'*w + '--+'
        
        separator += '\n'
        header = separator \
            + tavnit % tuple(fields) + '\n' \
            + separator
    
        formated_output += header
        
        for row in data_output:
            formated_output += tavnit % row + '\n'
        formated_output += separator
        
        return formated_output

    def file_save(self):
        fout = asksaveasfile(mode = 'w', defaultextension=".txt")
        if fout:
            fout.write(self.output)
            fout.close()

    def send_request(self):
        host = self.e1.get()
        port = self.e2.get()
        username = self.e3.get()
        password = self.e4.get()
        sql = self.e5.get()
        has_error = False

        config = {
                    'user': username,
                    'password': password,
                    'host': host,
                    'port': port
                }

        config = {
            'user': 'root',
            'password': 'root',
            'host': 'localhost',
            'port': '3306'}
        sql = 'SELECT * FROM master_dev.topo_comp_relationships limit 1'

        try:
            db = mysql.connector.connect(**config)
            cur = db.cursor()
        except mysql.connector.Error as err:
            has_error = True
            error_msg = "MySQL connection error to {0}".format(host)
        else:        
            try:
                cur.execute(sql)
                formated_data = self.output_to_vertical_format(cur)
            except Exception as e:
                has_error = True
                error_msg = "Error when getting data: %s" % e
            finally:
                db.close()      
        
        if has_error:
            self.output = error_msg
        else:
            self.output = formated_data
        self.txt.delete(0.0, tkinter.END)    
        self.txt.insert(tkinter.INSERT, self.output)


if __name__ == '__main__':
    root = tkinter.Tk()
    Application(root)
    root.mainloop()        
