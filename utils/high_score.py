class HighScore:
    """
    Manages the game's high score system.
    Keeps track of the highest score achieved in the current session.
    """
    
    def __init__(self):
        """Initialize the high score system with a starting score of 0"""
        self.high_score = 0  # Simply store in memory, no file persistence
        
    def update_high_score(self, score):
        """
        Check if the current score is a new high score and update if necessary
        
        Args:
            score (int): The score to check against the high score
            
        Returns:
            bool: True if a new high score was set, False otherwise
        """
        if score > self.high_score:
            self.high_score = score
            return True
        return False
        
    def get_high_score(self):
        """
        Retrieve the current high score
        
        Returns:
            int: The current high score
        """
        return self.high_score 