import json
from html.parser import HTMLParser

class HTMLElement:

    @property
    def id(self):
        return self.attributes.get('id')

    @property
    def class_name(self):
        return self.attributes.get('class')

    def __init__(self, tag, attrs):
        self.tag = tag
        self.attributes = {
            attr_name: attr_value 
            for attr_name, attr_value in attrs
        }
        self.data = None
        self.children = []

    def __str__(self):
        attrs = " ".join(f'{attr_name}="{attr_value}"' for attr_name, attr_value in self.attributes.items())
        attrs = " " + attrs if attrs else attrs
        return f'<{self.tag}{attrs}>'

    def __repr__(self):
        return f'{self.__class__.__name__}(\'{self.__str__()}\')'


class HTMLParser2(HTMLParser):
    def __init__(self, data, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._elements = []
        self._current_element = None
        self._element_stack = []
        self.feed(data)

    def get_elements_by_tag_name(self, name: str):
        return list(filter(lambda el: el.tag == name, self._elements))

    def get_elements_by_class_name(self, name: str):
        return list(filter(lambda el: el.class_name == name, self._elements))

    def get_element_by_id(self, id: str) -> HTMLElement | None:
        return next(filter(lambda el: el.id == id, self._elements), None)

    def handle_starttag(self, tag, attrs):
        element = HTMLElement(tag, attrs)
        if self._element_stack:
            self._element_stack[-1].children.append(element)
        self._elements.append(element)
        self._element_stack.append(element)
        self._current_element = element

    def handle_data(self, data):
        if self._current_element is None:
            return
        if self._current_element.data is None:
            self._current_element.data = data.strip()
        else:
            self._current_element.data += data.strip()

    def handle_endtag(self, tag):
        if self._element_stack:
            self._element_stack.pop()
        self._current_element = self._element_stack[-1] if self._element_stack else None
