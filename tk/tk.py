import re
from tkinter import *
from docx import Document


class MaYuan:

    def __init__(self):
        self.window = Tk()
        self.configure()
        self.path = "/home/sayno/Downloads/马原题目.docx"
        self.frame = Frame(self.window)
        self.frame2 = Frame(self.window)
        self.back = self.frame
        self.generator = self.get_docx()
        self.layout(*next(self.generator))

    def configure(self):
        # self.window.configure(bg="#000000")
        screenwidth = self.window.winfo_screenwidth()
        screenheight = self.window.winfo_screenheight()
        w = 800
        h = 500
        x = (screenwidth - w) / 2
        y = (screenheight - h) / 2
        self.window.geometry(f"{w}x{h}+{int(x)}+{int(y)}")
        self.window.title("马克思主义原理题库")

    def run(self):
        self.window.mainloop()

    def layout(self, question, selects, answer):
        select_length = len(selects)
        if select_length != 0:
            frame, self.back = self.frame, self.frame2
        else:
            frame, self.back = self.frame2, self.frame

        def get():
            result = var.get()
            if result == answer:
                answer_label.config(text=f"正确答案是{answer}，你答对了😉")
            elif result == "None":
                answer_label.config(text=f"请选择输入正确答案，{result}")
            else:
                answer_label.config(text=f"正确答案是{answer}，你选择了{var.get()}，很遗憾")

        def get_bool():
            choose_answer = ""
            for i in bool_var:
                if bool_var[i].get():
                    choose_answer += var_list[i]
            print(choose_answer)
            if choose_answer == answer:
                answer_label.config(text=f"正确答案是{answer}，你答对了😉")
            else:
                answer_label.config(text=f"正确答案是{answer}，你选择了{choose_answer}，很遗憾")

        var = StringVar()
        var.set(None)

        prefix = ""
        if len(answer) > 1:
            prefix = "(多选)"
        var_list = ["对", "错"]
        if select_length == 4:
            var_list = ["A", "B", "C", "D"]
        q_label = Label(frame, text=prefix + question, wraplength=800,
                        justify="left", font=("Helvetic 10"), anchor="nw")
        q_label.grid(row=0, column=0, columnspan=2, sticky=E + N + S + W)
        # q_label.pack(side=TOP)
        bool_var = {}
        if len(selects) != 0:
            if len(answer) > 1:
                for index, select in enumerate(selects):
                    bool_var[index] = BooleanVar()
                    Checkbutton(frame, text=var_list[index], variable=bool_var[index],
                                font=("Helvetic 10"), anchor="nw", width=5).grid(row=index + 1, column=0, sticky=N + S + W + E)
                    Label(frame, text=select, justify="left", anchor="w",
                          wraplength=800, font=("Helvetic 10")).grid(row=index + 1, column=1, sticky=W + E + N + S)
                check_button = Button(frame, text="提交", command=get_bool)
                check_button.grid(row=select_length + 1, column=0, sticky=W + E + N + S)
            else:
                for index, select in enumerate(selects):
                    Radiobutton(frame, text=var_list[index], variable=var, value=var_list[index],
                                font=("Helvetic 10"), anchor="nw", width=5).grid(row=index + 1, column=0, sticky=N + S + W + E)
                    Label(frame, text=select, justify="left", anchor="w",
                          wraplength=800, font=("Helvetic 10")).grid(row=index + 1, column=1, sticky=W + E + N + S)
                check_button = Button(frame, text="提交", command=get)
                check_button.grid(row=select_length + 1, column=0, sticky=W + E + N + S)
        elif len(selects) == 0:
            select_length += 2
            for index, select in enumerate(var_list):
                Radiobutton(frame, text=var_list[index], variable=var, value=var_list[index],
                            font=("Helvetic 10"), anchor="nw", width=5).grid(row=index + 1, column=0, sticky=N + S + W + E)
            check_button = Button(frame, text="提交", command=get)
            check_button.grid(row=select_length + 1, column=0, sticky=W + E + N + S)
        # if not check_button.winfo_exists():
        #     check_button = Button(frame, text="提交", command=get)
        #     check_button.grid(row=select_length + 1, column=0, sticky=W + E + N + S)

        next_button = Button(frame, text="下一题目", command=self.next_title)
        next_button.grid(row=select_length + 1, column=1, sticky=W + N + S)
        answer_label = Label(frame, anchor="nw", font=("Helvetic 10"))
        answer_label.grid(row=select_length + 2, column=0, columnspan=2, sticky=W + E + N + S)
        self.back.forget()
        frame.pack()

    def get_docx(self):
        questions = []
        document = Document(self.path)
        text = "".join([paragraph.text for paragraph in document.paragraphs])
        answers = re.findall('正确答案: ([对错]|[A-D]*)', text)
        questions = re.split('正确答案: (?:[A-D对错]*)', text)
        titles = []
        selects = []
        count = 0
        for question in questions:
            count += 1
            target = re.split("(?:[A-D]:)", question)
            titles.append(target[:1])
            selects.append(list(target[1:]))
        print(count)
        titles = [re.sub("（）", "_____", title[0]) for title in titles][:-1]
        selects = selects[:-1]
        for title, select, answer in zip(titles, selects, answers):
            yield title, select, answer

    def next_title(self):
        try:
            self.layout(*(next(self.generator)))
        except StopIteration as e:
            print("End")


if __name__ == '__main__':
    my = MaYuan()
    my.run()
