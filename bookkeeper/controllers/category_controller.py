from bookkeeper.services.category_service import CategoryService
from bookkeeper.views.category.category_view import CategoryWidget
from bookkeeper.models.category import Category


class CategoryController:
    """
    Controller for managing categories.
    """

    def __init__(
        self, view: CategoryWidget = None, category_service: CategoryService = None
    ):
        """
        Initializes the CategoryController.

        Args:
            view (CategoryWidget, optional): The category view widget. Defaults to None.
            category_service (CategoryService, optional): The category service. Defaults to None.
        """
        self.view = view or CategoryWidget()
        self.category_service = category_service or CategoryService()
        self.populate_categories()

        self.view.bind_delete_category(self.delete_category)
        self.view.bind_add_category(self.add_category)
        self.view.bind_edit_category(self.edit_category)
        self.view.bind_update_view(self.populate_categories)

    def populate_categories(self) -> None:
        """
        Populates the category view with the required data
        """
        categories = self.category_service.get_all()
        self.view.populate_categories(categories)

    def add_category(self, category: Category) -> None:
        """
        Adds a category.

        Args:
            name (str): The name of the category.
            parent (int, optional): The ID of the parent category. Defaults to None.
        """
        self.category_service.add(category)
        self.populate_categories()

    def edit_category(self, category: Category) -> None:
        """
        Edits a category.

        Args:
            category (dict): The category data to edit.
        """
        self.category_service.update(category)
        self.populate_categories()

    def delete_category(self, pk: int) -> None:
        """
        Deletes a category.

        Args:
            category_id (int): The ID of the category to delete.
        """
        self.category_service.delete(pk)
        self.populate_categories()
