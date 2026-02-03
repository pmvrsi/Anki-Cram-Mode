from aqt import mw
from aqt.qt import *
from aqt.utils import showInfo, tooltip

CRAM_DECK_NAME = "Cram Mode"
TEXT_START = "⚡ Cram"     
TEXT_STOP = "🛑 Stop"

class CramModeAddon:
    def __init__(self):
        self.action = None
        self.toolbar = None
        self.setup_ui()
        
        mw.addonManager.setConfigAction(__name__, self.show_config)
        from aqt.gui_hooks import state_did_reset
        state_did_reset.append(self.update_ui_state)

    def setup_ui(self):
        self.action = QAction(TEXT_START, mw)
        self.action.setShortcut("Ctrl+Shift+C")
        self.action.triggered.connect(self.toggle_cram)
        
        mw.form.menuTools.addAction(self.action)
        
        if hasattr(mw.form, 'mainToolBar'):
            mw.form.mainToolBar.addAction(self.action)
        else:
            self.toolbar = QToolBar("Cram Mode")
            self.toolbar.setObjectName("CramModeToolbar")
            self.toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
            self.toolbar.addAction(self.action)
            mw.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolbar)

    def is_cramming(self):
        if not mw.col: return False
        return bool(mw.col.decks.id(CRAM_DECK_NAME))

    def update_ui_state(self):
        if self.is_cramming():
            self.action.setText(TEXT_STOP)
            self.action.setToolTip("Click to Restore Original Decks")
        else:
            self.action.setText(TEXT_START)
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

    def show_config(self):
        showInfo("No configuration needed.")

cram_mode = CramModeAddon()
