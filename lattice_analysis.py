import ast
import staticfg


class Lattice:
    def __init__(self, checking_path):
        cfg = staticfg.CFGBuilder().build_from_file('cfg', checking_path)
        self.entry = cfg.entryblock
        self.var_num = 0
        self.var = {}  # map from variable name to its index
        self.all_block = []  # list of all blocks
        self.blocks = {}  # map from block to its index
        self.counting()
        self.lattice = [['B'] * self.var_num for _ in range(len(self.all_block))]
        self.all_var = '\t' + '\t'.join(sorted(list(self.var.keys()), key = lambda x: self.var[x]))
        print('For program at', checking_path, ':')

    # counting the number of blocks and variables and put them in maps
    def counting(self):
        visited = set()
        remain = [self.entry]
        while remain:
            this = remain.pop()
            all_var = self.count_var(this)
            for var in all_var:
                if not var in self.var:
                    self.var[var] = self.var_num
                    self.var_num += 1

            self.all_block.append(this)
            visited.add(this)

            for link in this.exits:
                if not link.target in visited:
                    remain.append(link.target)

        self.all_block.sort(key = lambda x: x.at())
        self.blocks = {block: i for i, block in enumerate(self.all_block)}

    # return all the variables in a block
    def count_var(self, target):
        if isinstance(target, staticfg.model.Block):
            return self.count_var(target.statements)

        if isinstance(target, ast.Name):
            return [target.id]

        if isinstance(target, list):
            this_var = []
            for i in target:
                this_var.extend(self.count_var(i))
            return this_var

        if isinstance(target, ast.BinOp):
            return self.count_var(target.left) + self.count_var(target.right)

        if isinstance(target, ast.Assign):
            return self.count_var(target.targets) + self.count_var(target.value)

        return []

    # iteratively solving the fixpoint
    def fix_solve(self):
        step_count = 0
        print('step 0 :')
        self.print_lattice()

        while self.step():
            step_count += 1
            print('step', step_count, ':')
            self.print_lattice()
            None
        print('reached a fix point')

    def print_lattice(self):
        print(self.all_var)
        for block, line in zip(self.all_block, self.lattice):
            print(block.at(), '\t', end='')
            print('\t'.join(line))
        print()

    # one step solving the fixpoint, return if any change is made
    def step(self):
        new_lattice = ['B'] * len(self.blocks)

        for block_i, block in enumerate(self.all_block):
            new_lattice[block_i] = self.update_block(block)

        if new_lattice == self.lattice:
            return False
        else:
            self.lattice = new_lattice
            return True

    # use last lattice and statements in the block to update lattice of this block
    def update_block(self, block):
        this_lattice = self.last_lattice(block)
        for statement in block.statements:
            if isinstance(statement, ast.Assign):
                if len(statement.targets) == 1:
                    target = statement.targets[0]
                    target_i = self.var[target.id]
                    value = self.eval(statement.value, this_lattice)
                    this_lattice[target_i] = value

                else:
                    for target in statement.targets:
                        target_i = self.var[target.id]
                        this_lattice[target_i] = 'B'

        return this_lattice

    # <= operation of all predecessor blocks' lattices
    def last_lattice(self, block):
        pre_block = []
        for link in block.predecessors:
            pre_block.append(self.lattice[self.blocks[link.source]])

        if not pre_block:
            return ['B'] * self.var_num
        else:
            res = []
            for i in range(self.var_num):
                this = 'B'
                for j in range(len(pre_block)):
                    this = self.le(this, pre_block[j][i])
                res.append(this)
        return res

    def le(self, a, b):
        if a == 'B':
            return b
        if b == 'B':
            return a
        if a == b:
            return a
        return 'T'

    # return the even/odd status of value under env
    def eval(self, value, env):
        if isinstance(value, ast.Num):
            this_num = value.n
            if this_num % 2:
                return 'O'
            return 'E'

        if isinstance(value, ast.Name):
            return env[self.var[value.id]]

        if isinstance(value, ast.UnaryOp):
            if isinstance(value.op, ast.USub):
                return self.eval(value.operand, env)

        if isinstance(value, ast.BinOp):
            op_l = self.eval(value.left, env)
            op_r = self.eval(value.right, env)
            if isinstance(value.op, ast.Sub):
                return self.sub(op_l, op_r)

            if isinstance(value.op, ast.Add):
                return self.add(op_l, op_r)

            if isinstance(value.op, ast.Mult):
                return self.multi(op_l, op_r)
        return 'B'

    # result adding two even/odd type
    def add(self, a, b):
        if a == 'B' or b == 'B':
            return 'B'
        if a == 'T' or b == 'T':
            return 'T'
        if a == b:
            return 'E'
        return 'O'

    def sub(self, a, b):
        return self.add(a, b)

    # result multiplying two even/odd type
    def multi(self, a, b):
        if a == 'B' or b == 'B':
            return 'B'
        if a == 'E' or b == 'E':
            return 'E'
        if a == 'T' or b == 'T':
            return 'T'
        return 'O'
