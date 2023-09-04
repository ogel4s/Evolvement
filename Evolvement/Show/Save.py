import os

def save(data):
    """Save results to desktop"""
    while True:

        check_save = input('Save data N/Y :').strip().lower()
        if check_save == 'y':
            
            desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop').replace('\\', '/')

            with open(desktop + '/result.txt', 'w') as file:
                for item in data.split('\n'):
                    file.write(item + '\n')
            
            print(f"File in -> {desktop}/result.txt")
            return
        
        elif check_save == 'n':
            return
