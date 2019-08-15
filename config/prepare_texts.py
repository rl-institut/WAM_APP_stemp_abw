from utils.widgets import InfoButton
from stemp_abw.app_settings import labels, text_files

def label_data():
    return {'panels': labels()['panels'],
            'tooltips': labels()['tooltips'],
            'charts': labels()['charts']}


def text_data():
    """Create reveal window with trigger button with content from markdown file
    (general app info buttons, e.g. in top navigation bar)
    """
    text_data_store = {}
    for name, data in text_files().items():
        f = open(data['file'], 'r', encoding='utf-8')
        text = f.read()
        text_data_store[name] = InfoButton(text=text,
                                     tooltip=text.split("\n")[0][2:],
                                     is_markdown=True,
                                     ionicon_type=data['icon'],
                                     ionicon_size='medium',
                                     info_id=name)
        f.close()
    return {'texts': text_data_store}
