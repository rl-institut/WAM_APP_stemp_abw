from utils.widgets import InfoButton
from stemp_abw.app_settings import LABELS, TEXT_FILES

def prepare_label_data():
    return {'panels': LABELS['panels'],
            'tooltips': LABELS['tooltips'],
            'charts': LABELS['charts']}


def create_reveal_info_button():
    """Create reveal window with trigger button with content from markdown file
    (general app info buttons, e.g. in top navigation bar)
    """
    text_data = {}
    for name, data in TEXT_FILES.items():
        f = open(data['file'], 'r', encoding='utf-8')
        text_data[name] = InfoButton(text=f.read(),
                                     tooltip='',
                                     is_markdown=True,
                                     ionicon_type=data['icon'],
                                     ionicon_size='medium',
                                     info_id=name)
        f.close()
    return {'texts': text_data}


LABEL_DATA = prepare_label_data()
TEXT_DATA = create_reveal_info_button()
