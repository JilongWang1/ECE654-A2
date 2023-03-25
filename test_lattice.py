import lattice_analysis


class TestLattice:
    def general_test(self, filepath, ans):
        self.eomap = {'T': 0, 'E': 1, 'O': 2, 'B': 3}
        ans_dic = self.counting_ans(ans)

        solver = lattice_analysis.Lattice(filepath)
        solver.fix_solve()
        ret_dic = self.counting_ans(solver.lattice)

        if len(ans_dic) != len(ret_dic):
            return False

        for key in ans_dic.keys():
            if key in ret_dic and ret_dic[key] == ans_dic[key]:
                continue
            else:
                return False
        return True

    def counting_ans(self, ans):
        ans_dic = {}
        for ans_line in ans:
            line_dic = [0] * 4
            for c in ans_line:
                line_dic[self.eomap[c]] += 1
            line_dic = tuple(line_dic)

            if line_dic in ans_dic:
                ans_dic[line_dic] += 1
            else:
                ans_dic[line_dic] = 1

        return ans_dic

    def test1(self):
        ans1 = [['E', 'B'],
                ['O', 'O'],
                ['E', 'O']]

        if self.general_test('TestCases/Test1.py', ans1):
            print('test1 passed')
        else:
            print('test1 failed')

    def test2(self):
        ans2 = [['E', 'B', 'B'],
                ['T', 'B', 'B'],
                ['T', 'B', 'B'],
                ['T', 'B', 'B'],
                ['T', 'B', 'B'],
                ['T', 'E', 'T']]

        if self.general_test('TestCases/Test2.py', ans2):
            print('test2 passed')
        else:
            print('test2 failed')

    def test3(self):
        ans2 = [['E'],
                ['T'],
                ['T'],
                ['O'],
                ['T']]

        if self.general_test('TestCases/Test3.py', ans2):
            print('test3 passed')
        else:
            print('test3 failed')
    
    def test4(self):
        ans2 = [['O', 'B', 'B', 'B'],
                ['E', 'B', 'B', 'B'],
                ['E', 'O', 'O', 'O']]

        if self.general_test('TestCases/Test3.py', ans2):
            print('test4 passed')
        else:
            print('test4 failed')


test = TestLattice()
test.test1()
test.test2()
test.test3()
test.test4()