# -*- coding: utf8 -*-
import random
import itertools


class abs_code:
    def __init__(self, n):
        i = 0
        print("Enter binary code.")
        while i == 0:
            self.initial_m = str(input())
            self.initial_m = list(self.initial_m)
            if len(self.initial_m) == n:
                if [x for x in self.initial_m if x != "0" and x != "1"]:
                    print("Incorrect input. Try again.")
                else:
                    print("Correct input.")
                    for i in range(0,len(self.initial_m)):
                        self.initial_m[i] = int(self.initial_m[i])
                        # i = 1
            else:
                print("Incorrect input. Try again.")
        self.m_old = []
        self.m_old.extend(self.initial_m)

    def correction(self):
        i = random.randint(0, 6)
        if self.initial_m[i] == 1:
            self.initial_m[i] = 0
        else:
            self.initial_m[i] = 1
        m = []
        m.extend(self.initial_m)
        return m

    def coding(self):
        pass

    def error_search(self):
        pass

    def name(self):
        pass

    def __repr__(self):
        return '-------------------------------------------------------------------------\n' \
               '{}\n' \
               '-------------------------------------------------------------------------\n' \
               'Initial binary code:        {}\n' \
               'Binary code:                {}\n' \
               'Binary code after transfer: {}\n' \
               'Restored binary code:       {}\n'.format(self.name(),
                                                         self.m_old,
                                                         self.coding(),
                                                         self.correction(),
                                                         self.error_search())


class loop_15_11(abs_code):

    def div(self, initial_m):
        # поиск единицы в m
        k = -1
        i = 0
        while k < 0:
            if initial_m[i] == 1:
                k = i
            elif i == 10:
                k = 15
            i = i + 1
        m = []
        if k != 15:
            # деление m на образующий полином
            m.extend(initial_m[k:k + 5])
            g = [1, 0, 0, 1, 1]
            k += 5
            while m[0] == 1:
                for i in range(0, 5):
                    if m[i] == g[i]:
                        m[i] = 0
                    else:
                        m[i] = 1
                while m[0] == 0 and k < 15:
                    del m[0]
                    m.append(initial_m[k])
                    k = k + 1
            del m[0]
        else:
            m.extend(initial_m[11:15])
        return m

    def coding(self):
        self.initial_m.extend([0, 0, 0, 0])
        m = []
        m = self.div(self.initial_m)
        # конкатенация
        for i in range(0, 4):
            self.initial_m[i + 11] = m[i]
        m = []
        m.extend(self.initial_m)
        return m

    def error_search(self):
        s = []
        s = self.div(self.initial_m)
        synd = [[1, 0, 0, 1], [1, 1, 0, 1], [1, 1, 1, 1], [1, 1, 1, 0], [0, 1, 1, 1], [1, 0, 1, 0], [0, 1, 0, 1],
                [1, 0, 1, 1], [1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 1], [1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0],
                [0, 0, 0, 1]]
        if s != [0, 0, 0, 0]:
            i = synd.index(s)
            if self.initial_m[i] == 0:
                self.initial_m[i] = 1
            else:
                self.initial_m[i] = 0
        m = []
        m.extend(self.initial_m)
        return m

    def name(self):
        return "Loop code (15,11)"


class loop_15_11_test(loop_15_11):

    def test(self, m, err_count, err_correct):
        err = self.error_search(m)
        m = []
        m.extend(err[0])
        n = 0
        err_count += err[1]
        for u in range(0, 15):
            if m[u] != self.initial_m[u]:
                n += 1
        if n == 0:
            err_correct += 1
        return err_count, err_correct

    def bit_correct(self, m, i):
        if m[i] == 1:
            m[i] = 0
        else:
            m[i] = 1
        return m

    def correction(self):
        m = []
        m.extend(self.initial_m)
        for err in range(1, 16):
            err_count = 0
            err_correct = 0
            if err == 1:
                print("\nTEST: " + str(err) + " error\n")
            else:
                print("\nTEST: " + str(err) + " errors\n")
            l = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
            mask = []
            mask.extend(list(itertools.combinations(l, err)))
            for i in range(0, len(mask)):
                mask[i] = list(mask[i])
                for j in range(0, len(mask[i])):
                    m = self.bit_correct(m, mask[i][j])
                err_list = self.test(m, err_count, err_correct)
                err_count = err_list[0]
                err_correct = err_list[1]
                m = []
                m.extend(self.initial_m)
            print("Correction ability: " + str(err_correct / len(mask) * 100) + "%\n"
                                                                                "    - Fixed errors: " + str(err_correct))
            print("Detecting ability: " + str(err_count / len(mask) * 100) + "%\n"
                                                                             "    - Detected errors: " + str(err_count))
        return m

    def error_search(self, m):
        s = []
        s = self.div(m)
        synd = [[1, 0, 0, 1], [1, 1, 0, 1], [1, 1, 1, 1], [1, 1, 1, 0], [0, 1, 1, 1], [1, 0, 1, 0], [0, 1, 0, 1],
                [1, 0, 1, 1], [1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 1], [1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0],
                [0, 0, 0, 1]]
        if s != [0, 0, 0, 0]:
            i = synd.index(s)
            if m[i] == 0:
                m[i] = 1
            else:
                m[i] = 0
            i = 1
        else:
            i = 0
        return [m, i]

    def __repr__(self):
        try:
            self.coding()
            self.correction()
        except:
            return '\nTest failed.\n'
        else:
            return '\nTest completed successfully.\n'


print("Check Loop code (15,11) by:\n"
              "     1 - Example\n"
              "     2 - Test\n"
              "0 - Exit")
s = str(input())
if s == "1":
    obj_m = loop_15_11(11)
    print(obj_m)
elif s == "2":
    obj_m = loop_15_11_test(11)
    print(obj_m)
elif s == "0":
    s = 0
else:
    print("Incorrect input. Try again.")