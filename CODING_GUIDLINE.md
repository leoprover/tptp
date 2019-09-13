* CamelCase classes with upper letter at the beginning
* camelCase everywhere else (files, functions, variables, etc.) with lower letter at the beginning
* Class attributes should start with _
* Use @property to give access to read only properties
  - YES:
    ```
    @property
    def name(self):
        return self._name
    ```
  - NO:
    ```
    def name(self):
        return self._name
    ```

* When using or defining functions with named parameters and exceeding one line, create one line per parameter, each line ending with ","
  - YES:
    ```
    def __init__(self, name: str, *,
        command: str, 
        version: str= None,
        prettyName: str= None,
    ):
    ```
  - NO:
    ```
    def __init__(self, name: str, *, command: str, 
        version: str= None, prettyName: str= None,
    ):
    ```
  - NO:
    ```
    def __init__(self, name: str, *,
        command: str, version: str= None, prettyName: str= None,
    ):
    ```
  - NO:
    ```
    def __init__(self, name: str, *,
        command: str, version: str= None, prettyName: str= None):
    ```
* Use at most one unqualified function parameter in function definitions, use ,* , to mark the remaining
  - YES:
    ```
    def __init__(self, name: str, *,
        command: str, 
        version: str= None,
        prettyName: str= None,
    ):
    ```
  - YES:
    ```
    def __init__(self, *, 
        name: str, 
        command: str, 
        version: str= None,
        prettyName: str= None,
    ):
    ```
  - NO:
    ```
    def __init__(self, name: str, command: str, 
        version: str= None,
        prettyName: str= None,
    ):
    ```
  - NO:
    ```
    def __init__(self, name: str, 
        command: str, 
        version: str= None,
        prettyName: str= None,
    ):
    ```
  - NO:
    ```
    def __init__(self, 
        name: str, 
        command: str, 
        version: str= None,
        prettyName: str= None,
    ):
    ```
