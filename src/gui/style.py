

style_sheet = """

    QTabBar::tab {
        height:24px;
        width: 110px;
        font-size: 14px;
    }

    /* Styling for QPushButton */
    QPushButton {
        background-color: #4CAF50; /* Green background */
        color: white; /* White text */
        border: none; /* No border */
        padding: 10px 20px; /* Padding */
        font-size: 16px; /* Font size */
        border-radius: 8px;
    }
    QPushButton:hover {
        background-color: #45a049; /* Darker green on hover */
    }


    /* Styling for QLabel (labels associated with QLineEdit and QRadioButton) */
    QLabel {
        font-size: 14px; /* Larger font size for labels */
    }

    /* Styling for QLineEdit */
    QLineEdit {
        padding: 8px; /* Padding */
        border: 1px solid #ccc; /* Gray border */
    }

    /* Styling for QRadioButton */
    QCheckBox {
        font-size: 16px; /* Font size */
        color: #333; /* Text color */
        spacing: 10px; /* Space between text and indicator */
        padding-left: 20px; /* Space between indicator and text */
        padding-right: 20px; /* Space between text and border */
    }
                   
    QCheckBox::indicator::unchecked {
        border: 2px solid #555; /* Border color of unchecked state */
        background-color: #EEE; /* Background color of unchecked state */
    }
    QCheckBox::indicator::checked {
        border: 2px solid #555; /* Border color of checked state */
        background-color: #4CAF50; /* Background color of checked state */
    }   
          
    /* Styling for QRadioButton */
    QRadioButton {
        font-size: 16px; /* Font size */
        color: #333; /* Text color */
        spacing: 10px; /* Space between text and indicator */
        padding-left: 20px; /* Space between indicator and text */
        padding-right: 20px; /* Space between text and border */
    }

    QRadioButton::indicator::unchecked {
        border: 2px solid #555; /* Border color of unchecked state */
        background-color: #EEE; /* Background color of unchecked state */
    }
    QRadioButton::indicator::checked {
        border: 2px solid #555; /* Border color of checked state */
        background-color: #4CAF50; /* Background color of checked state */
    }      
"""

__all__ = ['style_sheet']
