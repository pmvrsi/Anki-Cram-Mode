from aqt import mw
from aqt.qt import *
from aqt.utils import showInfo, tooltip

CRAM_DECK_NAME = "Cram Mode"

class CramModeAddon:
    def __init__(self):
        self.original_deck_id = None
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

        self.original_deck_id = current_deck['id']
        
        cram_did = mw.col.decks.id(CRAM_DECK_NAME)
        if not cram_did:
            cram_did = mw.col.decks.new_dyn(CRAM_DECK_NAME)
        
        deck = mw.col.decks.get(cram_did)
        
        search_term = f'deck:"{current_name}"'
        deck['terms'] = [[search_term, 9999, 5]]
        deck['resched'] = False
        
        mw.col.decks.save(deck)
        mw.col.sched.rebuild_dyn(cram_did)
        mw.col.decks.select(cram_did)
        mw.reset()
        
        card_count = mw.col.card_count(cram_did)
        try:
            tooltip(f"🔥 Cramming: {current_name} ({card_count} cards)", period=2000)
        except:
            showInfo(f"Cram Mode ON: {current_name} ({card_count} cards)")

    def stop_cram_mode(self):
        cram_did = mw.col.decks.id(CRAM_DECK_NAME)
        if cram_did:
            mw.col.sched.empty_dyn(cram_did)
            mw.col.decks.rem(cram_did, cardsToo=False)
            
            if self.original_deck_id:
                mw.col.decks.select(self.original_deck_id)
                self.original_deck_id = None
            
            mw.reset()
            
            try:
                tooltip("✅ Cram Mode OFF - Cards Returned", period=2000)
            except:
                showInfo("Cram Mode OFF")
        else:
            tooltip("Cram Mode is not active", period=1500)

cram_mode = CramModeAddon()