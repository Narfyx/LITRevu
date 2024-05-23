"""
Forms for creating and editing tickets and reviews.
"""

from django import forms

from .models import Review, Ticket


class CustomClearableFileInput(forms.ClearableFileInput):
    """
    A custom clearable file input widget.

    Attributes:
        template_name (str): Path to the custom template for this widget.
    """

    template_name = "custom_widgets/custom_clearable_file_input.html"


class TicketForm(forms.ModelForm):
    """
    A form for creating and editing tickets.
    """

    class Meta:
        """
        model (Ticket): The model associated with this form.

        fields (list): List of fields to include in the form.

        widgets (dict): Custom widgets for form fields.
        """

        model = Ticket
        fields = ["title", "description", "image"]
        widgets = {
            "image": CustomClearableFileInput,
        }


class ReviewForm(forms.ModelForm):
    """
    A form for creating and editing reviews.
    """

    class Meta:
        """
        model (Review): The model associated with this form.

        fields (list): List of fields to include in the form.

        widgets (dict): Custom widgets for form fields.
        """

        model = Review
        fields = ["headline", "rating", "body"]
        widgets = {
            "rating": forms.RadioSelect(
                choices=[
                    (0, " -0"),
                    (1, " -1"),
                    (2, " -2"),
                    (3, " -3"),
                    (4, " -4"),
                    (5, " -5"),
                ],
            )
        }
