# django-chess

### PersistentData Game Model :

```python
{
   'board': {[board.json]},
   'token': {
      'side': '[white/black]'
      'step': {
         'name': '[waitReadyToStart/waitCellSource/waitCellTarget/pieceMoved]'
         'data': {[step_data.json]
      }
   }
}
```

#### waitCellTarget model

```python
'waitCellTarget': {
   'sourceCell': {
      'line': '2',
      'column': 'e'
   }
}
```

#### pieceMoved model

```python
'pieceMoved': {
   'sourceCell': {
      'line': '2',
      'column': 'e'
   }
   'targetCell': {
      'line': '4',
      'column': 'e'
   },
}
```
