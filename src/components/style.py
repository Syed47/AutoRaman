StyleSheet = """
    /* General Styling for the Main Window */
    QWidget {
        background-color: #2e2e2e; /* Dark background for all widgets */
        color: #ffffff; /* White text */
    }

    /* Styling for QTabWidget */
    QTabWidget::pane {
        border: 1px solid #555555; /* Darker border for tab pane */
        margin: 0px; /* Remove default margin */
        padding: 0px; /* Remove default padding */
    }
    QTabBar::tab {
        background: #3e3e3e; /* Dark tab background */
        color: #ffffff; /* White text */
        padding: 12px 8px; /* Padding for tab */
        border: 1px solid #444444; /* Darker border */
        border-bottom: none; /* Remove bottom border for selected tab */
        font-size: 14px; /* Larger font size for tabs */
        min-width: 96px;
    }
    QTabBar::tab:selected {
        background: #2e2e2e; /* Slightly darker background for selected tab */
        border-bottom: 1px solid #2e2e2e; /* Match border with background */
    }

    /* Styling for QPushButton */
    QPushButton {
        background-color: #4CAF50; /* Green background */
        color: #ffffff; /* White text */
        border: none; /* No border */
        padding: 10px 10px; /* Padding */
        font-size: 16px; /* Font size */
        border-radius: 8px;
    }
    QPushButton:hover {
        background-color: #45a049; /* Darker green on hover */
    }
    

    /* Styling for QLabel */
    QLabel {
        font-size: 14px; /* Font size for labels */
        color: #ffffff; /* White text for labels */
    }

    /* Styling for QLineEdit */
    QLineEdit {
        padding: 8px; /* Padding */
        border: 1px solid #555555; /* Dark border */
        background-color: #333333; /* Dark background */
        color: #ffffff; /* White text */
    }

    /* Styling for QCheckBox */
    QCheckBox {
        font-size: 16px; /* Font size */
        color: #ffffff; /* White text */
        spacing: 10px; /* Space between text and indicator */
        padding-left: 20px; /* Space between indicator and text */
        padding-right: 20px; /* Space between text and border */
    }
    QCheckBox::indicator::unchecked {
        border: 2px solid #777777; /* Dark border for unchecked state */
        background-color: #555555; /* Dark background for unchecked state */
    }
    QCheckBox::indicator::checked {
        border: 2px solid #4CAF50; /* Green border for checked state */
        background-color: #4CAF50; /* Green background for checked state */
    }

    /* Styling for QRadioButton */
    QRadioButton {
        font-size: 16px; /* Font size */
        color: #ffffff; /* White text */
        spacing: 10px; /* Space between text and indicator */
        padding-left: 20px; /* Space between indicator and text */
        padding-right: 20px; /* Space between text and border */
    }
    QRadioButton::indicator::unchecked {
        border: 2px solid #777777; /* Dark border for unchecked state */
        background-color: #555555; /* Dark background for unchecked state */
    }
    QRadioButton::indicator::checked {
        border: 2px solid #4CAF50; /* Green border for checked state */
        background-color: #4CAF50; /* Green background for checked state */
    }
    
    /* Styling for QTextEdit */
    QTextEdit {
        background-color: #1e1e1e; /* Dark background for text area */
        color: #ffffff; /* White text */
        border: 1px solid #555555; /* Dark border */
    }


    /* Styling for QFrame */
    QFrame {
        border: 1px solid transparent; /* Darker border for frames */

    }
    
    /* Styling for QHBoxLayout and QVBoxLayout */
    QHBoxLayout, QVBoxLayout {
        margin: 0px; /* Remove default margin */
        padding: 0px; /* Remove default padding */
    }
"""

__all__ = ['StyleSheet']
