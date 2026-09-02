# v4 Kreator — GUI do skladu i rozbioru "jezyka AI" (NOR Protocol v4). Wersja publiczna.
# Sklad: opcje (od/do/namespace/komenda/modyfikatory) + tresc -> gotowa linia v4 do skopiowania.
# Rozbior: wklej v4 -> rozklad na jezyk (co to znaczy).
# Autor: MafiaAI — zespol ludzi i agentow AI. Wiecej: https://t8.pl
#
# Sens: skladanie jezyka v4 przestaje zalezec od tego czy model pamieta skladnie.
# Narzedzie robi to mechanicznie — zero driftu/halucynacji.
#
# Uruchomienie:  pip install PyQt6  ->  python v4_kreator_public.py

import sys

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QComboBox, QCheckBox, QPlainTextEdit,
    QGroupBox, QGridLayout,
)
from PyQt6.QtGui import QFont

import v4_core_public as v4

DARK = """
QWidget { background:#232629; color:#d3d7cf; font-family:'Segoe UI',sans-serif; font-size:13px; }
QGroupBox { border:1px solid #555; border-radius:4px; margin-top:10px; padding-top:14px; font-weight:bold; }
QGroupBox::title { color:#8ae234; subcontrol-position: top left; padding:0 6px; }
QLineEdit,QComboBox,QPlainTextEdit { background:#3c3c3c; border:1px solid #555; border-radius:3px; padding:4px 6px; }
QLineEdit:focus,QComboBox:focus,QPlainTextEdit:focus { border-color:#8ae234; }
QPushButton { background:#3c3c3c; border:1px solid #555; border-radius:3px; padding:6px 14px; }
QPushButton:hover { background:#4a4a4a; border-color:#8ae234; }
QTabBar::tab { background:#3c3c3c; border:1px solid #555; border-bottom:none;
  border-top-left-radius:4px; border-top-right-radius:4px; padding:6px 18px; margin-right:2px; font-weight:bold; }
QTabBar::tab:selected { background:#232629; color:#8ae234; }
"""

# Adresaci — podpowiedzi (pole i tak edytowalne; nazwij agentow jak chcesz)
ADRESACI = ["", "NOR", "all", "AI1", "AI2", "AI3"]


