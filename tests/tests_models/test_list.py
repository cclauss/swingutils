from javax.swing.event import ListDataEvent, ListDataListener

from swingutils.models.list import DelegateListModel
from swingutils.events import addEventListener


class TestListModel(object):
    addEvent = None
    removeEvent = None
    changeEvent = None

    def setup(self):
        self.model = DelegateListModel([])
        addEventListener(self.model, ListDataListener,
                         'intervalAdded', self.intervalAdded)
        addEventListener(self.model, ListDataListener,
                         'intervalRemoved', self.intervalRemoved)
        addEventListener(self.model, ListDataListener,
                         'contentsChanged', self.contentsChanged)

    def intervalAdded(self, event):
        self.addEvent = event

    def intervalRemoved(self, event):
        self.removeEvent = event

    def contentsChanged(self, event):
        self.changeEvent = event

    def testDelItem(self):
        self.model.append('TEST')
        self.model.append('123')
        self.model.append(456)
        assert len(self.model) == 3

        del self.model[1]

        assert self.removeEvent.index0 == 1
        assert self.removeEvent.index1 == 1
        assert len(self.model) == 2

    def testDelSlice(self):
        self.model.append('TEST')
        self.model.append('123')
        self.model.append(456)
        self.model.append(789)
        assert len(self.model) == 4

        del self.model[1:3]

        assert self.removeEvent.index0 == 1
        assert self.removeEvent.index1 == 2
        assert len(self.model) == 2

    def testAppend(self):
        self.model.append(u'Test')

        assert self.addEvent.index0 == 0
        assert self.addEvent.index1 == 0
        assert self.addEvent.type == ListDataEvent.INTERVAL_ADDED
        assert self.model[0] == u'Test'

        self.model.append(345)

        assert self.addEvent.type == ListDataEvent.INTERVAL_ADDED
        assert self.addEvent.index0 == 1
        assert self.addEvent.index1 == 1
        assert self.model[0] == u'Test'
        assert self.model[1] == 345

    def testInsert(self):
        self.model.append(u'Test')
        self.model.append(u'Test3')
        assert self.model[0] == u'Test'
        assert self.model[1] == u'Test3'

        self.model.insert(1, 'Test2')

        assert self.addEvent.index0 == 1
        assert self.addEvent.index1 == 1
        assert len(self.model) == 3
        assert self.model[1] == 'Test2'

        self.model.insert(0, 345)

        assert self.addEvent.index0 == 0
        assert self.addEvent.index1 == 0
        assert self.model[0] == 345
        assert len(self.model) == 4

    def testExtend(self):
        self.model.extend([u'Test', 'Test2', 678])

        assert self.addEvent.index0 == 0
        assert self.addEvent.index1 == 2
        assert self.model[0] == u'Test'
        assert self.model[1] == 'Test2'
        assert self.model[2] == 678

        self.model.extend([345, 7.0])

        assert self.addEvent.index0 == 3
        assert self.addEvent.index1 == 4
        assert self.model[3] == 345
        assert self.model[4] == 7.0

    def testCount(self):
        self.model.extend(['a', 'bb', 'ccc', 'bb'])

        assert self.model.count('bb') == 2

    def testIndex(self):
        self.model.extend(['a', 'bb', 'ccc', 'bb'])

        assert self.model.index('ccc') == 2

    def testRemove(self):
        self.model.extend(['a', 'bb', 'ccc', 'bb'])

        self.model.remove('bb')
        assert self.model._delegate == ['a', 'ccc', 'bb']

    def testSetSingle(self):
        self.model.append('abc')
        self.model[0] = '123'

        assert self.changeEvent.index0 == 0
        assert self.changeEvent.index1 == 0
        assert len(self.model) == 1
        assert self.model[0] == '123'

    def testSetSlice(self):
        self.model.extend([u'Test', 'Test2', 678])
        self.model[2:4] = ['abc', 'xyz', 'foo']

        assert self.changeEvent.index0 == 2
        assert self.changeEvent.index1 == 2
        assert self.addEvent.index0 == 3
        assert self.addEvent.index1 == 4

        for i, val in enumerate([u'Test', 'Test2', 'abc', 'xyz', 'foo']):
            assert self.model[i] == val

    def testSetSliceReplace(self):
        self.model.extend([u'Test', 'Test2', 678])
        self.model[:] = ['abc', 'xyz']

        assert self.changeEvent.index0 == 0
        assert self.changeEvent.index1 == 1
        assert self.removeEvent.index0 == 2
        assert self.removeEvent.index1 == 2

        for i, val in enumerate(['abc', 'xyz']):
            assert self.model[i] == val

    def testDelegateReplace(self):
        self.model.delegate = [1, 2, 3]

        assert self.addEvent.index0 == 0
        assert self.addEvent.index1 == 2
        assert self.removeEvent is None
        assert self.changeEvent is None

        self.model.delegate = [7, 6, 1, 2, 4]
        assert self.addEvent.index0 == 3
        assert self.addEvent.index1 == 4
        assert self.removeEvent is None
        assert self.changeEvent.index0 == 0
        assert self.changeEvent.index1 == 2

        del self.addEvent
        self.model.delegate = [4]
        assert self.addEvent is None
        assert self.removeEvent.index0 == 1
        assert self.removeEvent.index1 == 4
        assert self.changeEvent.index0 == 0
        assert self.changeEvent.index1 == 0
