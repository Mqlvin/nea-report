from abc import ABC, abstractmethod


class SourceHandler(ABC):
    '''

    returns generic comments.

    if they look like this:
    ///
    /// purpose: hi
    /// returns: hello
    ///
    it should return ['', 'purpose: hi', 'returns: hello', '']

    if they look like this
    #
    # purpose: hi
    # returns: hello
    #
    it should also return ['', 'purpose: hi', 'returns: hello', '']

    '''

    @abstractmethod
    def extract_comments(self, lined_file: list[str]) -> list[list[str]]:
        return NotImplemented


class CommentHandler(ABC):
    '''
    function is passed something like
    [
    'Name: whatever',
    'this and that',
    'purpose: whatever',
    ...
    ]

    obviously its a bit awkward because youll have to calculate when things go onto
    newlines in the function so sorry but what do you expect me to do
    '''

    @abstractmethod
    def get_features(self, comment_lines: list[str]) -> dict[str, str]:
        return NotImplemented
