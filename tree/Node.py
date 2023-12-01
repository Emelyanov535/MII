class Node:
    def __init__(self, left_node=None, right_node=None, value=None, nested_tree=None, av_price=None):
        self.left_node = left_node
        self.right_node = right_node
        self.value = value
        self.av_price = av_price
        self.nested_tree = nested_tree

    def __str__(self):
        return str(self.value)

    def add_node(self, new_node):
        if not self.value:
            self.value = new_node.value
            self.nested_tree = new_node.nested_tree
            self.av_price = new_node.av_price

        if new_node.value == self.value:
            return

        if new_node.value < self.value:
            if self.left_node:
                self.left_node.add_node(new_node)
                return
            self.left_node = new_node
            return

        if new_node.value > self.value:
            if self.right_node:
                self.right_node.add_node(new_node)
                return
            self.right_node = new_node
            return

    def search(self, country: str, year: int) -> float:
        node = self.search_country(country)
        if not node:
            return
        left_year = year - 1
        right_year = year + 1
        left_year_node = None
        right_year_node = None
        while not left_year_node:
            left_year_node = node.nested_tree.search_year(left_year)
            if left_year <= 1980:
                break
            left_year -= 1

        while not right_year_node:
            right_year_node = node.nested_tree.search_year(right_year)
            if right_year >= 2020:
                break
            right_year += 1
        if left_year_node and right_year_node:
            return (left_year_node + right_year_node) / 2
        return

    def search_year(self, year: int):
        if self.value == year:
            return self.av_price

        if year < self.value:
            if not self.left_node:
                return
            return self.left_node.search_year(year)

        if year > self.value:
            if not self.right_node:
                return
            return self.right_node.search_year(year)

    def search_country(self, country: str):
        if self.value == country:
            return self

        if country < self.value:
            if not self.left_node:
                return
            return self.left_node.search_country(country)

        if country > self.value:
            if not self.right_node:
                return
            return self.right_node.search_country(country)
