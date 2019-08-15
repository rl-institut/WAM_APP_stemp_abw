from utils.widgets import InfoButton
from stemp_abw.app_settings import labels, TEXT_FILES

def prepare_label_data():
    return {'panels': labels()['panels'],
            'tooltips': labels()['tooltips'],
            'charts': labels()['charts']}


def create_reveal_info_button():
    """Create reveal window with trigger button with content from markdown file
    (general app info buttons, e.g. in top navigation bar)
    """
    text_data = {}
    for name, data in TEXT_FILES.items():
        f = open(data['file'], 'r', encoding='utf-8')
        text = f.read()
        text_data[name] = InfoButton(text=text,
                                     tooltip=text.split("\n")[0][2:],
                                     is_markdown=True,
                                     ionicon_type=data['icon'],
                                     ionicon_size='medium',
                                     info_id=name)
        f.close()
    return {'texts': text_data}


LABEL_DATA = prepare_label_data()
TEXT_DATA = create_reveal_info_button()
