from PySide6.QtWidgets import QMessageBox


def handle_error(widget, handler):
    """
    Decorator that handles exceptions and shows an error message using a QMessageBox.

    Args:
        widget: The widget to display the error message on.
        handler: The function to be decorated.

    Returns:
        The decorated function.

    Example:
        @handle_error(widget, my_function)
        def my_decorated_function():
            # Code that may raise exceptions
    """

    def inner(*args, **kwargs):
        try:
            handler(*args, **kwargs)
        except Exception as ex:
            QMessageBox.critical(widget, "Ошибка", str(ex))

    return inner
