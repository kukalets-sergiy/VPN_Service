"""
    Mixin simplifies the display of error messages in Django forms by allowing you to easily display details
    about invalid fields on the page for the user.
"""

from django.contrib import messages


class ErrorFormMessagesMixin:
    def get_error_messages(self, form):
        # Create an empty list to store error messages.
        error_messages = []

        # Loop through the form's errors, which is a dictionary of field names and their error messages.
        for field_name, field_errors in form.errors.items():
            # Format the field name and its associated error messages.
            error_messages.append(f"{field_name.capitalize()}: {', '.join(field_errors)}")
        # Create an error message that lists all fields with validation errors.
        error_message = "Data error. Invalid information in the following fields:\n" + "\n".join(
            error_messages
        )

        return error_message

    def display_error_messages(self, request, form):
        # Get the formatted error message.
        error_message = self.get_error_messages(form)
        # Display the error message as a message with an error level for the user.
        messages.error(request, error_message)
