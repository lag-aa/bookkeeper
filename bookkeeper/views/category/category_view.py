from PySide6.QtWidgets import (
    QTreeWidgetItem,
    QTreeWidget,
    QMenu,
    QWidget,
    QVBoxLayout,
    QInputDialog,
    QLineEdit,
    QPushButton,
)
from PySide6.QtGui import Qt
from PySide6.QtGui import QAction
from bookkeeper.models.category import Category


class CategoryWidget(QWidget):
    def __init__(self):
        """
        Widget for managing categories.

        Attributes:
            tree_widget (QTreeWidget): Widget to display categories.
            create_parent_button (QPushButton): Button to add categories to the root.
        """
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderLabels(["Категории"])

        self.create_parent_button = QPushButton("Добавить категорию в корень")
        self.create_parent_button.clicked.connect(self.add_parent_category)

        self.tree_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree_widget.customContextMenuRequested.connect(self.show_context_menu)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.tree_widget)
        self.layout.addWidget(self.create_parent_button)

    def bind_delete_category(self, handler):
        """
        Binds the delete category handler.

        Args:
            handler (Callable[[int], None]): Callback function for deleting categories.
        """
        self.handle_delete_category = handler

    def bind_add_category(self, handler):
        """
        Binds the add category handler.

        Args:
            handler (Callable[[str, int], None]): Callback function for adding categories.
        """
        self.handle_add_category = handler

    def bind_edit_category(self, handler):
        """
        Binds the edit category handler.

        Args:
            handler (Callable[[Dict[str, Any]], None]): Callback function for editing categories.
        """
        self.handle_edit_category = handler

    def show_context_menu(self, pos):
        """
        Displays the context menu.

        Args:
            pos (QPoint): Position of the context menu.
        """
        menu = QMenu(self)

        add_action = QAction("Добавить категорию", self)
        add_action.triggered.connect(self.add_category)
        menu.addAction(add_action)

        edit_action = QAction("Изменить категорию", self)
        edit_action.triggered.connect(self.edit_category)
        menu.addAction(edit_action)

        delete_action = QAction("Удалить категорию", self)
        delete_action.triggered.connect(self.delete_category)
        menu.addAction(delete_action)

        menu.exec_(self.tree_widget.mapToGlobal(pos))

    def add_category(self):
        """
        Adds a category.
        """
        category_name, ok = QInputDialog.getText(
            self, "Создание категории", "Введите название категории:"
        )

        if ok and category_name:
            selected_item = self.tree_widget.currentItem()
            parent_category = None
            if selected_item:
                parent_category = selected_item.data(0, Qt.UserRole).get("pk")
            self.handle_add_category(Category(category_name, parent_category))

    def add_parent_category(self):
        """
        Adds a parent category.
        """
        category_name, ok = QInputDialog.getText(
            self, "Создание категории", "Введите название категории:"
        )

        if ok and category_name:
            self.handle_add_category(Category(category_name))

    def edit_category(self):
        """
        Edits a category.
        """
        selected_item = self.tree_widget.currentItem()
        if selected_item:
            new_name, ok = QInputDialog.getText(
                self,
                "Редактирование категории",
                "Введите новое имя:",
                QLineEdit.Normal,
                selected_item.text(0),
            )
            category = selected_item.data(0, Qt.UserRole)
            if ok and new_name:
                new_category = {**category, "name": new_name}
                self.handle_edit_category(Category(**new_category))

    def delete_category(self):
        """
        Deletes a category.
        """
        selected_item = self.tree_widget.currentItem()

        if selected_item:
            category = selected_item.data(0, Qt.UserRole)
            self.handle_delete_category(category.get("pk"))

    def clear(self):
        """
        Clears the tree widget.
        """
        self.tree_widget.clear()

    def populate_categories(self, categories):
        """
        Populates the tree widget with categories.

        Args:
            categories (List[Category]): List of categories to populate.
        """
        self.clear()
        category_map = {}

        for category in categories:
            category_item = QTreeWidgetItem([category.name])
            category_item.setData(0, Qt.UserRole, {**vars(category)})

            if category.parent is None:
                self.tree_widget.addTopLevelItem(category_item)
            else:
                parent_item = category_map.get(category.parent)
                if parent_item is not None:
                    parent_item.addChild(category_item)
            category_map[category.pk] = category_item
