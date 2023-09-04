import instaloader
from itertools import chain
import progressbar

class CommunicationFinder:

    def __init__(self, your_username, target, depth_user, depth_user_following):

        self.connection = instaloader.Instaloader()
        self.connection.load_session_from_file(your_username)

        
        self.depth_user_following = depth_user_following
        self.copy_target = target
        self.target = target
        self.depth_user = depth_user
        self.delete = []
        self.result = {}
        
        self.pbar = progressbar.ProgressBar(max_value=self.depth_user)

    def finding_target_followings(self):
        """Find people followed by a target"""

        if self.target:
            # Make profile for target
            profile = instaloader.Profile.from_username(self.connection.context, self.target)
            # Extract following
            following = [_following.username for _following in list(profile.get_followees())]
            # Check lenght based on depth_user_following
            if following:
                following_lenght = len(following)

                if following_lenght < self.depth_user_following:
                    return following
                else:
                    return following[:self.depth_user_following]
            else:
                return ['private-page-0 or no-following']
        else:
            return ['']

    def find_unused_key(self):
        """Find a previously unused user as a target if you reach a point in recursive mining where growth is no longer possible."""

        # Temporarily remove the first target from the results
        CommunicationFinder.delete_root_from_result(self)

        # Sort keys from last to first except the last key used
        keys = list(self.result.keys())[::-1][1:]

        for key in keys:
            for item in self.result[key]:
                if item not in self.result.keys() and item != 'private-page-0 or no-following':
                    # Return the results to the first state
                    CommunicationFinder.add_root_to_result(self)
                    return item
    
    def delete_root_from_result(self):
        """Remove the first target from the results"""

        for user in self.result:
            for following in self.result[user]:
                if following == self.copy_target:
                    self.delete.append(user)
                    self.result[user].remove(self.copy_target)
        
        return self.result
    
    def add_root_to_result(self):
        """Add the first target to the results [reset the results to the first state]"""

        for key in self.delete:
            self.result[key].append(self.copy_target)
        
        self.delete = []
    
    def check_finish(self):
        """Checking the end of the extraction process based on the extracted results"""

        if len(self.result) == 0:
            return False

        values = list(set(list(chain.from_iterable(list(self.result.values())))))
        keys = list(self.result.keys())
        
        while 'private-page-0 or no-following' in values:
            try:
                values.remove('private-page-0 or no-following')
            except ValueError:
                pass
        
        if len(values) == len(keys):
            
            for value in values:
                if value not in keys:
                    return False
            
            return True
        
        return False
    
    def following_extractor(self):

        """The process of extracting followings"""

        self.pbar.update(len(self.result.keys()))

        # Delete None key from result
        while None in self.result.keys():
            del self.result[None]
        
        # Checking the completion of extraction
        if CommunicationFinder.check_finish(self) or len(self.result) == self.depth_user:
            return self.result
        
        self.result[self.target] = CommunicationFinder.finding_target_followings(self)

        for sub_target in self.result[self.target]:
            if sub_target not in self.result.keys():
                if sub_target == 'private-page-0 or no-following':
                    self.target = CommunicationFinder.find_unused_key(self)
                    
                else:
                    self.target = sub_target
                    
                CommunicationFinder.following_extractor(self)
        
        # Delete empty key from result
        while '' in self.result.keys():
            del self.result['']
        
        return self.result


if __name__ == '__main__':

    target = 'EXAMPLE'
    data = CommunicationFinder('YOUR_USERNAME', target, 10, 10).following_extractor()
    print(data)