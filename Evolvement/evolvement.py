from Communication.Communicationfinder import CommunicationFinder
from Show.Screensplitter import ScreenSplitter, LoadFromFile
from Show.Graphcomminucation import GraphComminucation
from Config.SetConf import account
from Show.Save import save


def get_info():
    """Get the information you need"""
    target = input('Enter your target:').strip()

    while True:
        number_of_key = input('How many users to search:').strip()
        number_of_following = input('How many following should be extracted from each user:').strip()

        if number_of_key.isdigit():
            if number_of_following.isdigit():
                return target, int(number_of_key), int(number_of_following)
            else:
                print('Please enter a number for the number of followings to be extracted')
        else:
            print('Please enter a number for the number of users')
    
def main():
    """Main program"""
    while True:

        load_file_status = input('Load file N/Y:').strip().lower()

        if load_file_status == 'y':
            
            file = LoadFromFile()
            file.get_path()
            file.read()

            break
        
        else:

            while True:

                target, number_of_key, number_of_following = get_info()
                communications = CommunicationFinder(account, target, number_of_key, number_of_following).following_extractor()

                tree = GraphComminucation(communications).connections()
                splitter = ScreenSplitter(tree)

                splitter.screen_splitter()

                save(tree)

                _continue = input('Continue N/Y:').strip().lower()

                if _continue == 'n':
                    return
                elif _continue == 'y':
                    break


main()