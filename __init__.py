from aqt import mw
from aqt.qt import *
from aqt.utils import showInfo, tooltip

CRAM_DECK_NAME = "Cram Mode"

class CramModeAddon:
    def __init__(self):
        self.setup_ui()

    def setup_ui(self):
        self.action_start = QAction("Start Cram Mode", mw)
        self.action_start.triggered.connect(self.start_cram_mode)
        mw.form.menuTools.addAction(self.action_start)

        self.action_stop = QAction("Stop Cram Mode", mw)
        self.action_stop.triggered.connect(self.stop_cram_mode)
        mw.form.menuTools.addAction(self.action_stop)

    def start_cram_mode(self):
        current_deck = mw.col.decks.current()
        current_name = current_deck['name']
        
        if current_name == CRAM_DECK_NAME:
            tooltip("Already in Cram Mode!", period=1500)
            return

        cram_did = mw.col.decks.id(CRAM_DECK_NAME)
        if not cram_did:
            cram_did = mw.col.decks.new_dyn(CRAM_DECK_NAME)
        
        deck = mw.col.decks.get(cram_did)
        
        search_term = f'deck:"{current_name}"'
        deck['terms'] = [[search_term, 9999, 5]]
        deck['resched'] = False 
        deck['dyn'] = 1
        
        mw.col.decks.save(deck)
        mw.col.sched.rebuild_dyn(cram_did)
        mw.col.decks.select(cram_did)
        mw.reset()
        
        try:
            tooltip(f"🔥 Cramming: {current_name}", period=1500)
        except:
            showInfo(f"Cram Mode ON: {current_name}")

    def stop_cram_mode(self):
        cram_did = mw.col.decks.id(CRAM_DECK_NAME)
        if cram_did:
            mw.col.decks.rem(cram_did)
            mw.reset()
            try:
                tooltip("✅ Decks Restored", period=1500)
            except:
                showInfo("Cram Mode OFF")
        else:
            tooltip("Cram Mode is not active", period=1500)

cram_mode = CramModeAddon()