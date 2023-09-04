from copy import deepcopy
import sys
import os

# Setting the command to clear the page based on the type of platform
clear_screen = 'clear'

if sys.platform == 'win32':
    clear_screen = 'cls'


class GraphComminucation:

    # Increase the return depth if needed
    sys.setrecursionlimit(10*7)

    def __init__(self, data):
        self.data = data

    def create_target_square(self, name):
        """Place the name inside a square/rectangle"""
        return ('╔' +''.join(['═' for _ in range(len(name) + 2)]) + '╗')  + ('\n' + '║ ' + name + ' ║'  + '\n')  + ('╚' + ''.join(['═' for _ in range(len(name) + 2)]) + '╝' ) 

    def create_personal_connection(self, data):
        """Place a list of names that are inside the square next to each other"""

        _data = [GraphComminucation.create_target_square(self, i).split('\n') for i in data]


        lenght = len(data)
        connection = ""

        for i in range(3):
            temp = ""
            for j in range(lenght):

                if j == lenght - 1 and i == 1:
                    temp += _data[j][i] + ' '
                    break

                if i == 1:
                    temp += _data[j][i] + '-' #'←' #'→'
                else:
                    temp += _data[j][i] + ' '
                
            if i != 2:
                temp += '\n'

            connection += temp
        
        return connection

    def add_space(self, value, num_space=0):
        """Add an arbitrary number of spaces to the back of a string"""
        return '\n'.join([' ' * num_space + i for i in value.split('\n')])
    
    def calc_space(self, codpy_dict, old_key, new_key):
        """Calculation of the number of spaces that should be placed behind the current string based on the results before this string"""
        num_space = 0

        for item in codpy_dict[old_key]:
            if item == new_key:
                return num_space
            else:
                num_space += len(item) + 5
    
    def find_and_create_connctions(self, copy_dict, start_key, space=0, result='\nSTART\n\n', n=0):
        """Create a string of connections within a dictionary"""

        if n == 0:
            result += GraphComminucation.add_space(self, GraphComminucation.create_target_square(self, start_key), space) + '\n'
            result += GraphComminucation.add_space(self, '↓', space + 2) + '\n'
            result += GraphComminucation.add_space(self, GraphComminucation.create_personal_connection(self, self.data[start_key]), space) + '\n'
        else:
            result += GraphComminucation.add_space(self, '↓', space + 2) + '\n'
            result += GraphComminucation.add_space(self, GraphComminucation.create_personal_connection(self, self.data[start_key]), space) + '\n'

        for key in self.data[start_key]:
            if key in self.data.keys():
                del self.data[start_key]
                return GraphComminucation.find_and_create_connctions(self, copy_dict, key, space + GraphComminucation.calc_space(self, copy_dict, start_key, key), result, n=1)
        
        del self.data[start_key]

        for relict_key in self.data:

            if relict_key in result:
                result += f'\nContinue from {relict_key}\n'
            else:
                result += f"\n******Outlier******\n\n"

            return GraphComminucation.find_and_create_connctions(self, copy_dict, relict_key, space=0, result=result, n=0)
        
        return result + '\nEND'
        
    def connections(self):

        obj = GraphComminucation(self.data)
        return obj.find_and_create_connctions(deepcopy(self.data), [key for key in self.data][0])

    def __str__(self):
        """Show string that maked"""
        os.system(clear_screen)
        return GraphComminucation.connections(self)



if __name__ == '__main__':

    sample = { # A simple sample

        'a': ['b', 'c', 'd'],
        'b': ['c', 'a', 'e'],
        'c': ['b', 'd', 'f'],
        'd': ['a', 'c', 'e'],
        'e': ['d', 'f', 'b'],
        'f': ['e', 'a', 'c'],
        
    }

    connection = GraphComminucation(sample).connections()

    print(connection)
