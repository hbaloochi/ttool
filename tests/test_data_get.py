from pkgutil import get_data
from ttool.data import Olist
def test_get_data():
    olist=Olist()
    assert olist.get_data() != 0
