from prettytable import *
import pytest
import random
import string
import functools

FUZZ_SIZE = 3
FUZZED_STYLES = []
STYLES = [DEFAULT,MSWORD_FRIENDLY,PLAIN_COLUMNS,RANDOM]

while len(FUZZED_STYLES) < FUZZ_SIZE :
    toAdd = random.randint(1,1000)
    if toAdd not in FUZZED_STYLES and toAdd not in STYLES:
        FUZZED_STYLES.append(toAdd)

# Decorator experiment to implement "before" behavior
def table(func):
    """Ensures a new table on each use"""
    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):
        args[0].table = PrettyTable() #equivalent to self.table = prettyTable()
        value = func(*args, **kwargs)
        return value
    return wrapper_decorator


class TestPrettyTable(object):

    #STYLE Expectations
    @table
    def __tableStyleHandler(self, style):
        """Tester for table Styles"""
        if style in STYLES: #If it's a good style
            try:
                self.table.set_style(style) #Set the style
            except: #and fail if an exception is raised
                pytest.fail("set_style raised Exception unexpectedly!")

        else: #If it's a bad style
            try:
                self.table.set_style(style)
                pytest.fail("Exception failed to hit")
            except Exception as e:
                assert(str(e) == "Invalid pre-set style!")


    #Style Tests

    def test_setGoodTableStyle(self):
        for style in STYLES:
            self.__tableStyleHandler(style=style)

    def test_setBadTableStyle(self):
        for style in FUZZED_STYLES:
            self.__tableStyleHandler(style=style)

    def test_setWrongTypeTableStyle(self):
        for i in range(5):
            self.__tableStyleHandler(style=random.choice(string.ascii_uppercase))


    #Column/Row Tests

    @table
    def test_addEmptyRowToEmptyTable(self):
        try:
            self.table.add_row([])
        except:
            pytest.fail("Error Adding Empty row to empty table!!")

    @table
    def test_addNonEmptyRowToEmptyTable(self):
        try:
            self.table.add_row(["fail","fail","fail"])
        except Exception as e:
            assert(str(e).startswith("Row has incorrect number of values"))

    @table
    def test_addEmptyColumnToEmptyTable(self):
        try:
            self.table.add_column("testField",[])
        except:
            pytest.fail("Error Adding Empty Column to empty table!!")

    @table
    def test_addNonEmptyColumnToEmptyTable(self):
        try:
            column = ["fail","fail","fail"]
            self.table.add_column("testField", column)
        except Exception as e:
            assert(str(e).startswith("Column length {} does not match number of rows".format(len(column))))

    @table
    def test_addRowToExistingTable(self):
        try:
            self.table.add_column("testField",[])
            self.table.add_row(["test here!"])
        except:
            pytest.fail("Error Adding row to table!!")

    @table
    def test_addColumnToExistingTable(self):
        try:
            self.table.add_column("testField",[])
            self.table.add_row(["test here!"])
            self.table.add_row(["another test here!"])
            self.table.add_column("second field", ["2nd","second"])
        except:
            pytest.fail("Error Adding column to table!!")


    def test_GoodfromHtmlOne(self):
        """Confirm an html table can be converted into a """
        try:
            #Table Source https://www.w3schools.com/html/html_tables.asp
            html="""<table>
                  <tr>
                    <th>Firstname</th>
                    <th>Lastname</th> 
                    <th>Age</th>
                  </tr>
                  <tr>
                    <td>Jill</td>
                    <td>Smith</td>
                    <td>50</td>
                  </tr>
                  <tr>
                    <td>Eve</td>
                    <td>Jackson</td>
                    <td>94</td>
                  </tr>
                  <tr>
                    <td>John</td>
                    <td>Doe</td>
                    <td>80</td>
                  </tr>
                </table>"""
            from_html_one(html)
        except:
            pytest.fail("Error creating a table!!")

    def test_BadfromHtml(self):
        """assert no table is created from a random string (theoretically possible but not realistic)"""
        randomString = "".join([random.choice(string.printable) for i in range(500)])
        assert(len(from_html(randomString)) == 0)
