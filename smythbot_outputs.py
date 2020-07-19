import datetime
class Table(object):
    def __init__(self, header_row_list, use_css = True):
        self._table_header_row = header_row_list
        self.use_css = use_css 
        self.table_body = [[]]
        self._table_size = 0
        self._table_row_index = 0
        self._table_column_index = 0
        return
        
    async def add_cell_item(self, item):
        if self._table_column_index < len(self._table_header_row):
           self.table_body[self._table_row_index].append(item)
           self._table_column_index = self._table_column_index + 1
           self._table_size = self._table_size + 1
        else:
            self._table_row_index = self._table_row_index + 1
            self._table_column_index = 0
            self.table_body.append([])
            self.table_body[self._table_row_index].append(item)
            self._table_column_index = self._table_column_index + 1
            self._table_size = self._table_size + 1
        return

    def _add_table_row(self, item):
        pass

    def _add_table_column(self, item):
        pass
        
    def remove_item(self, item):
        pass

    async def output_as_html(self):
        html_string = "<table>\n"
        if self.use_css:
            html_string = html_string + self.add_css_formatting() + "\n"
        
        # Insert table header:
        html_string = html_string + "<tr>"
        for singleHeaderItem in self._table_header_row:
            html_string = html_string +"<th>" + singleHeaderItem + "</th>"
        
        html_string = html_string + "</tr>\n"
        # Insert table body:
        for row in self.table_body:
            html_string = html_string + await self.insert_html_table_row(row)
        
        html_string = html_string + "</table>"
        return html_string

    async def insert_html_table_row(self, row_items):
        rowOutput = ""
        rowOutput = rowOutput + "<tr>"
        for item in row_items:
            rowOutput = rowOutput + "<td>" + item + "</td>"
        rowOutput = rowOutput + "</tr>"
        rowOutput = rowOutput +"\n"
        return rowOutput

    def add_header_title(self, header_title, index = -1):
        pass

    def remove_header_title(self, header_title):
        pass

    def batch_add_header_titles(self, header_list):
        pass

    def add_css_formatting(self, css_string = ""):
        style_format = """
        <style>
        table, th, td {
        border: 1px solid black;
        border-collapse: collapse;
        }
        th, td {
        padding: 5px;
        }
        </style>"""
        return style_format

    def isEmpty(self):
        if self._table_size == 0:
            return True
        else:
            return False
