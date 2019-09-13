* CamelCase classes with upper letter at the beginning
* camelCase everywhere else (files, functions, variables, etc.) with lower letter at the beginning
* Class attributes should start with _
* Use typehints where possible
  - YES:
    ```python
    def f(name: str):
    ```
  - NO:
    ```python
    def f(name):
    ```
* Use @property to give access to read only properties
  - YES:
    ```python
    @property
    def name(self):
        return self._name
    ```
  - NO:
    ```python
    def name(self):
        return self._name
    ```
* When using or defining functions with named parameters and exceeding one line, create one line per parameter, each line ending with ","
  - YES:
    ```python
    def __init__(self, name: str, *,
        command: str, 
        version: str= None,
        prettyName: str= None,
    ):
    ```
  - NO:
    ```python
    def __init__(self, name: str, *, command: str, 
        version: str= None, prettyName: str= None,
    ):
    ```
  - NO:
    ```python
    def __init__(self, name: str, *,
        command: str, version: str= None, prettyName: str= None,
    ):
    ```
  - NO:
    ```python
    def __init__(self, name: str, *,
        command: str, version: str= None, prettyName: str= None):
    ```
* Use at most one unqualified function parameter in function definitions, use ,* , to mark the remaining
  - YES:
    ```python
    def __init__(self, name: str, *,
        command: str, 
        version: str= None,
        prettyName: str= None,
    ):
    ```
  - YES:
    ```python
    def __init__(self, *, 
        name: str, 
        command: str, 
        version: str= None,
        prettyName: str= None,
    ):
    ```
  - NO:
    ```python
    def __init__(self, name: str, command: str, 
        version: str= None,
        prettyName: str= None,
    ):
    ```
  - NO:
    ```python
    def __init__(self, name: str, 
        command: str, 
        version: str= None,
        prettyName: str= None,
    ):
    ```
  - NO:
    ```python
    def __init__(self, 
        name: str, 
        command: str, 
        version: str= None,
        prettyName: str= None,
    ):
    ```
