from BuyScript import main_for_gui
import tkinter as tk


def gui():
    # 初始化窗口
    root = tk.Tk()
    # 设置标题
    root.title('抢购脚本')
    # 窗口大小
    root.geometry('600x300')
    tk.Label(root, text='第一版脚本，能不能用不知道', font=('Arial', 16)).pack()
    # 文本框
    tk.Label(root, text='商品id:', font=('Arial', 10)).place(x=110, y=60)
    entry1 = tk.Entry(root, width=40)
    entry1.place(x=200, y=60)
    tk.Label(root, text='抢购日期 格式：YYYY-MM-DD', font=('Arial', 10)).place(x=110, y=80)
    entry2 = tk.Entry(root, width=60)
    entry2.place(x=110, y=100)
    tk.Label(root, text='抢购时间 格式：HH:MM:SS', font=('Arial', 10)).place(x=110, y=120)
    entry3 = tk.Entry(root, width=60)
    entry3.place(x=110, y=140)
    tk.Label(root, text='登录预留时间 单位：s', font=('Arial', 10)).place(x=110, y=160)
    entry4 = tk.Entry(root, width=20)
    entry4.place(x=110, y=180)
    is_qr = tk.IntVar()
    tk.Checkbutton(master=root, text='是否扫码登录',
                   variable=is_qr, onvalue=1, offvalue=0,).place(x=110, y=200)
    is_qg = tk.IntVar()
    tk.Checkbutton(master=root, text='该商品是否需要抢购',
                   variable=is_qg, onvalue=1, offvalue=0,).place(x=110, y=220)

    def execute():
        # 参数
        (eid, buytime) = ('', '')
        delay = 0
        eid = entry1.get()
        date = entry2.get()
        time = entry3.get()
        delay = int(entry4.get())
        buytime = date + ' ' + time
        print('id: ' + eid + ' buytime: ' + buytime)
        root.destroy()
        main_for_gui(eid, buytime, delay, is_qr, is_qg)

    tk.Button(root, text='开整！', command=execute).place(x=250, y=240)
    root.mainloop()


if __name__ == '__main__':
    gui()
