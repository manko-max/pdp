"""
State Pattern Example - Digital Media Player

The State pattern allows an object to alter its behavior when its internal state changes.
Instead of using long if-else statements, each state handles its own behavior.
"""

from abc import ABC, abstractmethod


class State(ABC):
    """Abstract state interface"""
    
    @abstractmethod
    def play(self, player):
        pass
    
    @abstractmethod
    def pause(self, player):
        pass
    
    @abstractmethod
    def stop(self, player):
        pass


class PlayingState(State):
    """State when media is playing"""
    
    def play(self, player):
        print("Already playing!")
    
    def pause(self, player):
        print("Pausing...")
        player.set_state(PausedState())
    
    def stop(self, player):
        print("Stopping...")
        player.set_state(StoppedState())


class PausedState(State):
    """State when media is paused"""
    
    def play(self, player):
        print("Resuming...")
        player.set_state(PlayingState())
    
    def pause(self, player):
        print("Already paused!")
    
    def stop(self, player):
        print("Stopping...")
        player.set_state(StoppedState())


class StoppedState(State):
    """State when media is stopped"""
    
    def play(self, player):
        print("Starting playback...")
        player.set_state(PlayingState())
    
    def pause(self, player):
        print("Cannot pause - not playing!")
    
    def stop(self, player):
        print("Already stopped!")


class MediaPlayer:
    """Media player that changes behavior based on state"""
    
    def __init__(self):
        self.current_state = StoppedState()
        self.current_track = "Unknown Track"
    
    def set_state(self, new_state):
        """Change the current state"""
        self.current_state = new_state
        print(f"State changed to: {new_state.__class__.__name__}")
    
    def play(self):
        """Delegate play action to current state"""
        self.current_state.play(self)
    
    def pause(self):
        """Delegate pause action to current state"""
        self.current_state.pause(self)
    
    def stop(self):
        """Delegate stop action to current state"""
        self.current_state.stop(self)
    
    def set_track(self, track_name):
        """Set the current track"""
        self.current_track = track_name
        print(f"Track set to: {track_name}")


def main():
    """Demonstrate the State pattern with a media player"""
    
    print("=== Digital Media Player Demo ===\n")
    
    # Create media player
    player = MediaPlayer()
    player.set_track("My Favorite Song")
    
    print(f"\nCurrent state: {player.current_state.__class__.__name__}")
    print("Available actions: play, pause, stop\n")
    
    # Test different actions in different states
    
    print("--- Testing from STOPPED state ---")
    player.play()    # Should start playback
    player.pause()   # Should not work
    player.stop()    # Should not work
    
    print("\n--- Testing from PLAYING state ---")
    player.play()    # Should not work
    player.pause()   # Should pause
    player.stop()    # Should stop
    
    print("\n--- Testing from PAUSED state ---")
    player.play()    # Should resume
    player.pause()   # Should not work
    player.stop()    # Should stop
    
    print("\n--- Testing from STOPPED state again ---")
    player.play()    # Should start playback
    player.play()    # Should not work
    player.pause()   # Should pause
    player.play()    # Should resume
    player.stop()    # Should stop
    
    print("\n=== State Pattern Benefits ===")
    print("✓ Behavior changes automatically with state")
    print("✓ No long if-else statements needed")
    print("✓ Easy to add new states")
    print("✓ Each state handles its own logic")
    print("✓ Clear separation of concerns")


if __name__ == "__main__":
    main()
