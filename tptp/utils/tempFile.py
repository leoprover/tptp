import tempfile
from pathlib import Path


class TempFileManager():

    @staticmethod
    def namedFileDescriptor(
        mode='w+b', buffering=-1, encoding=None,
        newline=None, suffix=None, prefix=None,
        dir=None, delete=True
    ):
        return tempfile.NamedTemporaryFile(
            mode=mode, buffering=buffering, encoding=encoding,
            newline=newline, suffix=suffix, prefix=prefix,
            dir=dir, delete=delete
        )

    @staticmethod
    def namedFile() -> Path:
        tempfile =  TempFileManager.namedFileDescriptor(delete=False)
        tempfile.close()
        return Path(tempfile)

