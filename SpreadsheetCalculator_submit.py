import operator
import string
import sys


def main():
    name_to_cell = {}
    all_cells = []

    # parse input
    dim = sys.stdin.readline()
    x_dim = int(dim.split(" ")[0])
    y_dim = int(dim.split(" ")[1])
    for i in range(x_dim * y_dim):
        equation_list = sys.stdin.readline().rstrip().split()
        x_coord = i % x_dim
        y_coord = i // x_dim
        newCell = Cell(x_coord, y_coord, equation_list)
        
        name_to_cell[newCell.name] = newCell
        all_cells.append(newCell)

    # generate final spreadsheet with "topological sort" like evaluation
    resulting_spreadsheet = [[0 for i in range(y_dim)] for j in range(x_dim)]
    changed = True
    while changed:
        changed = False
        cells_to_del = []
        for cell in all_cells:
            cell.try_evaluate(name_to_cell)
            if not cell.hasDependencies:
                resulting_spreadsheet[cell.x][cell.y] = cell.value
                changed = True
                cells_to_del.append(cell)
        for cell in cells_to_del:
            all_cells.remove(cell)
        

    if len(all_cells) > 0:
        print("Error: Circular dependency!")
        sys.exit()

    # print appropriate output
    print_output_spreadsheet(resulting_spreadsheet)




### FUNCTIONS ###

def matrix_coord_to_cellname(x,y):
    xAlpha = str(x+1)
    yAlpha = NUM_TO_ALPHA[y + 1]
    return yAlpha + xAlpha


def print_output_spreadsheet(spreadsheet):
    for j in range(len(spreadsheet[0])):
        for i in range(len(spreadsheet)):
            print('{0:.5f}'.format(float(spreadsheet[i][j])))


def calculate_rpn(equation_list):
    stack = []
    for elem in equation_list:
        if is_number(elem):
            stack.append(elem)
        else:
            if len(stack) < 2:
                print("Error: Bad RPN!")
                sys.exit()
            else:
                num2 = float(stack.pop())
                num1 = float(stack.pop())
                value = OP_TO_FUNCTION[elem](num1, num2)
                stack.append(value)
    if len(stack) != 1:
        print("Error: Bad RPN!")
        sys.exit()
    return stack.pop()


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False



### MODELS & CONSTANTS ###

class Cell():

    def __init__(self, x, y, equation_list):
        self.x = x
        self.y = y
        self.name = matrix_coord_to_cellname(self.x, self.y)
        self.equation_list = equation_list
        
        self.hasDependencies = False
        self.value = None
        self.try_evaluate()

    def try_evaluate(self, name_to_cell = {}):
        self.hasDependencies = False
        for i in range(len(self.equation_list)):
            elem = self.equation_list[i]
            if not is_number(elem) and elem not in OP_TO_FUNCTION:
                if elem == self.name:
                    print("Error: Circular dependency!")
                    sys.exit()
                if elem in name_to_cell and not name_to_cell[elem].hasDependencies: #elem can be resolved
                    self.equation_list[i] = name_to_cell[elem].value
                else:
                    self.hasDependencies = True

        if not self.hasDependencies:
            self.value = calculate_rpn(self.equation_list)



OP_TO_FUNCTION = {
    "+" : operator.add,
    "-" : operator.sub,
    "*" : operator.mul,
    "/" : operator.truediv
}


NUM_TO_ALPHA = dict(zip(range(1, 27), string.ascii_uppercase))
ALPHA_TO_NUM = dict(zip(string.ascii_uppercase, range(1, 27)))



### RUN MAIN ###
if __name__ == "__main__":
    main()

