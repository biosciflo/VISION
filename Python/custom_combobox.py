# -*- coding: utf-8 -*-
"""
custom_combobox.py

This module defines a CheckableComboBox class, which extends QComboBox to include
checkable items. This allows users to select multiple items from the combo box
list, with each item having a checkbox.

Classes:
    CheckableComboBox(QComboBox): A combo box with checkable items.

Usage:
    Import this module and use the CheckableComboBox class to create a combo box
    where items can be checked or unchecked. The checked items can be retrieved
    using the checkedItems method.
"""


from PyQt5.QtWidgets import QComboBox,QListView
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtCore import Qt

class CheckableComboBox(QComboBox):
    def __init__(self, parent=None):
        super(CheckableComboBox, self).__init__(parent)
        self.setView(QListView())
        self.view().pressed.connect(self.handleItemPressed)
        self.setModel(QStandardItemModel(self))

    def handleItemPressed(self, index):
        item = self.model().itemFromIndex(index)
        if item.checkState() == Qt.Checked:
            item.setCheckState(Qt.Unchecked)
        else:
            item.setCheckState(Qt.Checked)
        self.updateText()

    def addItem(self, text, data=None):
        item = QStandardItem()
        item.setText(text)
        item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        item.setData(Qt.Unchecked, Qt.CheckStateRole)
        self.model().appendRow(item)

    def addItems(self, texts):
        for text in texts:
            self.addItem(text)

    def checkedItems(self):
        checked_items = []
        for index in range(self.model().rowCount()):
            item = self.model().item(index)
            if item.checkState() == Qt.Checked:
                checked_items.append(item.text())
        return checked_items

    def updateText(self):
        checked_items = self.checkedItems()
        if checked_items:
            self.setEditText(", ".join(checked_items))
        else:
            self.setEditText("")
