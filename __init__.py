from aqt import mw
from aqt.qt import *
from aqt.utils import tooltip

# --- Configuration ---
CRAM_DECK_NAME = "Cram Mode"
ICON_START = "⚡ Cram"    
ICON_STOP = "🛑 Stop Cram"

class CramModeAddon:
    def __init__(self):
        self.action = None
        self.setup_ui()
      
        mw.addonManager.setConfigAction(__name__, self.show_config)
        from aqt.gui_hooks import state_did_reset
        state_did_reset.append(self.update_ui_state)

    def setup_ui(self):

        self.action = QAction(ICON_START, mw)
        self.action.setShortcut("Ctrl+Shift+C")
        self.action.triggered.connect(self.toggle_cram)
        
        mw.form.mainToolBar.addAction(self.action)
        
       
        mw.form.menuTools.addAction(self.action)

    def is_cramming(self):
        """Check if the Cram Mode deck currently exists."""
        return bool(mw.col.decks.id(CRAM_DECK_NAME))

    def update_ui_state(self):
        """Update the button text/icon based on whether we are cramming."""
        if self.is_cramming():
            self.action.setText(ICON_STOP)
            # You could also set a red background or icon here
            self.action.setToolTip("Click to Restore Original Decks")
        else:
            self.action.setText(ICON_START)
            self.action.setToolTip("Click to Create Filtered Cram Deck")

    def toggle_cram(self):
        if self.is_cramming():
            self.stop_cram_mode()
        else:
            self.start_cram_mode()
        self.update_ui_state()

    def start_cram_mode(self):
        current_deck = mw.col.decks.current()
        current_name = current_deck['name']
        
        if current_name == CRAM_DECK_NAME:
            tooltip("You are already inside the Cram deck!", period=2000)
            return

        # Create/Rebuild Dynamic Deck
        cram_did = mw.col.decks.id(CRAM_DECK_NAME)
        if not cram_did:
            cram_did = mw.col.decks.new_dyn(CRAM_DECK_NAME)
        
        deck = mw.col.decks.get(cram_did)
        
        # Configuration: Random order (5), No rescheduling
        search_term = f'deck:"{current_name}"'
        deck['terms'] = [[search_term, 9999, 5]] # 5 = Random Order
        deck['resched'] = False 
        deck['dyn'] = 1
        
        mw.col.decks.save(deck)
        mw.col.sched.rebuild_dyn(cram_did)
        mw.col.decks.select(cram_did)
        mw.reset()
        
        tooltip(f"🔥 Cram Mode ON: {current_name}", period=1500)

    def stop_cram_mode(self):
        cram_did = mw.col.decks.id(CRAM_DECK_NAME)
        if cram_did:
            mw.col.decks.rem(cram_did)
            mw.reset()
            tooltip("✅ Cram Mode OFF: Decks Restored", period=1500)

    def show_config(self):
        # Placeholder if you add a settings menu later
        tooltip("No configuration needed for Cram Mode.")

# Initialize the Add-on
cram_mode = CramModeAddon()
