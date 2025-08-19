# lib/classes/many_to_many.py

class Article:
    all = []

    def __init__(self, author, magazine, title):
        if not isinstance(title, str) or not (5 <= len(title) <= 50):
            raise ValueError("Title must be a string between 5 and 50 characters.")
        self._title = title

        self.author = author
        self.magazine = magazine

        Article.all.append(self)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        # Ignore attempts to change title (immutable)
        pass


class Author:
    def __init__(self, name):
        if not isinstance(name, str) or len(name) == 0:
            raise ValueError("Author name must be a non-empty string.")
        self._name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        # Ignore attempts to change author name (immutable)
        pass

    def articles(self):
        return [article for article in Article.all if article.author == self]

    def magazines(self):
        mags = list({article.magazine for article in self.articles()})
        return mags if mags else None

    def add_article(self, magazine, title):
        return Article(self, magazine, title)

    def topic_areas(self):
        areas = list({magazine.category for magazine in self.magazines() or []})
        return areas if areas else None


class Magazine:
    def __init__(self, name, category):
        self._name = None
        self._category = None
        self.name = name
        self.category = category

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, str) and (2 <= len(value) <= 16):
            self._name = value
        # if invalid, ignore and keep old value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if isinstance(value, str) and len(value) > 0:
            self._category = value
        # if invalid, ignore and keep old value

    def articles(self):
        arts = [article for article in Article.all if article.magazine == self]
        return arts if arts else None

    def contributors(self):
        contribs = list({article.author for article in Article.all if article.magazine == self})
        return contribs if contribs else None

    def article_titles(self):
        titles = [article.title for article in Article.all if article.magazine == self]
        return titles if titles else None

    def contributing_authors(self):
        contribs = []
        for author in {article.author for article in Article.all if article.magazine == self}:
            if sum(1 for a in Article.all if a.magazine == self and a.author == author) > 2:
                contribs.append(author)
        return contribs if contribs else None