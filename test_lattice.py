import lattice_analysis


class TestLattice:
    def general_test(self, filepath, ans):
        self.eomap = {'T': 0, 'E': 1, 'O': 2, 'B': 3}
        ans_dic = self.counting_ans(ans)

        solver = lattice_analysis.Lattice(filepath)
        solver.fix_solve()
        ret_dic = self.counting_ans(solver.lattice)

        assert len(ans_dic) == len(ret_dic)
        for key in ans_dic.keys():
            assert key in ret_dic and ret_dic[key] == ans_dic[key]

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

        self.general_test('TestCases/Test1.py', ans1)

    def test2(self):
        ans2 = [['E', 'B', 'B'],
                ['T', 'B', 'B'],
                ['T', 'B', 'B'],
                ['T', 'B', 'B'],
                ['T', 'B', 'B'],
                ['T', 'E', 'T']]

        self.general_test('TestCases/Test2.py', ans2)

    def test3(self):
        ans2 = [['E'],
                ['T'],
                ['T'],
                ['O'],
                ['T']]

        self.general_test('TestCases/Test3.py', ans2)
    
    def test4(self):
        ans2 = [['O', 'B', 'B', 'B'],
                ['E', 'B', 'B', 'B'],
                ['E', 'O', 'O', 'O']]

        self.general_test('TestCases/Test3.py', ans2)