class ComposeTab(QWidget):
    def __init__(self):
        super().__init__()
        lay = QVBoxLayout(self)

        # ── Adresowanie ──
        addr = QGroupBox("Adresowanie")
        ag = QGridLayout()
        ag.addWidget(QLabel("Od (@FROM):"), 0, 0)
        self.frm = QComboBox(); self.frm.setEditable(True); self.frm.addItems(ADRESACI); self.frm.setCurrentText("NOR")
        ag.addWidget(self.frm, 0, 1)
        ag.addWidget(QLabel("Do (@TO):"), 0, 2)
        self.to = QComboBox(); self.to.setEditable(True); self.to.addItems(ADRESACI)
        ag.addWidget(self.to, 0, 3)
        self.broadcast = QCheckBox("Broadcast (do wszystkich)")
        ag.addWidget(self.broadcast, 0, 4)
        addr.setLayout(ag)
        lay.addWidget(addr)

        # ── Tresc wiadomosci ──
        msg = QGroupBox("Treść (namespace + komenda + ładunek)")
        mg = QGridLayout()
        mg.addWidget(QLabel("Obszar (namespace):"), 0, 0)
        self.ns = QComboBox()
        for n in v4.CORE_NAMESPACES:
            self.ns.addItem(f"{n}  — {v4.NS_HUMAN[n]}", n)
        mg.addWidget(self.ns, 0, 1, 1, 3)

        mg.addWidget(QLabel("Komenda:"), 1, 0)
        self.cmd = QComboBox(); self.cmd.setEditable(True)
        self.cmd.addItems([""] + v4.ALL_COMMANDS)
        mg.addWidget(self.cmd, 1, 1, 1, 3)

        mg.addWidget(QLabel("Ładunek / treść:"), 2, 0)
        self.payload = QLineEdit()
        self.payload.setPlaceholderText("treść wiadomości (dowolny język)")
        mg.addWidget(self.payload, 2, 1, 1, 3)
        msg.setLayout(mg)
        lay.addWidget(msg)

        # ── Modyfikatory ──
        mod = QGroupBox("Modyfikatory (opcjonalne)")
        og = QGridLayout()
        og.addWidget(QLabel("Priorytet:"), 0, 0)
        self.prio = QComboBox(); self.prio.addItems(v4.PRIORITY)
        og.addWidget(self.prio, 0, 1)
        og.addWidget(QLabel("@SEQ:"), 0, 2)
        self.seq = QLineEdit(); self.seq.setFixedWidth(70)
        og.addWidget(self.seq, 0, 3)
        og.addWidget(QLabel("@DEPENDS:"), 0, 4)
        self.depends = QLineEdit(); self.depends.setFixedWidth(90)
        og.addWidget(self.depends, 0, 5)
        self.parallel = QCheckBox("@PARALLEL")
        og.addWidget(self.parallel, 0, 6)
        og.addWidget(QLabel("@IF:"), 1, 0)
        self.cond = QLineEdit(); self.cond.setPlaceholderText("warunek")
        og.addWidget(self.cond, 1, 1, 1, 5)
        mod.setLayout(og)
        lay.addWidget(mod)

        # ── Podglad ──
        prev = QGroupBox("Gotowa linia v4")
        pv = QVBoxLayout()
        self.out = QPlainTextEdit(); self.out.setReadOnly(True)
        self.out.setFont(QFont("Consolas", 11)); self.out.setFixedHeight(70)
        pv.addWidget(self.out)
        row = QHBoxLayout()
        copy_btn = QPushButton("📋 Kopiuj")
        copy_btn.clicked.connect(self._copy)
        row.addWidget(copy_btn)
        row.addStretch()
        pv.addLayout(row)
        self.status = QLabel(""); self.status.setStyleSheet("color:#888;font-size:11px;")
        pv.addWidget(self.status)
        prev.setLayout(pv)
        lay.addWidget(prev)
        lay.addStretch()

        # live update
        for w in (self.frm, self.to, self.ns, self.cmd, self.prio):
            w.currentTextChanged.connect(self._update)
        for w in (self.payload, self.seq, self.depends, self.cond):
            w.textChanged.connect(self._update)
        for w in (self.broadcast, self.parallel):
            w.stateChanged.connect(self._update)
        self._update()

    def _build(self) -> str:
        return v4.compose(
            self.ns.currentData() or self.ns.currentText().split()[0],
            self.cmd.currentText(),
            self.payload.text(),
            frm=self.frm.currentText(), to=self.to.currentText(),
            broadcast=self.broadcast.isChecked(),
            priority=self.prio.currentText(), seq=self.seq.text(),
            depends=self.depends.text(), parallel=self.parallel.isChecked(),
            cond_if=self.cond.text(),
        )

    def _update(self, *_):
        try:
            self.out.setPlainText(self._build())
            self.status.setText("")
        except v4.V4Error as e:
            self.out.setPlainText("")
            self.status.setText(f"⚠ {e}")

    def _copy(self):
        t = self.out.toPlainText().strip()
        if t:
            QApplication.clipboard().setText(t)
            self.status.setText("✓ Skopiowano do schowka")


class ParseTab(QWidget):
    def __init__(self):
        super().__init__()
        lay = QVBoxLayout(self)
        lay.addWidget(QLabel("Wklej linię v4 — rozłożę ją na język:"))
        self.inp = QPlainTextEdit()
        self.inp.setFont(QFont("Consolas", 11)); self.inp.setFixedHeight(80)
        self.inp.setPlaceholderText("@VERSION[4.0]@FROM[AI1]@TO[NOR]::ACK::PROCESSED[gotowe]")
        self.inp.textChanged.connect(self._parse)
        lay.addWidget(self.inp)
        lay.addWidget(QLabel("Rozbiór:"))
        self.out = QPlainTextEdit(); self.out.setReadOnly(True)
        self.out.setFont(QFont("Segoe UI", 12))
        lay.addWidget(self.out, 1)

    def _parse(self):
        self.out.setPlainText(v4.parse_human(self.inp.toPlainText()))


class V4KreatorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("v4 Kreator — język AI (skład + rozbiór)")
        self.setGeometry(70, 50, 1000, 780)
        tabs = QTabWidget()
        tabs.addTab(ComposeTab(), "Skład (opcje → v4)")
        tabs.addTab(ParseTab(), "Rozbiór (v4 → język)")
        self.setCentralWidget(tabs)


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(DARK)
    win = V4KreatorWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
